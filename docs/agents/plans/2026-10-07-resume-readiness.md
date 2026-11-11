# Resume Readiness (Tier 1 + Tier 2) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the public GitHub repo hold up to a hiring reviewer: honest, skimmable storefront (Tier 1) and clean, conventionally packaged code (Tier 2), with no behavior change to the app.

**Architecture:** Tier 1 touches only docs, tests, config, and CI. Tier 2 renames the `src/` import root into a real installable package `face_analyzer` (src-layout: `src/face_analyzer/...`), removes the test-aware `_dispatch` shim, makes `analyze_frame` take an `AnalysisConfig`, and splits `app.py` into `ui/` modules. A golden characterization test lands *before* the Tier 2 refactors and must stay green through all of them.

**Tech Stack:** Python 3.11 (Docker) / 3.12 (local `.venv`), Streamlit 1.65, OpenCV, pytest, ruff (via `uvx ruff` locally, pip in CI), GitHub Actions.

**Spec:** The two review reports + scoping in the session of 2026-10-07 (Tier 1 = storefront, Tier 2 = engineering credibility; Tier 3 — public-dataset eval, weights off LFS, HF Spaces demo — is a *separate later plan*). User records their own demo GIF; this plan only leaves a placeholder.

## Global Constraints

- Work on branch `chore/resume-readiness` off `master`. Commit after every task (more often is fine); short imperative subjects with `feat:`/`fix:`/`chore:`/`docs:`/`refactor:`/`test:`/`ci:` prefixes; **no attribution trailers**. Stage files explicitly — never `git add -A`.
- **No behavior change** to the app's predictions or UI in any task. The golden test (Task 7) and full suite are the proof.
- **CI must never fetch LFS** (`actions/checkout` with `lfs: false`, the default). 3.4 GB of weights would exhaust the GitHub LFS bandwidth quota. Any test needing a real model file must skip cleanly when that file is absent or an LFS pointer.
- Do not touch vendored code in `src/nets/` beyond import-path changes forced by the package move.
- Full suite command: `.venv/bin/python -m pytest -q`. Baseline: 199 passed, 66 subtests.
- Ruff: `uvx ruff check .` locally; config lives in `pyproject.toml`.
- New Python code follows CLAUDE.md: PEP 257 one-line docstrings, `#` comments only for WHY.
- Docker changes are verified with the `docker-tester` subagent, never by inspection.
- `docs/superpowers/` (including this plan) stays on disk but is untracked from Task 1 on.

## Review Focus

1. **Fresh clone without LFS** (what CI and most cloners see): `pytest` must pass/skip, never error. Pinned by Task 5's no-LFS clone check.
2. **`streamlit run` entry after the package move**: the app must boot both natively and in Docker with model paths still resolving to repo-root `models/`. Pinned by Task 8's `AppTest` smoke test + `BASE_DIR` assertion + docker-tester.
3. **Live webcam callback** (`_video_frame_callback`, frame-skip path swapping in `_NO_MODELS`) after the `analyze_frame` signature change and `app.py` split: no test drives webrtc. Pinned by Task 10's unit test calling the extracted callback builder with a fake frame.
4. **Loop-variable closures (ruff B023, 77 hits)**: fixing them changes binding semantics; each fix must bind the current-iteration value. Pinned by Task 3 running the golden test after the fix.
5. **Test patch targets after `_dispatch` removal**: tests that silently stop patching would hit real models and pass/skip for the wrong reason. Pinned by Task 9 asserting the mocks were called (`assert_called`).

---

## Tier 1 — Storefront

### Task 1: Repo hygiene

**Files:**
- Untrack: `docs/superpowers/` (all 4 tracked files)
- Delete: `models/pose_iter_160000.caffemodel`, `models/pose_deploy_linevec_faster_4_stages.prototxt`
- Move: `models/DEX_AGE_SPEC.md` → `docs/models/dex_age.md`
- Modify: `.git/info/exclude` (local only)

- [ ] **Step 1:** `git switch -c chore/resume-readiness`
- [ ] **Step 2:** Confirm pose files unreferenced: `grep -rn "pose_iter\|pose_deploy" --exclude-dir=.git --exclude-dir=.venv .` → only matches inside `docs/agents/` or none.
- [ ] **Step 3:** `git rm --cached -r docs/superpowers` and append `docs/superpowers/` to `.git/info/exclude` (not `.gitignore` — keep it invisible publicly).
- [ ] **Step 4:** `git rm` the two pose files; `git mv models/DEX_AGE_SPEC.md docs/models/dex_age.md`.
- [ ] **Step 5:** Run the full suite → 199 passed.
- [ ] **Step 6:** Commit: `chore: drop unused OpenPose weights and internal planning docs`

