# AGENTS.md

Instructions for coding agents (Codex, Claude Code, and any tool that reads `AGENTS.md`) working
in this repository. `CLAUDE.md` is a one-line `@AGENTS.md` import, so this file is the single
source of truth. Keep it, [README.md](README.md) and [ARCHITECTURE.md](ARCHITECTURE.md) current
whenever a change affects what they describe.

The repo is a Streamlit face analyzer: multi-backend face detection plus age, gender, race,
emotion and other per-face attributes, packaged as `face_analyzer` (src layout). Product context
for UI work is in [PRODUCT.md](PRODUCT.md) and the design system in [DESIGN.md](DESIGN.md).

## Ground rules

- Avoid Docker builds unless a change can't be verified otherwise; stop processes/containers
  you start and delete scratch files when done.
- **No tool attribution in commits:** commit messages carry no `Co-Authored-By` or other
  trailers and don't mention the assistant that wrote them. Keep product code and user-facing
  docs free of tool mentions; agent tooling belongs in the agent files listed below.
- **Conventional commits** (`feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `chore:`, `ci:`),
  short imperative subject, body only when the "why" isn't obvious. Commit after every
  meaningful change; stage files explicitly (never `git add -A`).
- **Worktrees go in `.worktrees/<name>`**, never inside `.claude/`. Worktrees share the main
  checkout's `.venv`; never `pip install -e` a worktree into it (it would repoint the package).
- **Docstrings and comments:** PEP 257 one-line imperative docstrings; `#` comments only to
  explain WHY. Skip vendored code in `src/face_analyzer/nets/` (also excluded from ruff).
- **Never pretend a feature works** when its model file is absent or known-bad. Features whose
  only known weights are broken, gated or unlicensed ship wired-up code with no default weights;
  `Models.offline_features` surfaces this in the sidebar.

## Commands

```bash
pip install -r requirements-dev.txt        # pinned runtime deps + pytest + ruff + `-e .`
ruff check .                               # lint (ruff version pinned in requirements-dev.txt)
ruff format --check .                      # formatting (CI and the pre-commit hook enforce it)
python -m pytest -q                        # tests; CI runs this on Python 3.11 and 3.12
lefthook install                           # pre-commit: gitleaks, ruff check/format, typos
streamlit run src/face_analyzer/app.py     # app (native; needs the editable install)
streamlit run streamlit_app.py             # public demo: forces demo mode, fetches demo weights once
./install-and-run.sh                       # guided native install of optional heavy deps
./build-and-run.sh                         # guided Docker build + run (port 8501)
```

- Weights are not in git: `python tools/fetch_models.py --keys AGE_MODEL=fairface ...` (or `--all`,
  `--list`) downloads them per `models/manifest.json` (size, sha256, license, build-arg keys,
  `source` hf/upstream/manual). Stdlib only.
- pytest needs no install (`pythonpath = ["src"]` in `pyproject.toml`). Tests needing model
  weights or local photos skip via `tests/_models.py` (`require_model`, `require_local_data`)
  when the file is missing (or an old git-lfs pointer). Point loading at real weights elsewhere
  with `FACE_ANALYZER_MODEL_DIR=/path/to/models`.
- **`tests/test_pipeline_golden.py` is the behavior safety net.** Never hand-edit
  `tests/fixtures/golden_analysis.json` or regenerate it during a refactor; only run
  `UPDATE_GOLDEN=1 python -m pytest tests/test_pipeline_golden.py` for an intended behavior change.
- The package is installed editable everywhere (`requirements-dev.txt` ends with `-e .`; the
  Dockerfile and `install-and-run.sh` run `pip install --no-deps -e .`) so `BASE_DIR` stays the
  repo root.
- Per-feature model lists are ordered most-accurate-first; re-run `tools/benchmark.py` after
  changing any model or its preprocessing.

## Environment variables

None are required and the app reads no secrets.

| Variable | Effect |
| --- | --- |
| `FACE_ANALYZER_MODEL_DIR` | Load and fetch weights from this directory instead of `models/`. |
| `FACE_ANALYZER_DEMO` | Truthy value turns on demo mode (see below). |
| `FACE_ANALYZER_ORT_THREADS` | onnxruntime thread count. |
| `AGE_MODEL`, `GENDER_MODEL`, `EMOTION_MODEL`, `RACE_MODEL`, ... | Same names as the Docker build ARGs. A comma-separated list restricts which backends the native app loads (empty = none); unset loads whatever is present. Set by `install-and-run.sh`. |

## Evaluation and experiments

- **Held-out eval (FairFace)** runs in its own Python 3.11 venv `.venv-eval` (gitignored; install
  steps in [docs/setup.md](docs/setup.md)). Never install into `.venv`, and keep scikit-learn
  (for `tools/fit_stacker.py`) there too. `.venv-eval/bin/python tools/fetch_fairface.py`
  (default 1.25 padding; 0.25 crops break SSD), then
  `FACE_ANALYZER_MODEL_DIR=$PWD/models .venv-eval/bin/python tools/eval_heldout.py --n 2000`
  (~2.5 h on 2 cores, resumable; `--score-only` re-scores `data/eval_cache/` without models;
  `--extra-age KEY=model.onnx` scores a non-app age model on the same crops). Writes
  `docs/eval/heldout_fairface.json`; the doc tables come from its stdout.
  `tests/test_heldout_eval.py` covers the pure scoring code and runs in CI without data.
- A stacker or new model ships only if its paired CI against the shipped answer is above zero.
- **Age model experiment (not adopted):** `tools/kaggle/age_model/` holds the Kaggle kernels and
  `faceprep.py`, the torch-free crop rebuild that `tests/test_age_model_parity.py` pins to the
  app's input. `tools/eval_utkface.py` is the UTKFace OOD eval. Results: `docs/eval/age_model.md`.

## Invariants and gotchas

- **Pins must resolve on Python 3.11** (Docker base `python:3.11-slim`, dev container) and 3.12
  (CI, local `.venv`). CI fetches only the required files (`fetch_models.py --keys`, about 3 MB);
  never make it fetch the optional weights (several GB).
- **Weights live outside git** (moved off git-lfs; history kept). `models/*` is gitignored except
  the manifest and its `"in_git": true` files; `.gitignore` and `.dockerignore` exceptions must
  match those entries (a test checks), and every model path in `core/constants.py` needs a
  manifest entry (a test checks). License decides `source`: permissive -> `hf` (mirror
  `kaitlynbassford/face-analyzer-weights`; upload there and update its model card),
  restricted/unclear -> `upstream` (original URL, pinned), no direct URL -> `manual`. Keep
  `MODEL_LICENSES.md` in sync. `hf` URLs are pinned to `hf_revision`; after changing HF files,
  re-pin all of them.
- Never check out an old branch that still tracks the weights under git-lfs in the main
  checkout (use a worktree): switching back deletes the ignored local copies, including the
  bring-your-own `dan`/`deep3d` files that cannot be downloaded again.
- Check model files through `load_models()` / `_present()` in `pipeline/loader.py` (treats an old
  LFS pointer as absent), never with a bare `.exists()`.
- Face detection needs any one detector, not SSD: `detectors/factory.py`
  `resolve_face_detector()` falls back to SSD, then any loaded detector.
- `requirements.txt` is also the Streamlit Community Cloud install file: keep it free of anything
  that breaks a plain `pip install -r` (no mediapipe: it drags in opencv-contrib 5.x).
- **Demo mode** (`FACE_ANALYZER_DEMO=1`, `demo.py`): any new feature that persists or shares
  faces must be gated on `is_demo_mode()`. The demo loads only the `DEMO_MODELS` allowlist
  (hf-mirrored, no torch/TF; RetinaFace, never SSD). Don't add a tracked
  `.streamlit/config.toml`: it would apply to local dev too.
- **Themes:** colour tokens in `ui/theme.css` stay plain `#rrggbb`; `tests/test_theme.py` parses
  them and enforces WCAG AA. `theme.css` is read once per process: restart Streamlit to see edits.
- Live webcam state is per-session (`new_live_session()` on every script run), never module-level.
- **Imports:** relative inside the package; absolute (`from face_analyzer import inference`) only
  in `app.py` (run as a script), `tests/` and `tools/`. `inference.py` re-exports public names
  only; import private helpers from their defining module. `try/except ImportError` is reserved
  for genuinely optional dependencies (torch, tensorflow, mediapipe, onnxruntime, scipy).
- Local-only, untracked data: `data/` (FairFace + eval cache), `assets/` (benchmark photos for
  `tools/benchmark.py` and `tools/ground_truth.json`), `tmp/`, `ideas/`.

## Agent workflow

- **Skills:** `.agents/skills/` holds the repo's skills (`investigate-first`, `lean-build`,
  `safe-refactor`, `surgical-patch`, `verify-and-stop`), each with Codex metadata in
  `agents/openai.yaml`. `.claude/skills/` symlinks to them so Claude Code sees the same set.
  Streamlit's own `developing-with-streamlit` skill ships inside the installed package; link it
  locally with
  `ln -s ../../.venv/lib/python3.12/site-packages/streamlit/.agents/skills/developing-with-streamlit .agents/skills/`
  and `ln -s ../../.agents/skills/developing-with-streamlit .claude/skills/` (both links are
  gitignored).
- **Subagents:** `docker-tester` (`.claude/agents/docker-tester.md`, Codex:
  `.codex/agents/docker-tester.toml`, same instructions) builds the image, checks its contents,
  smoke-tests the pipeline and boots the app. Use it to verify Docker changes.
- **MCP:** `.mcp.json` registers the Playwright MCP server for checking the UI in a browser.
- **Plugins:** `.claude/settings.json` enables `impeccable` (design review against
  `PRODUCT.md`/`DESIGN.md`) and `commit-commands`; `.codex/config.toml` enables `python-skills`
  from the `fcakyon/claude-codex-settings` marketplace.
- **Specs and plans:** design specs live in `docs/agents/specs/` and implementation plans in
  `docs/agents/plans/`, named `YYYY-MM-DD-<topic>.md`. Commit them once the work lands.
- Personal settings stay out of git: `.claude/settings.local.json`, `CLAUDE.local.md`, and the
  owner's to-do ledger `STEPS-FOR-OWNER.md`.
