# Security policy

## Supported versions

Only the latest commit on `master` (and the public demo deployed from it) gets security fixes.

## Reporting a vulnerability

Please report vulnerabilities privately through
[GitHub's private vulnerability reporting](https://github.com/dpologdvinity/multimodel-face-analyzer/security/advisories/new),
not in a public issue. Include the steps to reproduce, the affected version or commit, and the
impact you expect. You should get a first response within a week.

Things that count: code execution through an uploaded image or a model file, a way around the
demo's upload limits or its no-storage guarantee, leaking one visitor's faces to another, and
supply-chain issues in the build (a model download that skips its sha256 check, for example).

## How the project guards itself

CI runs CodeQL, gitleaks, pip-audit, dependency review, zizmor (workflow security), Trivy on the
Docker image and OpenSSF Scorecard; [docs/ci.md](docs/ci.md) describes each check.