### Task 2: Replace source-grep tests with a real app smoke test

**Files:**
- Delete: `tests/test_body_pose_removed.py`, `tests/test_blendshapes_removed.py`, `tests/test_ui_design.py`, `tests/test_app_presentation.py`, `tests/test_image_editing_ui.py`, `tests/test_face_editor_toggle.py`, `tests/test_landmark_controls.py`, `tests/test_live_capture.py`, `tests/test_face_detector.py`
- Modify: `tests/test_liveness.py` (remove the two source/README-grep tests at :16 and :25; keep the 6 behavioral ones)
- Modify: `src/inference.py:546-548` (remove `_liveness_task` "signature anchor" stub if its only purpose was those grep tests)
- Keep: `test_remote_access_boundary.py`, `test_keras_input_structure.py`, `test_build_and_run.py`, `test_install_and_run.py` (config/behavior checks, not UI copy)
- Create: `tests/test_app_smoke.py`

- [ ] **Step 1:** Before deleting, skim each deleted file and list any assertion that guards *behavior* (not copy/markup). For each such assertion, add an equivalent `AppTest` assertion to `tests/test_app_smoke.py` instead of losing it.
- [ ] **Step 2: Write the smoke test**

```python
from streamlit.testing.v1 import AppTest

APP = "src/app.py"  # Task 8 changes this path


def test_app_boots_without_exception():
    at = AppTest.from_file(APP, default_timeout=60).run()
    assert not at.exception


def test_app_renders_upload_and_live_tabs():
    at = AppTest.from_file(APP, default_timeout=60).run()
    labels = [t.label for t in at.tabs]
    assert any("UPLOAD" in l.upper() for l in labels)
    assert any("LIVE" in l.upper() or "WEBCAM" in l.upper() for l in labels)


def test_confidence_slider_present():
    at = AppTest.from_file(APP, default_timeout=60).run()
    assert len(at.slider) >= 1
```

Adjust the tab label substrings to the real labels in `src/app.py` (~line 1289). Verify against Context7 `/streamlit/docs` if an `AppTest` attribute behaves unexpectedly.

- [ ] **Step 3:** Run `.venv/bin/python -m pytest tests/test_app_smoke.py -v` → PASS. If AppTest can't execute the script because of `import inference` path resolution, add `tests/conftest.py` inserting `src/` on `sys.path` *for now* (Task 8 removes it).
- [ ] **Step 4:** Delete the files listed above; trim `test_liveness.py`; remove the `_liveness_task` stub if now unused (`grep -rn _liveness_task`).
- [ ] **Step 5:** Full suite → all pass (count drops; record new count).
- [ ] **Step 6:** Commit: `test: replace source-text UI assertions with AppTest smoke tests`

### Task 3: Ruff config and lint-clean codebase

**Files:**
- Create: `pyproject.toml` (ruff section only in this task)
- Modify: `requirements-dev.txt` (add `ruff==0.16.10`)
- Modify: `src/core/__init__.py`, `src/core/constants.py`, facade modules with re-exports, every file with B023/E741/F401 hits

`pyproject.toml` (initial):

```toml
[tool.ruff]
target-version = "py311"
extend-exclude = ["src/nets"]

[tool.ruff.lint]
select = ["E4", "E7", "E9", "F", "I", "B", "UP"]
```

- [ ] **Step 1:** `uvx ruff check . --statistics` → record baseline counts.
- [ ] **Step 2:** `uvx ruff check . --fix` (safe fixes only — no `--unsafe-fixes`); run full suite → pass.
- [ ] **Step 3:** F405/F403: replace `from .constants import *` in `src/core/__init__.py` with explicit imports of the names actually used by importers of `core` (find them with `uvx ruff check . --select F405 --output-format concise`).
- [ ] **Step 4:** F401 in facade modules (`src/inference.py`, `src/fusion/__init__.py`, etc.): declare an explicit `__all__` listing the re-exported public names rather than `noqa`. Remove genuinely unused imports elsewhere.
- [ ] **Step 5:** B023: for each closure capturing a loop variable, bind the current value via a default argument (`lambda x, _v=v: ...`) or pass it explicitly. Do not change any closure that is called synchronously inside the same iteration *unless* ruff flags it — then still bind explicitly (cheap, and makes intent obvious).
- [ ] **Step 6:** E741: rename ambiguous `l`/`O`/`I` variables.
- [ ] **Step 7:** `uvx ruff check .` → `All checks passed!`; `uvx ruff format --check .` is **not** required (formatting churn out of scope).
- [ ] **Step 8:** Full suite → pass.
- [ ] **Step 9:** Commit: `chore: add ruff config and fix lint findings` (split into two commits if the B023 fixes are large: `fix: bind loop variables in closures`).

