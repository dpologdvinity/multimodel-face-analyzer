# AGENTS.md

Instructions for coding agents in this repo; `CLAUDE.md` imports this file.

Multimodel Face Analyzer is a Streamlit app: multi-backend face detection plus age, gender, race,
emotion and other per-face attributes, packaged as `face_analyzer` (src layout). Module layout:
[ARCHITECTURE.md](ARCHITECTURE.md). For UI work: [PRODUCT.md](PRODUCT.md) (audience, goals) and
[DESIGN.md](DESIGN.md) (design system).

## Before you finish

Run what applies and report each result; say so if you skipped a check.

- [ ] `ruff check .`, `ruff format --check .` and `python -m pytest -q` pass (CI runs all three on
  Python 3.11 and 3.12).
- [ ] `tests/fixtures/golden_analysis.json` is unchanged. Regenerate it
  (`UPDATE_GOLDEN=1 python -m pytest tests/test_pipeline_golden.py`) only for an intended behavior
  change, and say why; never hand-edit it or regenerate it to make a refactor pass.
- [ ] UI change: look at it in a browser (Playwright MCP) in the Night and Day themes, and with
  `FACE_ANALYZER_DEMO=1` if demo mode can reach it.
- [ ] `Dockerfile`, `requirements*.txt`, `models/manifest.json` or `tools/fetch_models.py`
  changed: verify with the `docker-tester` subagent.
- [ ] Model or preprocessing changed: re-run `tools/benchmark.py` (needs the local `assets/`
  photos) and update [docs/benchmark.md](docs/benchmark.md).
- [ ] Docs that describe what you changed (README, ARCHITECTURE, this file, `docs/`) are updated.

## How to work

Branch from `master` as `<type>/<topic>` (e.g. `fix/center-edit`) and open a pull request into
`master`; it merges once CI is green. Pick the project skill that fits:

| Task | Skill |
| --- | --- |
| Failure with an unknown or intermittent cause | `investigate-first`, then fix |
| Bug or small behavior change | `surgical-patch` (failing test first) |
| New feature or integration | `lean-build` |
| Restructure without behavior change | `safe-refactor` (the golden test is the guard) |
| Validation only, or proving work is done | `verify-and-stop` |

A new feature, user-visible redesign, new model backend or cross-module refactor starts with a
spec in `docs/agents/specs/` (what and why), then a plan in `docs/agents/plans/` (small test-first
tasks with exact files, commands and commits), both `YYYY-MM-DD-<topic>.md`; see
[past examples](docs/agents/README.md). Bug fixes and docs don't need one.

## Ground rules

