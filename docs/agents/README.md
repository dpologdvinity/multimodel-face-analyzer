# Specs and plans

Design specs and implementation plans written before larger changes, kept as a record of the
decisions behind them. The workflow: a short spec settles *what* and *why*, a plan breaks it
into small test-first tasks with exact files, commands and commit messages, and the plan is
then executed task by task with the test suite green after each commit.

These are historical documents. Paths, line counts and commands are as of their date (for
example, `src/inference.py` predates the `face_analyzer` package); the current layout is in
[ARCHITECTURE.md](../../ARCHITECTURE.md).

| Date | Spec | Plan | Outcome |
| --- | --- | --- | --- |
| 2026-09-21 | [UI redesign](specs/2026-09-21-ui-redesign-design.md) | [plan](plans/2026-09-21-ui-redesign.md) | First UI foundation; later replaced by the story-card design in [DESIGN.md](../../DESIGN.md). |
| 2026-10-02 | [Architecture modularization](specs/2026-10-02-code-architecture-modularization-design.md) | [plan](plans/2026-10-02-code-architecture-modularization.md) | Split the monolithic `inference.py` into domain packages behind a facade. |
| 2026-10-07 | (scoped from two review reports) | [Resume readiness, Tier 1 + 2](plans/2026-10-07-resume-readiness.md) | Storefront docs and CI, golden test, installable `face_analyzer` package; merged in PRs #1 and #2. |

New specs go in `specs/` and plans in `plans/`, named `YYYY-MM-DD-<topic>.md`.
