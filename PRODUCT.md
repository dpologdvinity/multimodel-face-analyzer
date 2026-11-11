# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Primary: visitors to the public demo (https://multimodal-face-analyzer.streamlit.app/) such as
recruiters, hiring managers and curious people. They open the link, upload one photo, and want
an instant, clear, enjoyable result within one or two minutes.

Secondary: someone running the full app locally, who toggles many models, compares backends,
and uses the live webcam tab, galleries, identity search and enrollment. These features must
keep working but are not the design's first audience.

## Product Purpose

Detect every face in a photo or webcam frame and report per-face estimates (age, gender, race,
emotion, eye color, and more locally) from interchangeable model backends. Success for a demo
visitor: they upload a photo, see each face boxed and numbered, and read what each model said
about it without confusion.

## Positioning

Every answer names the model that produced it, and the choice of which model answers (or
whether answers are fused) was decided by a held-out evaluation with bootstrap confidence
intervals, not by instinct. The readouts carry that evidence story.

## Operating Context

- Streamlit app (`src/face_analyzer/app.py`); UI in `src/face_analyzer/ui/`, styling in
  `ui/theme.css` injected as CSS over native Streamlit widgets. No `.streamlit/config.toml`, so
  Streamlit's base light/dark follows the visitor's system and the CSS restates widgets.
- Public demo runs on Streamlit Community Cloud in demo mode (`FACE_ANALYZER_DEMO=1`): CPU only,
  reduced model set, upload tab plus webcam snapshot; saving, galleries, identity search and live
  webcam streaming are hidden.
- Face boxes are drawn into the annotated image with the active theme's colors
  (`box_style(theme)` feeding `AnalysisConfig`).

## Capabilities and Constraints

- Tabs: image upload (multiple images) and webcam; sidebar with theme picker, model selection
  per feature, confidence threshold, aggregate summary; per-image results (counts, annotated
  image with hoverable boxes, JSON/CSV download) and per-face cards with crop, readouts,
  "Open image" and "Edit face".
- Theme tokens are plain `#rrggbb` hex in `theme.css`, parsed by `theme_tokens()`;
  `tests/test_theme.py` enforces WCAG AA contrast. Stale theme names fall back through
  `resolve_theme()`.
- Must stay within Streamlit's DOM: styling through CSS and `st.markdown` HTML, no custom
  component build step.

## Brand Commitments

- Name: "Multimodal Face Analyzer".
- Each readout names its backend (for example `fairface`, `ferplus`); keep this visible.
- Keep the demo's responsible-use notice (results are appearance estimates with known
  demographic bias, images never stored) visible, though it need not dominate.

## Evidence on Hand

- Held-out FairFace results (1,002 test faces): gender 96.7%, race 76.5%, age bucket 62.3%
  (`docs/eval/heldout_fairface.md`); UTKFace age check (`docs/eval/age_model.md`).
- Sample photo: `tests/fixtures/crew_portrait.jpg` (NASA, public domain).
- No testimonials, users, or usage numbers exist; do not invent them.

## Product Principles

1. The result is the hero: faces, boxes and readouts get the space and the attention.
2. Every estimate shows which model made it.
3. Instant clarity for a first-time visitor beats density for an expert.
4. Honest about limits: estimates, not identity; bias acknowledged.

## Accessibility & Inclusion

WCAG AA contrast for every theme (enforced by `tests/test_theme.py`).