### Task 4: Pin dependencies

**Files:**
- Modify: `requirements.txt`, `requirements-dev.txt`, `Dockerfile` (pip lines :89, 101, 107, 114, 126, 134, 144, 161)

- [ ] **Step 1:** Pin `requirements.txt` to the versions installed in `.venv`, exact: `streamlit==1.65.0`, `opencv-python-headless==4.14.0.94`, `numpy==2.5.3`, `pillow==12.3.0`, `streamlit-webrtc==0.78.1`, `streamlit-cropper==0.3.1`, `av==17.1.0`, `PyWavelets==1.10.0`. Pin `pytest==9.1.1` in dev.
- [ ] **Step 2:** For the optional heavy deps installed by Dockerfile `RUN pip install` lines (torch, torchvision, tensorflow, tf-keras, onnxruntime, mediapipe, scipy, opencv-contrib-python-headless): dispatch `docker-tester` to build with every ARG at its full list and report `pip freeze` for those packages from the running container; pin each Dockerfile install to those exact versions. Keep the CPU torch index URL.
- [ ] **Step 3:** Confirm `opencv-contrib-python-headless` pin equals the `opencv-python-headless` pin version (they must match to coexist/replace cleanly).
- [ ] **Step 4:** `docker-tester`: rebuild full-ARG image and default image → both PASS (boot + smoke).
- [ ] **Step 5:** Full suite → pass.
- [ ] **Step 6:** Commit: `chore: pin runtime and Docker dependency versions`

### Task 5: GitHub Actions CI

**Files:**
- Create: `.github/workflows/ci.yml`

Workflow: on `push` and `pull_request` to `master`; one job, `ubuntu-latest`, matrix `python-version: ["3.11", "3.12"]`; steps: `actions/checkout@v4` (no `lfs`), `actions/setup-python@v5` with pip cache, `pip install -r requirements-dev.txt`, `ruff check .`, `python -m pytest -q`.

- [ ] **Step 1:** Simulate CI locally — clone without LFS into a temp dir and run the suite there:

```bash
rm -rf /tmp/mfa-nolfs && GIT_LFS_SKIP_SMUDGE=1 git clone -q -b chore/resume-readiness . /tmp/mfa-nolfs
cd /tmp/mfa-nolfs && python3.11 -m venv .v && .v/bin/pip install -q -r requirements-dev.txt && .v/bin/python -m pytest -q
```

Expected: no failures/errors. Any test that loads a real model file and fails on an LFS pointer gets a skip guard via a shared helper `tests/_models.py::require_model(path: Path) -> None` (calls `pytest.skip` if missing or the first bytes are `b"version https://git-lfs"`).
- [ ] **Step 2:** Write `ci.yml`; validate syntax with `uvx actionlint` if available (else skip and note it).
- [ ] **Step 3:** Commit: `ci: run ruff and pytest on push and PR`
- [ ] **Step 4:** After the branch is pushed (end of Tier 1), confirm the run is green with `gh run list --branch chore/resume-readiness`.

### Task 6: README overhaul, licenses, responsible use, repo metadata

**Files:**
- Rewrite: `README.md` (target ≤ ~170 lines)
- Create: `docs/models.md` (all current per-model `###` sections from README lines 36-381, moved verbatim then lightly edited), `docs/setup.md` (Local Setup, Guided run scripts, Docker Web App incl. the full ARG table and remote-access notes, README lines 458-616), `docs/benchmark.md` (methodology + full tables + age-fusion rejection narrative, from README "Combined answers" 122-166 and Performance 382-388)
- Create: `LICENSE` (MIT, `Copyright (c) 2026 Kaitlyn Bassford`), `MODEL_LICENSES.md`
- Create: `docs/media/.gitkeep`
- Modify (local, untracked): `CLAUDE.md` — every "README is the source of truth / README's ARG table" pointer now points at `docs/models.md` / `docs/setup.md`

