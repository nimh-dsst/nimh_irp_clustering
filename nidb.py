"""Fetch and parse NIH IRP annual reports from intramural.nih.gov.

The FY2018 and FY2021 rounds did this inline in the notebook, keying on
``class="headings"`` / ``class="data"``. Those classes no longer exist. Current
markup (verified Aug 2026) lays each report out as a flat sequence inside
``div.datacontainer``::

    <div class="headinggrid">Report Title</div>       <- label
    <div class="easygrid">Studies of ...</div>        <- value
    <div class="headinggrid">Research Organization</div>
    <div style="margin: ...">Section on ...</div>     <- value, no class
    <div class="headinggrid">Collaborators from other NIMH organizations</div>
    <div class="morelist">There were 3 collaborators within NIMH</div>
    <div class="collabgrid">                          <- value, paired cells
      <div>Elizabeth Day Ballard, PhD</div>
      <div style="font-size:0.9em;">Experimental Therapeutics ...</div>
      ...
    </div>

So the parse rule is: a ``headinggrid`` labels the sibling divs that follow it,
up to the next ``headinggrid``. Value divs do not reliably carry a class, so we
key on position rather than class. Inside a ``collabgrid`` the cells strictly
alternate name / institution, with the institution cell marked by its inline
``font-size:0.9em``.

Field names here deliberately match the headings, so the ``col_rn`` rename and
everything downstream of it in the notebook keep working unchanged.
"""

from __future__ import annotations

import re
import time

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://intramural.nih.gov/search/searchview.taf"

# Without this parameter every URL returns a ~381-byte JavaScript redirect stub
# instead of the report. The site appends it client-side; requests will not.
RELOAD_PARAM = "nidbreload=true"

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)

# Headings whose values are collaborator lists. Keys are matched as substrings
# because the site switches between singular and plural with the count
# ("External Collaborator" vs "External Collaborators").
COLLAB_HEADINGS = {
    "Collaborators from other NIMH organizations": "Collaborators from other NIMH organizations",
    "Collaborators from other NIH organizations": "Collaborators from other NIH organizations",
    "External Collaborator": "External Collaborators",
}

_WS = re.compile(r"\s+")


class ReportFetchError(RuntimeError):
    """A report page could not be retrieved."""


def report_url(ipid: int | str) -> str:
    """Return the report page URL for an ipid."""
    return f"{BASE_URL}?ipid={ipid}&{RELOAD_PARAM}"


def make_session() -> requests.Session:
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT
    return session


def fetch_report(
    ipid: int | str,
    session: requests.Session | None = None,
    *,
    timeout: int = 30,
    retries: int = 3,
    backoff: float = 2.0,
) -> str:
    """Fetch one report page, retrying on transport errors.

    Raises ReportFetchError if the page never arrives, or arrives as the
    redirect stub (which means the ipid does not resolve to a report).
    """
    session = session or make_session()
    url = report_url(ipid)
    last_error: Exception | None = None

    for attempt in range(retries):
        try:
            response = session.get(url, timeout=timeout)
            response.raise_for_status()
        except requests.RequestException as exc:  # transport or HTTP error
            last_error = exc
        else:
            html = response.text
            if "Not a valid Report request" in html or len(html) < 1000:
                raise ReportFetchError(f"ipid {ipid} does not resolve to a report")
            return html
        if attempt < retries - 1:
            time.sleep(backoff * (attempt + 1))

    raise ReportFetchError(f"ipid {ipid} failed after {retries} attempts: {last_error}")


def _clean(text: str) -> str:
    """Collapse whitespace, including the non-breaking spaces the site pads with."""
    return _WS.sub(" ", text.replace("\xa0", " ")).strip()


def _clean_name(text: str) -> str:
    """Tidy a person's name without collapsing runs of spaces.

    The site renders names as "First Middle Last" and leaves a double space where
    there is no middle name, so 648 of the 1086 names in the FY2021 round look
    like "Joyce  Chung, MD". The hand-curated collab_corrections and drop_list
    entries are keyed on those exact strings, so collapsing the spaces here would
    silently break every one of those lookups. Institution names never have this
    quirk, so they use _clean instead.
    """
    return re.sub(r"[\t\r\n]+", " ", text.replace("\xa0", " ")).strip()