- **Conventional commits** (`feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `chore:`, `ci:`),
  short imperative subject, body only when the "why" isn't obvious. Commit after every meaningful
  change; stage files explicitly (never `git add -A`).
- **No tool attribution:** no `Co-Authored-By` or other trailers, and no mention of the assistant
  in commits, product code or user-facing docs.
- **Worktrees go in `.worktrees/<name>`**, never inside `.claude/`. They share the main `.venv`;
  never `pip install -e` a worktree into it (it would repoint the package).
- Avoid Docker builds unless a change can't be verified otherwise; stop processes and containers
  you start and delete scratch files.
- PEP 257 one-line imperative docstrings; `#` comments only explain WHY. Skip vendored
  `src/face_analyzer/nets/` (also excluded from ruff).
- **Never pretend a feature works** when its model file is absent or known-bad: ship the wired-up
  code without default weights and let `Models.offline_features` say so in the sidebar.

## Commands

```bash
pip install -r requirements-dev.txt        # pinned deps + pytest + ruff + editable `-e .`
lefthook install                           # pre-commit: gitleaks, ruff check/format, typos
python tools/fetch_models.py --keys        # required detector only; --list, --all, or ARG=key pairs
streamlit run src/face_analyzer/app.py     # app
streamlit run streamlit_app.py             # public demo (demo mode, fetches demo weights once)
./install-and-run.sh                       # guided native install of optional heavy deps
./build-and-run.sh                         # guided Docker build + run (port 8501)
```

Tests that need weights or local photos skip via `tests/_models.py`; point them at real weights
with `FACE_ANALYZER_MODEL_DIR=/path/to/models`.

## Environment variables

None are required and the app reads no secrets.

| Variable | Effect |
| --- | --- |
| `FACE_ANALYZER_MODEL_DIR` | Load and fetch weights here instead of `models/`. |
| `FACE_ANALYZER_DEMO` | Truthy value turns on demo mode. |
| `FACE_ANALYZER_ORT_THREADS` | onnxruntime thread count. |
| `AGE_MODEL`, `RACE_MODEL`, ... (the Docker build ARG names) | Comma-separated backends the native app may load (empty = none, unset = all present). Set by `install-and-run.sh`. |

## Invariants and gotchas

- **Pins must resolve on Python 3.11** (Docker, dev container) and 3.12 (CI, local `.venv`). CI
  fetches only the required ~3 MB of weights; never make it fetch the optional ones (several GB).
- **Weights live outside git**, listed in `models/manifest.json`. To add or change one, follow
  [docs/setup.md](docs/setup.md#adding-or-changing-a-model-file); tests enforce the manifest, the
  pinned mirror revision and the ignore-file exceptions. Check files through `load_models()` /
  `_present()` (an old LFS pointer counts as absent), never a bare `.exists()`.
- Never check out an old branch that still tracks the weights in git-lfs in the main checkout
  (use a worktree): switching back deletes the ignored local copies, including the
  bring-your-own `dan`/`deep3d` files that can't be downloaded again.
- Model lists are ordered most-accurate-first. A new model, fusion or stacker ships only if its
  paired confidence interval against the shipped answer is above zero.
- **Evaluation** uses its own Python 3.11 venv, `.venv-eval`; never install eval packages into
  `.venv`. Setup in [docs/setup.md](docs/setup.md#held-out-evaluation), method and results in
  [docs/eval/](docs/eval/).
- Detection needs any one detector, not SSD (`resolve_face_detector()` falls back to SSD, then
  any loaded detector).
- `requirements.txt` is also the Streamlit Community Cloud install file: it must survive a plain
  `pip install -r` (no mediapipe, which drags in opencv-contrib 5.x).
- **Demo mode:** gate any feature that persists or shares faces on `is_demo_mode()`. The demo
  loads only the `DEMO_MODELS` allowlist (hf-mirrored, no torch/TF, RetinaFace not SSD). Don't
  track a `.streamlit/config.toml`; it would apply to local dev too.
- Theme colour tokens in `ui/theme.css` stay plain `#rrggbb` (`tests/test_theme.py` checks WCAG
  AA). The CSS is read once per process: restart Streamlit to see edits.
- Live webcam state is per-session (`new_live_session()`), never module-level.
- **Imports:** relative inside the package; absolute only in `app.py` (run as a script),
  `tests/` and `tools/`. `inference.py` re-exports public names only. `try/except ImportError`
  only for optional dependencies (torch, tensorflow, mediapipe, onnxruntime, scipy).
- Local-only, untracked: `data/` (FairFace and eval cache), `assets/` (benchmark photos), `tmp/`,
  `ideas/`.

## Responsible use

The README's [Responsible use](README.md#responsible-use) section applies to the code you write.

- Present age, gender, race and emotion as appearance-based guesses, never facts about a person.
- Don't add features that identify, track or profile people (new recognition or search paths,
  cross-photo tracking, exporting face data) without the owner's explicit sign-off.
- Storing a face stays an explicit user action and is disabled in demo mode.

## Agent configuration

- **Skills:** `.agents/skills/` (with Codex metadata in `agents/openai.yaml`); `.claude/skills/`
  symlinks to them. To add Streamlit's bundled skill locally (the links are gitignored):

  ```bash
  ln -s "$(.venv/bin/python -c 'import pathlib, streamlit; print(pathlib.Path(streamlit.__file__).parent / ".agents/skills/developing-with-streamlit")')" .agents/skills/
  ln -s ../../.agents/skills/developing-with-streamlit .claude/skills/
  ```

- **Subagent:** `docker-tester` (`.claude/agents/`, Codex: `.codex/agents/`, same instructions).
- **MCP:** Playwright, in `.mcp.json`.
- **Plugins:** `impeccable` and `commit-commands` (`.claude/settings.json`); `python-skills` for
  Codex (`.codex/config.toml`).
- Personal, untracked: `.claude/settings.local.json`, `CLAUDE.local.md`, `STEPS-FOR-OWNER.md`.