**README structure (in order):**
1. Title + one-line pitch: *Real-time multi-model face analysis: ~15 per-face and whole-frame features, pluggable detectors, and benchmarked fusion across interchangeable backends.* + badges (CI badge from Task 5, Python, License).
2. Demo media placeholder:
   ```markdown
   <!-- DEMO: record 5-10s of LIVE mode (age/gender/emotion/landmarks on, change expression once),
        export ≤5 MB, ~800px wide → docs/media/demo.gif; full-UI screenshot → docs/media/screenshot.png -->
   ```
3. Highlights (5-6 bullets): pluggable detector layer (`src/detectors/` base + factory: SSD, YOLO, SCRFD, RetinaFace); fusion with label-taxonomy canonicalization; age fusion rejected on evidence; threaded per-face inference + prediction cache + live latency/FPS metrics; build-time per-feature model selection in Docker with graceful runtime degradation.
4. Architecture: a Mermaid `flowchart LR` — Frame → (Colorization) → Detector factory → per-face crop → attribute backends (parallel) → fusion → overlay/UI; whole-frame branch (hands) alongside.
5. Results: compact table (see Step 2 for numbers) + 3-line honest caveat + link to `docs/benchmark.md`.
6. Quick start: 4-5 commands each for native and Docker (link `docs/setup.md` for ARGs). State git-lfs is required and that the full weight set is ~3.4 GB.
7. Feature list: one table, `Feature | Backends | Notes`, one row per feature; mark 3D Reconstruction **"no working default weights"** explicitly.
8. Responsible use (see Step 3).
9. Licensing: code MIT; model weights under their own licenses → `MODEL_LICENSES.md`.

- [ ] **Step 1:** Move sections to `docs/models.md`, `docs/setup.md`, `docs/benchmark.md` with `git mv`-free cut/paste; fix the stale "weights live in `src/inference.py`" reference → `src/core/constants.py`.
- [ ] **Step 2: Benchmark honesty.** Resolve the race row contradiction (README:147, best `fairface` 93.3% vs weakest `deepface` 94.7%) by re-scoring: `.venv/bin/python tools/score_fusion.py` against local `tmp/predictions.json` (exists locally, untracked). Use whichever numbers the tool prints; if the tool can't run, label the row's columns correctly by the existing numbers (`deepface` 94.7% is then the *best* single). Rewrite the "Weights are measurements, not taste" paragraph to say: weights are **hand-set**, ordered by each model's per-model accuracy on the 75-face set; they were not fitted, and they were chosen on the same set they're scored on (no held-out split — Tier 3 adds a public held-out evaluation). Add to `docs/benchmark.md`: emotion ground truth covers 42 of 75 faces and 38 of those are `happy`; age counts correct on range overlap with hand-estimated ranges; 75 faces from 12 images, 51 F / 24 M.
- [ ] **Step 3: Responsible use section** (README, ~8 lines): predicted race/gender/age are statistical guesses of *apparent* attributes, not identity; categories are coarse and culturally contingent; training sets (FairFace, AffectNet, IMDB-WIKI, etc.) carry known demographic biases; not for decisions about individuals (hiring, policing, access, surveillance); recognition/identity search should only be run on people who consented.
- [ ] **Step 4: `MODEL_LICENSES.md`** — table `Feature | Model key | File(s) | Upstream source (URL) | License | Redistribution`. Populate from the inline notes in README lines 20, 23, 49, 76, 87, 100, 120, 225-232, 242-250, 284, 292, 332, 380 and `src/nets/mivolo/LICENSE_MIVOLO`. Where a license is unknown or non-commercial (SCRFD, DEX, DAN, HSEmotion, VGG-Face-derived `deepface_*.h5`, yolov8n_face, glasses detector, face_reaging CC BY-NC-SA, caffe age/gender, opencv SSD), say so plainly; don't guess — "not stated upstream" is a valid entry. Header note: code is MIT; weights are third-party, included for research/demo use; moving restricted weights to download-at-build is planned.
- [ ] **Step 5:** Verify every relative link in README/docs resolves: `grep -oE '\]\(([^)#]+)' README.md docs/*.md MODEL_LICENSES.md` → each path exists.
- [ ] **Step 6:** `test_remote_access_boundary.py` greps README for remote-access text — update it to read `docs/setup.md`. Full suite → pass.
- [ ] **Step 7:** Commit (two commits): `docs: restructure README with architecture, results and responsible use` and `docs: add LICENSE and model license inventory`.
- [ ] **Step 8:** Push branch; open PR to `master` titled `Resume readiness: storefront (Tier 1)`; confirm CI green; merge after user review. Then set repo metadata:

