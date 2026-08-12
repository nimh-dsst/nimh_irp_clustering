# nimh_irp_clustering

This repo contains the code for an analysis of collaborations within the NIMH IRP based on collaborators reported in investigator's annual reports available from https://nidb.nih.gov. This analysis was requested from the Scientific Director's office (Jenny Mehren) and originally conducted by Dylan Nielson in 2019, using FY2018 annual reports. It was re-run on FY2021 reports in 2022, and on FY2025 reports in 2026 (with Claude Code assisting on the 2026 round).

See [ANALYSIS.md](ANALYSIS.md) for how to run a round, what each round reported,
and which parts are known to break between rounds.

```bash
uv sync
uv run jupyter lab
```
