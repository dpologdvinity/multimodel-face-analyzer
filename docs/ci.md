# CI and automation

Every workflow lives in [`.github/workflows/`](../.github/workflows/); each file starts with a
comment explaining what it guards and why. This page is the map.

## The merge gate: `CI`

[`ci.yml`](../.github/workflows/ci.yml) runs on every pull request and every push to `master`.
A ruleset on `master` requires its single **CI OK** check, which is green only when every job
is, so pull requests merge (`gh pr merge --auto --squash`) only on a fully green run.

| Job | What it proves |
| --- | --- |
| `lint` | `ruff check` (findings annotated inline on the diff), `ruff format --check`, `typos`, and the basedpyright ratchet (below). |
| `test (3.11)`, `test (3.12)` | The full suite with branch coverage and a coverage floor (`fail_under` in `pyproject.toml`), a test report and a coverage table in the run summary, and a check that the run left every tracked file unchanged. Tests that need optional weights skip, as locally; that includes the golden pipeline test, so `tests/fixtures/golden_analysis.json` is still checked by running the suite with the weights before you push (AGENTS.md). |
| `browser (public demo)` | Installs `requirements.txt` exactly as Streamlit Community Cloud does, serves `streamlit_app.py`, and drives it in Chromium ([`tests/test_browser_smoke.py`](../tests/test_browser_smoke.py)): the Responsible use notice renders, the sample photo yields all six faces, the Day theme applies, and no exception box appears. Night and Day screenshots are kept as the `demo-screenshots` artifact. |
| `audit` | `pip-audit` of `requirements.txt` against the PyPI advisory database. |
| `coverage report` | Comments the coverage of the changed lines on the pull request, and on `master` records the total (on the `python-coverage-comment-action-data` branch) so later comments show the change. |

### The type-check ratchet

`basedpyright` checks `src/`, `tests/`, `tools/` (except the Kaggle training scripts) and
`streamlit_app.py`, configured by `[tool.pyright]` in `pyproject.toml`. Errors that predate the
check are recorded in [`.basedpyright/baseline.json`](../.basedpyright/baseline.json); many come
from optional dependencies (torch, TensorFlow, mediapipe) that CI doesn't install. A new error
fails `lint`. Fixing a baselined error also fails it until the smaller baseline is committed, so
the count only goes down.

Results depend on what is installed, so run it through
[`tools/typecheck.sh`](../tools/typecheck.sh), which keeps a `.venv-types` with exactly
`requirements-dev.txt`, as CI has. In the main `.venv` the optional packages change the errors
and basedpyright rewrites the baseline.

```bash
tools/typecheck.sh                   # what CI runs; must report no new errors
tools/typecheck.sh --writebaseline   # after fixing errors: shrink the baseline, then commit it
```

## Path-triggered checks