```bash
gh repo edit --description "Real-time multi-model face analysis in Streamlit: pluggable detectors, interchangeable backends, benchmarked fusion" \
  --add-topic computer-vision --add-topic face-analysis --add-topic streamlit --add-topic opencv \
  --add-topic pytorch --add-topic onnx --add-topic docker --add-topic model-ensemble
```

---

## Tier 2 — Engineering credibility

### Task 7: Golden characterization test (safety net for Tasks 8-11)

**Files:**
- Create: `tests/fixtures/crew_portrait.jpg` (+ `tests/fixtures/SOURCE.md`), `tests/fixtures/golden_analysis.json`, `tests/test_pipeline_golden.py`
- Uses: `tests/_models.py::require_model` (Task 5)

- [ ] **Step 1:** Fetch a **US-government public-domain** multi-face photo (e.g. a NASA ISS expedition crew official portrait from images.nasa.gov) into a fresh empty temp dir, downscale to ≤1024px wide JPEG, copy into `tests/fixtures/`. `SOURCE.md` records URL, title, and "Public domain (NASA)". Confirm with the SSD detector that ≥3 faces are detected at `conf_threshold=0.5`.
- [ ] **Step 2: Write the test**

```python
def test_analyze_frame_matches_golden():
    for p in REQUIRED_MODELS: require_model(p)   # SSD .pb/.pbtxt, caffe age/gender, fairface/ferplus/hsemotion .onnx — whatever loads via cv2.dnn without torch/TF
    models = load_models()
    frame = cv2.imread(str(FIXTURE))
    _, faces, *_ = analyze_frame(models, frame, <config: ssd detector, every active_* set = the loaded cv2.dnn-only model keys, everything else empty>)
    assert normalize(faces) == json.loads(GOLDEN.read_text())
```

