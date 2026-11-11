# Architecture

How the face analyzer is put together. The data-flow diagram is in the
[README](README.md#architecture); per-feature models and preprocessing are in
[docs/models.md](docs/models.md); setup, Docker build ARGs and optional dependencies are in
[docs/setup.md](docs/setup.md). All paths below are under `src/face_analyzer/` unless noted.

## Modules

| Module | Responsibility |
| --- | --- |
| `app.py` | Thin Streamlit entry point. Calls `new_live_session()` on every script run and wires the `ui/` modules together. |
| `ui/` | `theme.py` (+ `theme.css`, package data), `sidebar.py` (`SidebarState`), `adjustments.py` (image sliders shared by the batch and per-face views), `results.py` (per-image results, `process_and_display`), `live.py` (Live webcam tab), `share_card.py` (PNG share cards). |
| `inference.py` | Facade re-exporting the public names the UI, tools and tests use. |
| `pipeline/` | `loader.py` `load_models()`, `analyzer.py` `analyze_frame(models, frame, config)`, `config.py` `AnalysisConfig`, `stages.py`, `face_tasks.py`, `cache.py` (prediction cache and thread pool), `landmarks.py`, `drawing.py`, `tracker.py`. |
| `core/` | Constants (`BASE_DIR`, `MODEL_DIR`, model paths) and the `Models` container in `types.py`. |
| `detectors/` | Face detectors (SSD, YOLOv8-Face, SCRFD, RetinaFace) and `factory.py` `resolve_face_detector()`. |
| `attributes/`, `fusion/`, `gallery/`, `liveness.py` | Per-face attribute backends, combining their answers, the face gallery / identity search, liveness. |
| `model_selection.py`, `demo.py` | Which backends may load (installer selection, demo allowlist) and demo-mode policy. |
| `nets/` | Vendored third-party architectures (upstream licenses, excluded from lint). |

`tools/` holds the weight fetcher, benchmark and evaluation scripts; `streamlit_app.py` at the
repo root is the Streamlit Community Cloud entry point for the public demo.

## Design patterns

- **Multiple backends per feature run side by side.** `Models` holds a `dict[str, net]` per
  feature; `load_models()` loads whatever weights are present; `analyze_frame()` runs only the
  backends in the `active_*` sets of the passed `AnalysisConfig`. Emotion is fused across
  backends; age, gender and race name their best model (`select_*`). A learned stacker was
  tested and not adopted. Measurements are in [docs/benchmark.md](docs/benchmark.md) and
  [docs/eval/](docs/eval/).
- **Whole-frame vs. per-face features.** Most features run once per detected face.
  Colorization runs in the UI layer (`ui/results.py`, `ui/live.py`) *before* detection, and hand
  landmarks run once per frame alongside the face loop.
- **On-demand actions** (SAVE, SEARCH, 3D RECON, SCAN ALL FACES) call helpers directly from
  `ui/results.py`, outside `analyze_frame()`, gated by a plain availability check.
- **"No working weights shipped" is explicit.** Features whose only known weights are broken,
  gated or unlicensed ship wired-up code with no default weights; `Models.offline_features`
  lists them in the sidebar.
- **Any detector will do.** `load_models()` raises only when no face detector loads;
  `resolve_face_detector()` falls back to SSD, then to any loaded detector.

## Model weights lifecycle

Weights never live in git. `models/manifest.json` records each file's size, sha256, license,
build-arg keys and `source`: `hf` (the project's Hugging Face mirror, pinned to a commit),
`upstream` (original URL, pinned) or `manual` (bring-your-own instructions).
`tools/fetch_models.py` (stdlib only) downloads the selected keys and verifies hashes; the
Dockerfile runs it at build time with the build ARGs, and CI runs it with no keys to fetch only
the required SSD detector. `MODEL_DIR` is `models/` unless `FACE_ANALYZER_MODEL_DIR` is set.
License details are in [MODEL_LICENSES.md](MODEL_LICENSES.md).

## Demo mode

`FACE_ANALYZER_DEMO=1` (or the `streamlit_app.py` entry point) turns the app into a stateless
public demo, described in [docs/deploy.md](docs/deploy.md):

- loads only the `DEMO_MODELS` allowlist (hf-mirrored, no torch/TF; RetinaFace, never SSD)
  through `native_model_selected()`;
- hides SAVE/SEARCH/SCAN/ENROLL, galleries, identity search and Live mode, and the face writers
  (`save_face`, `save_gallery`, `enroll_lbph_face`) raise `PermissionError`;
- caps uploads (JPEG/PNG/WebP under a pixel cap), runs one analysis at a time through the
  `analysis_slot()` semaphore, skips the decode and prediction caches, hides error details and
  shows a model credit footer.

`streamlit_app.py` sets the flag, adds `src/` to `sys.path` (no install, so `BASE_DIR` stays the
repo root), fetches the demo weights once under `st.cache_resource`, then runs `app.py`.

## UI

Layout is input-first: a compact `app-bar` header, a tall centred drop area or camera, then the
annotated photo with a `wrap-summary` strip under it, then one `story-card` per face
(`ui/results.py` `face_story_html()`), coloured by rotating through `POP_COUNT` fills.

- **Themes** (Night default, Day) are each one `body:has(.theme-<name>)` block of `#rrggbb`
  tokens in `ui/theme.css`; `theme_tokens()` parses them and `tests/test_theme.py` enforces WCAG
  AA for text, accent and every card fill. There is no `.streamlit/config.toml`, so Streamlit's
  base follows the visitor's system and the CSS restates native widgets from the tokens. The
  `--box`/`--box-outline` tokens are also drawn into the annotated image via `box_style(theme)`.
- **Share card:** `ui/share_card.py` `render_share_card()` draws a face's story card as a
  1080x1350 PNG with Pillow in the bundled Bricolage Grotesque font (OFL). It downloads only to
  the visitor's own device, so demo mode allows it.
- **Sample photo:** `ui/sample_photo.jpg` (public domain) runs through the same
  `decode_image_bytes` / `process_and_display` path as an upload.

The design system and its rules are in [DESIGN.md](DESIGN.md); the audience and goals in
[PRODUCT.md](PRODUCT.md).