| Workflow | Runs when | What it does |
| --- | --- | --- |
| [Docker](../.github/workflows/docker.yml) | The Dockerfile, requirements, `models/`, `tools/fetch_models.py` or `src/` change; weekly | hadolint, then builds the `minimal` (SSD only) and `onnx` (the demo's model set) images. In each one it checks that only the requested heavy runtimes are installed, the pipeline finds all six faces in the sample photo, and the app answers its health check. Trivy scans the `onnx` image. The weekly run also builds the `full` default image (torch, TensorFlow, several GB of weights). |
| [Model links](../.github/workflows/model-links.yml) | `models/manifest.json` changes; weekly | Probes every manifest URL with a one-byte range request. A weekly failure opens an issue; the next passing run closes it. |
| [Link check](../.github/workflows/link-check.yml) | Markdown changes; weekly | lychee over the docs ([`.lychee.toml`](../.lychee.toml)). A weekly failure keeps one issue open with the report; the next clean run closes it. |
| [actionlint](../.github/workflows/actionlint.yml) | Workflow files change | Lints the workflows, including shellcheck on every `run:` block. |
| [zizmor](../.github/workflows/zizmor.yml) | `.github/` changes | Security audit of the workflows (injection, credential persistence, unpinned actions, permissions); any finding fails it. |

## Security

| Workflow | What it does |
| --- | --- |
| [CodeQL](../.github/workflows/codeql.yml) | `security-and-quality` queries over the Python code and the workflows, on every change and weekly. |
| [gitleaks](../.github/workflows/gitleaks.yml) | Secret scan of each push and pull request, and of the full history weekly. |
| [Dependency review](../.github/workflows/dependency-review.yml) | Blocks a pull request that adds a dependency with a known high or critical vulnerability. |
| [Scorecard](../.github/workflows/scorecard.yml) | OpenSSF Scorecard: grades the repository's supply-chain practices and publishes the score. |

Every third-party action is pinned to a full commit SHA (Dependabot keeps them current), every
job has a timeout and least-privilege `permissions`, and checkouts don't persist credentials.
Findings from CodeQL, Trivy and Scorecard land in the repository's Security tab. Dependabot alerts
and security updates are on, and [`.gitleaksignore`](../.gitleaksignore) lists the reviewed false
positives in the history.

## Monitoring the deployed demo

[Live demo](../.github/workflows/live-demo.yml) runs the browser test daily against
<https://multimodel-face-analyzer.streamlit.app/>. It wakes the app if Community Cloud put it to
sleep and drives it inside Community Cloud's iframe. A failure opens an issue
(`ci: the live demo check is failing`), with screenshots in the run's artifacts; the next passing
run closes it.

## Pull request automation

| Workflow | What it does |
| --- | --- |
| [PR title](../.github/workflows/pr-title.yml) | Squash merges use the title as the commit subject, so it must be a Conventional Commit. |
| [Labeler](../.github/workflows/labeler.yml) | Labels each pull request by area ([`.github/labeler.yml`](../.github/labeler.yml)). |
| [Dependabot auto-merge](../.github/workflows/dependabot-automerge.yml) | Turns on auto-merge for Dependabot's minor and patch pip and Actions updates; GitHub merges them once CI OK is green. It refuses unless `master`'s ruleset requires CI OK. Major and Docker updates wait for a person. A merge made this way runs no workflows on `master` (GitHub doesn't trigger them from its own token); the next push does. |

## Agents

These run Claude Code on the owner's Claude subscription through the `CLAUDE_CODE_OAUTH_TOKEN`
repository secret. They also need the Claude GitHub App installed on the repository. Until both
are set up, each one logs a notice and does nothing.

| Workflow | Trigger | What it does |
| --- | --- | --- |
| [Claude](../.github/workflows/claude.yml) | The owner mentions `@claude` in an issue, comment or review | Answers, reviews, or pushes a branch with a fix, following AGENTS.md. |
| [Claude review](../.github/workflows/claude-review.yml) | Every ready, same-repository pull request | Reviews against AGENTS.md and the Responsible use rules (demo gating, model honesty, the golden fixture, the Community Cloud install) with inline comments and one updated summary. |
| [Claude triage](../.github/workflows/claude-triage.yml) | A new issue | Adds type, area, `needs-info`, `duplicate` and `responsible-use` labels. Issue text is untrusted, so a fixed step fetches the issue and labels into files and the agent can only read files and add existing labels ([`add-labels.sh`](../.github/scripts/add-labels.sh)). |
| [Claude CI doctor](../.github/workflows/claude-ci-doctor.yml) | CI fails on a same-repository pull request | Reads the failed logs and the code, and comments the root cause and the smallest fix. |

[CodeRabbit](https://www.coderabbit.ai/) reviews pull requests too, configured in
[`.coderabbit.yaml`](../.coderabbit.yaml) to review against AGENTS.md, once its GitHub App is
installed for the repository.

## Running the checks locally

```bash
pip install -r requirements-dev.txt
ruff check . && ruff format --check . && typos && tools/typecheck.sh
python -m pytest -q --cov                               # the coverage floor applies

# The browser test, against a locally served demo:
pip install -r requirements-e2e.txt && python -m playwright install chromium
streamlit run streamlit_app.py --server.headless=true &
FACE_ANALYZER_E2E_URL=http://localhost:8501 python -m pytest tests/test_browser_smoke.py

actionlint && zizmor .github                            # after editing a workflow
hadolint Dockerfile                                     # after editing the Dockerfile
```