`normalize(faces) -> list[dict]`: keep box coords and every per-feature label/value string, round floats to 3 dp, drop images/arrays and timing fields; sort faces by box `(x, y)`. Regenerate the golden only when `UPDATE_GOLDEN=1` is set (write file, then `pytest.skip("golden updated")`).
- [ ] **Step 3:** `UPDATE_GOLDEN=1 .venv/bin/python -m pytest tests/test_pipeline_golden.py`, then run without the env var → PASS. Inspect the JSON: it must contain non-empty age, gender, and emotion entries for each face (otherwise models didn't actually load — fix `REQUIRED_MODELS`).
- [ ] **Step 4:** In the no-LFS clone (Task 5 Step 1 recipe) the test SKIPs.
- [ ] **Step 5:** Commit: `test: add golden characterization test for analyze_frame`

> **Tasks 8-11 must not modify `golden_analysis.json`.** If the golden test fails, the refactor changed behavior — fix the refactor.

### Task 8: Make `face_analyzer` an installable package

**Files:**
- Move: `src/{__init__.py,inference.py,app.py,attributes,core,detectors,fusion,gallery,nets,pipeline}` → `src/face_analyzer/...` (`git mv`)
- Modify: `pyproject.toml` (add `[build-system]`, `[project]`), all 21 try/except-import modules, every `from src.` import in `tests/` and `tools/`, `src/face_analyzer/core/constants.py:10`, `Dockerfile` (:164 COPY, :208 CMD, plus an install step), `install-and-run.sh:511`, `build-and-run.sh` (if it references `src/app.py`), `docs/setup.md`, README quick start, `tests/test_core_types.py:143`, `tests/test_app_smoke.py` path, `.github/workflows/ci.yml`
- Delete: `tests/conftest.py` sys.path hack (if Task 2 added it); `sys.path.insert` lines in `tests/test_hair_color_accuracy.py:10`, `tools/{benchmark:26,dump_predictions:16,annotate_faces:14,score_fusion:15}`

**Interfaces — Produces:** import root `face_analyzer` (e.g. `from face_analyzer.pipeline.analyzer import analyze_frame`); app entry `src/face_analyzer/app.py`; `face_analyzer.core.constants.BASE_DIR` == repo root.

`pyproject.toml` additions: setuptools build backend; `[project] name = "face-analyzer"`, `version = "1.0.0"`, `requires-python = ">=3.11"`, `dependencies` read dynamically from `requirements.txt` (`[tool.setuptools.dynamic]`); `[tool.setuptools.packages.find] where = ["src"]`; `[tool.pytest.ini_options] testpaths = ["tests"]`. Keep the ruff section.

- [ ] **Step 1: Failing test** — replace `tests/test_core_types.py:143` (the "imports with only `src/` on path" test) with:

```python
def test_base_dir_is_repo_root():
    from face_analyzer.core.constants import BASE_DIR

    assert (BASE_DIR / "models").is_dir() and (BASE_DIR / "pyproject.toml").is_file()
```

Run → FAIL (`ModuleNotFoundError: face_analyzer`).
- [ ] **Step 2:** `git mv` the tree. In every module, replace the `try: from src.x import … except ImportError: from x import …` blocks with a single **relative** import inside the package (`from ..core import …`); `src/nets` keeps its relative imports. `app.py` uses absolute `from face_analyzer import inference` (Streamlit runs it as a script, so relative imports won't work there). `BASE_DIR = Path(__file__).resolve().parents[3]`.
- [ ] **Step 3:** `sed`-rewrite `from src.` → `from face_analyzer.` and `import src.` → `import face_analyzer.` in `tests/` and `tools/`; also string patch targets like `"src.pipeline.analyzer.detect_faces"`. Remove the listed `sys.path.insert` lines (`tools/` keep `ROOT` for data paths only).
- [ ] **Step 4:** `.venv/bin/pip install -e .`; add `-e .` as the last line of `requirements-dev.txt`. Run the full suite → all pass incl. golden + new BASE_DIR test. `grep -rn "except ImportError" src/face_analyzer --include=*.py | grep -v nets` → only genuine optional-dependency guards (torch/tensorflow/mediapipe etc.), none for intra-package imports.
- [ ] **Step 5:** Native boot: `.venv/bin/streamlit run src/face_analyzer/app.py --server.headless true` → reachable on :8501 (curl `/_stcore/health` → `ok`), then stop it.
- [ ] **Step 6:** Dockerfile: after `COPY src/ src/`, also `COPY pyproject.toml requirements.txt ./` (before it) and `RUN pip install --no-deps .`; CMD → `src/face_analyzer/app.py`. Update `install-and-run.sh:511` (add `pip install -e .` to its install step), `build-and-run.sh`, `docs/setup.md`, README. `tests/test_build_and_run.py` / `test_install_and_run.py` → pass.
- [ ] **Step 7:** `docker-tester`: default build + one multi-model build → PASS. CI no-LFS clone recipe → pass/skip.
- [ ] **Step 8:** Commit: `refactor: package source as installable face_analyzer`

### Task 9: Remove the test-aware `_dispatch` shim

**Files:**
- Modify: `src/face_analyzer/pipeline/analyzer.py` (delete `_dispatch` :178-185 and its 14 call sites at :191, 235, 346-349, 373, 383, 386-391)
- Create: `src/face_analyzer/pipeline/landmarks.py`
- Modify: `src/face_analyzer/inference.py` (becomes a pure facade: re-exports + `load_models`; delete its `analyze_frame` wrapper :494-576 and re-export the pipeline one)
- Modify: `tests/test_expression_accuracy.py:18-22`, `tests/test_dex_preprocessing.py:64-65`, `tests/test_fairface_alignment.py:90-91`

**Interfaces — Produces:** `face_analyzer.pipeline.landmarks._detect_face_landmarker` and `.detect_hand_landmarks_mediapipe` (moved verbatim from `inference.py:471` / `:480`); `analyzer.py` imports every formerly-dispatched name directly at module top, so tests patch `face_analyzer.pipeline.analyzer.<name>`.

- [ ] **Step 1:** Update the three tests to `patch("face_analyzer.pipeline.analyzer.<name>")` and add `mock.assert_called()` for each patched function the test expects to be hit. Run them → FAIL (patches miss because analyzer still dispatches via `inference`), confirming the assertions bite.
- [ ] **Step 2:** Move the two landmark functions into `pipeline/landmarks.py`; replace every `_dispatch("x", x)` with `x`; delete `_dispatch` and the `unittest.mock`/`sys` imports. `inference.py` re-exports `analyze_frame` from `pipeline` and the landmark functions from `pipeline.landmarks` (listed in `__all__`).
- [ ] **Step 3:** `grep -rn "unittest" src/` → no matches. Full suite → pass (golden unchanged).
- [ ] **Step 4:** Commit: `refactor: drop test-aware dispatch shim in favor of direct imports`

### Task 10: `analyze_frame(models, frame, config)`

**Files:**
- Modify: `src/face_analyzer/pipeline/analyzer.py:307` (signature + body split), `src/face_analyzer/pipeline/config.py`
- Modify callers: `app.py:1028`, `app.py:1368` (`_video_frame_callback`), `tools/benchmark.py:169,291`, `tests/test_expression_accuracy.py:23`, `tests/test_dex_preprocessing.py:68`, `tests/test_fairface_alignment.py:92`, `tests/test_pipeline_modular.py:181,209`, `tests/test_pipeline_golden.py`
- Create: `tests/test_live_callback.py`

**Interfaces — Produces:**
- `analyze_frame(models: Models, frame: np.ndarray, config: AnalysisConfig) -> tuple[np.ndarray, list[dict], bool, bool]` (return type unchanged)
- `AnalysisConfig` unchanged fields/defaults; `to_dict()` kept only if something still uses it (else delete).
- `analyze_frame_with_config` deleted.
- Body split into private stage helpers in `analyzer.py` (or `pipeline/stages.py` if `analyzer.py` would stay > 500 lines): `_prepare_frame` (adjustments + colorization), `_detect(models, frame, config) -> list[box]`, `_run_whole_frame_features`, `_analyze_face(models, frame, box, config, ...) -> dict`, `_annotate`. `analyze_frame` itself ≤ ~60 lines, orchestrating them. Exact helper parameters are the implementer's choice; each helper ≤ ~120 lines.
- `app.py`'s live callback logic exposed as `make_video_frame_callback(models_provider, config_provider) -> Callable[[av.VideoFrame], av.VideoFrame]` (in `app.py` now, moves with the live tab in Task 11) so it's testable without webrtc.

- [ ] **Step 1: Failing tests** — in `tests/test_pipeline_modular.py`, assert `inspect.signature(analyze_frame).parameters` keys == `["models", "frame", "config"]`; in `tests/test_live_callback.py`, build a callback with a fake models provider returning `_NO_MODELS`-style empty `Models`, feed `av.VideoFrame.from_ndarray(np.zeros((240, 320, 3), np.uint8), format="bgr24")`, assert it returns an `av.VideoFrame` of the same size and raises nothing — once for a normal frame and once on the frame-skip path. Run → FAIL.
- [ ] **Step 2:** Change the signature; convert all callers to build an `AnalysisConfig(...)` with keyword fields; extract `make_video_frame_callback`.
- [ ] **Step 3:** Run full suite → signature + callback tests pass, golden unchanged.
- [ ] **Step 4:** Commit: `refactor: analyze_frame takes an AnalysisConfig`
- [ ] **Step 5:** Extract the stage helpers (pure moves; no logic edits). Full suite → golden unchanged. `wc -l` on `analyzer.py` and any new stage module → report.
- [ ] **Step 6:** Commit: `refactor: split analyze_frame into pipeline stage helpers`

### Task 11: Split `app.py` into `ui/` modules

**Files:**
- Create: `src/face_analyzer/ui/__init__.py`, `ui/theme.py` + `ui/theme.css`, `ui/sidebar.py`, `ui/results.py`, `ui/live.py`
- Modify: `src/face_analyzer/app.py` (target ≤ ~200 lines: page config, theme apply, model load, sidebar → tabs wiring)

**Interfaces — Produces** (move code verbatim; signatures are whatever is needed to pass the state that was module-global, explicitly):
- `ui/theme.py`: theme maps (app.py:37-56) + `apply_theme(name: str) -> None` that reads `theme.css` (the ~590-line inline CSS at app.py:66-655, with theme values substituted the same way as today).
- `ui/sidebar.py`: `MODEL_DISPLAY_NAMES`, `_display_model_name`, `_model_checkboxes`, `_landmark_enable_button`, `_reset_adjustments`, `_adjustment_sliders`, and `render_sidebar(models) -> SidebarState` (a dataclass holding every value the sections at app.py:774-900 currently produce). `SidebarState.to_config(...) -> AnalysisConfig`.
- `ui/results.py`: `process_and_display` and its helpers (`_model_result_order`, `_target_card_html`, `_one_line_summary`, `_hoverable_face_image`, `_show_fullscreen_image`, `_render_bounded_image`, `_render_photo_editor`).
- `ui/live.py`: live globals/locks (app.py:23-27), `_get_face_tracker`, `_get_liveness_tracker`, `_get_voice_fusion`, `make_video_frame_callback` (from Task 10), `render_live_tab(...)`.

- [ ] **Step 1:** Extend `tests/test_app_smoke.py`: assert the sidebar renders at least one checkbox per loaded-model feature (`len(at.sidebar.checkbox) >= 1`), and that changing the confidence slider and re-running raises no exception (`at.slider[0].set_value(0.7).run(); assert not at.exception`). Run → PASS on current code (characterization).
- [ ] **Step 2:** Extract in this order, running `pytest tests/test_app_smoke.py tests/test_live_callback.py -q` after each: theme → results → sidebar → live. Commit after each extraction (`refactor(ui): extract theme`, `... results view`, `... sidebar`, `... live tab`).
- [ ] **Step 3:** `wc -l src/face_analyzer/app.py` ≤ ~200; full suite pass; `uvx ruff check .` clean.
- [ ] **Step 4:** Manual check: native `streamlit run src/face_analyzer/app.py`, upload `tests/fixtures/crew_portrait.jpg`, confirm faces annotated and sidebar toggles work; note anything visually off. Use the `webapp-testing` skill (Playwright screenshot) if available rather than eyeballing.

### Task 12: Tier 2 wrap-up

- [ ] **Step 1:** Full suite, `uvx ruff check .`, no-LFS clone recipe, `docker-tester` default + full-ARG builds → all PASS. Record test count.
- [ ] **Step 2:** Update README architecture section / Mermaid diagram and `docs/setup.md` for the new package layout and `ui/` modules; update local `CLAUDE.md` Architecture section (paths `src/face_analyzer/...`, `analyze_frame(models, frame, config)`, no `_dispatch`). Commit: `docs: update architecture for package layout`.
- [ ] **Step 3:** Push; PR `Resume readiness: package layout and pipeline refactor (Tier 2)`; CI green; merge after user review.
- [ ] **Step 4:** Hand off to the user: record the demo GIF/screenshot (instructions in the README placeholder), then the resume bullet rewrite, then a separate Tier 3 plan.

---
## Status (2026-10-07, end of session)
Tier 1 merged (PR #1, fd62d08). Tier 2 merged (PR #2, 745b205). CI green on 3.11/3.12.

## Tier 3 backlog (carried from reviews)
- DONE (PR #5, 533ca81): held-out FairFace eval (N=2000, test half 1002). Findings: race fusion 63.3% < fairface alone 76.5% (deepface overconfident); gender fusion == MiVOLO; SSD misses tight 0.25 crops.
- DONE (PR #6): option A chosen; race headline names its most reliable model (select_race), held-out race 63.3% -> 76.5%. .venv-eval (3.9G) + data/ (291M) kept for re-scoring.
- DONE (PR #7, 5e4786a): weights off git-lfs. models/manifest.json + tools/fetch_models.py; 15 permissive files on HF kaitlynbassford/face-analyzer-weights (pinned rev 4c7e361), 15 from upstream, 3 bring-your-own (dan, deep3d, BFM). Docker downloads at build time. History kept.
- DONE (PR #8): learned stacker tested, not adopted (no attribute beat shipped beyond noise); gender headline -> best model (mivolo). Emotion only fused attribute.
- DONE (PR #9, 30cc214): Kaggle ConvNeXt-Tiny age model trained (~2.9 GPU-h); not adopted (FairFace -2.3pp ns, UTKFace -8.7pp). UTKFace OOD eval added: MiVOLO 67.5%, MAE 3.7y. Kaggle kernels face-age-prep/-crops/-convnext-train still on account.
- TODO: live HF Spaces demo with permissive models only.
- DONE (PR #3, 3fd3ff0): dead code removed, inference.__all__ trimmed to 76 public names.
- DONE (PR #4): _format_race_label deduplicated (fusion/ensembles.py is the single copy).
- Full-ARG Docker build re-verification (skipped this session under the CPU limit; only a light all-empty-ARG build was run after the package move).
- Demo GIF + screenshot (user records) -> docs/media/.