def _parse_pigrid(grid) -> str:
    """Return the investigator name(s) from a pigrid.

    FY2025 pages append an "IRP Faculty Profile" link inside this block, which
    would otherwise end up glued to the name. Multiple investigators are joined
    with "; ", which is the separator the notebook's label code splits on.
    """
    for link in grid.find_all("a"):
        link.decompose()
    names = [
        _clean_name(cell.get_text(" ", strip=True))
        for cell in grid.find_all("div", recursive=False)
    ]
    return "; ".join(n for n in names if n)


def _strip_link_decorations(container) -> None:
    """Remove the site's inline link chrome.

    FY2025 summaries interleave "PubMed ID 39441700 / Pubmed Central ID 11586909"
    link labels with the prose. They are markup, not part of the field, and they
    end up in pj_text if left alone.
    """
    for element in container.find_all(
        attrs={"class": ["showlinkpmid", "showlinkpmcid", "showlink", "showlinknospace"]}
    ):
        element.decompose()


def _extract_publications(container) -> str | None:
    """Pull the publications block out of the tree and return its text.

    This block is nested *inside* the Summary value on FY2021 pages and sits as
    an unclassed sibling on FY2025 pages. Either way it has to come out before
    the main walk, or its text gets attributed to whatever field precedes it.
    """
    # Extract each publication element wherever it sits, rather than trying to
    # find one enclosing block: the nesting differs by year, and on FY2021 pages
    # the heading's siblings are at a different level from the citation list.
    parts = []
    for element in container.find_all(attrs={"class": ["publistgrid", "pubmedlinksgrid"]}):
        parts.append(_clean(element.get_text(" ", strip=True)))
        element.extract()

    # The accession numbers live in a separate div after each citation. Keep them
    # with the publication text — they are the useful part — but get them out of
    # the tree so they stop landing in Summary.
    for element in container.find_all(attrs={"class": "nolink"}):
        text = _clean(element.get_text(" ", strip=True))
        if re.search(r"(PubMed|Pubmed Central) ID\b", text):
            parts.append(text)
            element.extract()

    boilerplate = re.compile(
        r"Publications Generated|Project Bibliography|Ordered by (reference|publication)"
    )
    for element in container.find_all(["div", "span"]):
        text = element.get_text(" ", strip=True)
        if text and boilerplate.search(text) and not element.find(["div", "span"]):
            element.extract()

    return " ".join(p for p in parts if p) or None


def _parse_collabgrid(grid) -> list[list[str]]:
    """Return [name, institution] pairs from a collabgrid.

    Cells alternate name / institution. The institution cell is the one carrying
    an inline font-size, which is what we key on rather than trusting position,
    so a stray empty cell cannot silently shift every pair by one.
    """
    pairs: list[list[str]] = []
    pending: str | None = None

    for cell in grid.find_all("div", recursive=False):
        is_institution = "font-size" in (cell.get("style") or "")
        raw = cell.get_text(" ", strip=True)
        text = _clean(raw) if is_institution else _clean_name(raw)
        if is_institution:
            if pending is not None:
                pairs.append([pending, text])
                pending = None
            elif text:
                # Institution with no preceding name; keep it rather than drop it.
                pairs.append(["", text])
        elif text:
            if pending is not None:
                # Two names in a row means the institution cell was missing.
                pairs.append([pending, ""])
            pending = text

    if pending is not None:
        pairs.append([pending, ""])
    return pairs


