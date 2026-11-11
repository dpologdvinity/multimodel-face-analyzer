# Contributing

Thanks for your interest in Multimodel Face Analyzer. This guide covers local setup, the
checks a change must pass, and how commits and pull requests are shaped. The repo's invariants
(model weights, demo mode, themes, imports) are listed in [AGENTS.md](AGENTS.md), and the module
layout in [ARCHITECTURE.md](ARCHITECTURE.md); read both before a non-trivial change.

## Local setup

Python 3.11 or 3.12.

```bash
git clone https://github.com/dpologdvinity/multimodel-face-analyzer.git
cd multimodel-face-analyzer
python -m venv .venv && . .venv/bin/activate     # or: uv venv && . .venv/bin/activate
pip install -r requirements-dev.txt              # pinned deps, pytest, ruff, and `-e .`
python tools/fetch_models.py --keys              # required detector only (~3 MB)
streamlit run src/face_analyzer/app.py
```

Optional backends need their weights: `python tools/fetch_models.py --list` shows every file,
its license and source; `--keys AGE_MODEL=fairface ...` fetches a selection. See
[docs/setup.md](docs/setup.md) for optional dependencies and Docker.

Install the pre-commit hooks with [lefthook](https://lefthook.dev): `lefthook install`. They run
gitleaks, `ruff check`, `ruff format --check` and [typos](https://github.com/crate-ci/typos) on
staged files.

## Checks

CI runs these on Python 3.11 and 3.12; run them before you push:

```bash
ruff check .
ruff format --check .
python -m pytest -q
```

Tests that need optional weights or local photos skip when the files are missing.
`tests/test_pipeline_golden.py` pins the pipeline's output: a refactor must keep it green
without touching `tests/fixtures/golden_analysis.json`. Regenerate it
(`UPDATE_GOLDEN=1 python -m pytest tests/test_pipeline_golden.py`) only for an intended
behavior change, and say so in the pull request. After changing a model or its preprocessing,
re-run `tools/benchmark.py`.

## Branches, commits and pull requests

- Branch from `master` as `<type>/<topic>`, e.g. `feat/input-first` or `fix/center-edit`.
- Use [Conventional Commits](https://www.conventionalcommits.org/): `feat:`, `fix:`,
  `refactor:`, `test:`, `docs:`, `chore:`, `ci:`, with a short imperative subject. Keep commits
  small and atomic; add a body only when the "why" isn't obvious.
- Bug fixes start with a failing test that reproduces the bug.
- Update README.md, ARCHITECTURE.md, AGENTS.md or `docs/` when a change affects what they
  describe.
- Open a pull request against `master`; it merges once CI is green.

## Model weights and licensing

Never commit weights. Add new models to `models/manifest.json` (a test checks every model path
has an entry) and record their license in [MODEL_LICENSES.md](MODEL_LICENSES.md). Code
contributions are accepted under the project's [MIT License](LICENSE).
