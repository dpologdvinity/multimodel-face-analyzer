## What and why

<!-- What this changes and why. Link the issue, spec or plan if there is one. -->

## How it was checked

- [ ] `ruff check .`, `ruff format --check .` and `python -m pytest -q` pass
- [ ] `tests/fixtures/golden_analysis.json` is unchanged, or the change is intended and explained above
- [ ] UI change: looked at in the Night and Day themes (and in demo mode, if it can reach it)
- [ ] Docker inputs changed (`Dockerfile`, `requirements*.txt`, `models/manifest.json`, `tools/fetch_models.py`): the image was built and booted
- [ ] Model or preprocessing changed: `tools/benchmark.py` re-run and `docs/benchmark.md` updated
- [ ] Docs that describe the change are updated