def parse_report(html: str, ipid: int | str | None = None) -> dict:
    """Parse a report page into one flat record.

    Collaborator fields come back as lists of [name, institution] pairs, matching
    the shape the notebook's downstream code already expects.
    """
    soup = BeautifulSoup(html, "lxml")
    record: dict = {}

    if ipid is not None:
        record["ipid"] = str(ipid)
        record["url"] = report_url(ipid)

    label = soup.find(attrs={"class": "contentlabel"})
    record["pj_num"] = _clean(label.get_text()) if label else None

    container = soup.find(attrs={"class": "datacontainer"})
    if container is None:
        raise ValueError(f"no datacontainer in report {ipid} (page structure changed?)")

    # Both must happen before the walk: these sit inside other fields' values,
    # so leaving them in place bleeds citation text into Summary.
    _strip_link_decorations(container)
    record["Publications Generated"] = _extract_publications(container)

    # Walk the flat sequence, attributing each value div to the heading above it.
    current: str | None = None
    values: list = []

    def flush() -> None:
        if current is None:
            return
        if current in COLLAB_HEADINGS.values():
            pairs = [p for group in values for p in group]
            record[current] = pairs or None
        else:
            text = " ".join(v for v in values if v).strip()
            # Don't let an empty repeat heading clobber a value already captured.
            if text or current not in record:
                record[current] = text or None

    for element in container.find_all("div", recursive=False):
        classes = element.get("class") or []
        if "headinggrid" in classes:
            heading = _clean(element.get_text(" ", strip=True))
            # Some headings carry their value inline rather than in a sibling.
            inline = ""
            nested = element.find(attrs={"class": ["easygrid", "collabgrid", "morelist"]})
            if nested is not None:
                inline = _clean(nested.get_text(" ", strip=True))
                heading = _clean(heading.replace(inline, ""))

            flush()
            current, values = _normalise_heading(heading), []
            if inline:
                values.append(inline)
            continue

        if current is None:
            continue

        if "collabgrid" in classes:
            values.append(_parse_collabgrid(element))
        elif "pigrid" in classes:
            values.append(_parse_pigrid(element))
        elif "morelist" in classes:
            # The "There were 3 collaborators within NIMH" count line. Redundant
            # with the grid itself, and it would pollute a text field.
            continue
        else:
            values.append(_clean(element.get_text(" ", strip=True)))

    flush()

    record["fiscal_year"] = _fiscal_year(soup)
    record["more_references"] = "See Project Bibliography" in html
    return record


def _normalise_heading(heading: str) -> str:
    """Map a raw heading to a stable field name."""
    for needle, field in COLLAB_HEADINGS.items():
        if needle in heading:
            return field
    if "Lab Staff and Collaborators" in heading:
        # Heading embeds the organization name: "... within the Section on X".
        return "Lab Staff and Collaborators"
    if "Publications Generated" in heading:
        return "Publications Generated"
    if heading.endswith("Fiscal Year"):
        return "report_period"
    return heading


def _fiscal_year(soup: BeautifulSoup) -> int | None:
    """Pull the fiscal year out of the '<YYYY> Fiscal Year' heading."""
    for element in soup.find_all(attrs={"class": "headinggrid"}):
        match = re.search(r"\b(20\d{2})\s+Fiscal Year\b", element.get_text(" ", strip=True))
        if match:
            return int(match.group(1))
    return None


def scrape_reports(
    ipids,
    *,
    expect_fy: int | None = None,
    delay: float = 0.5,
    session: requests.Session | None = None,
    progress_every: int = 25,
) -> tuple[list[dict], list[tuple[str, str]]]:
    """Fetch and parse many reports.

    Returns (records, errors). Pass expect_fy to assert every report is from the
    year you think it is — ipids are not namespaced by year, and a stale ipid
    list silently yields the wrong year's data, which is the failure mode most
    likely to go unnoticed.
    """
    session = session or make_session()
    records: list[dict] = []
    errors: list[tuple[str, str]] = []
    ipids = list(ipids)

    for index, ipid in enumerate(ipids, start=1):
        try:
            record = parse_report(fetch_report(ipid, session=session), ipid)
        except (ReportFetchError, ValueError) as exc:
            errors.append((str(ipid), str(exc)))
        else:
            if expect_fy is not None and record.get("fiscal_year") != expect_fy:
                errors.append(
                    (str(ipid), f"expected FY{expect_fy}, got FY{record.get('fiscal_year')}")
                )
            else:
                records.append(record)

        if progress_every and index % progress_every == 0:
            print(f"  {index}/{len(ipids)} fetched, {len(errors)} error(s)")
        if delay:
            time.sleep(delay)

    return records, errors
