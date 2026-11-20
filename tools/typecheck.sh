#!/usr/bin/env bash
# Run CI's type check (the basedpyright ratchet, docs/ci.md) in CI's environment.
#
# Type-check results depend on what is installed: torch, TensorFlow or mediapipe in the main
# .venv resolve imports that CI leaves unresolved, which changes the errors and makes
# basedpyright rewrite .basedpyright/baseline.json. So this keeps a separate .venv-types with
# exactly requirements-dev.txt, rebuilt when the requirements change.
#
# Usage: tools/typecheck.sh                    # what CI runs: fails on any new error
#        tools/typecheck.sh --writebaseline    # after fixing errors: shrink the baseline
set -euo pipefail
cd "$(dirname "$0")/.."
venv=.venv-types
stamp=$venv/.requirements-stamp
if [ ! -x "$venv/bin/python" ] || [ requirements-dev.txt -nt "$stamp" ] \
  || [ requirements.txt -nt "$stamp" ]; then
  # Start clean, so a package dropped from the requirements doesn't linger.
  rm -rf "$venv"
  if command -v uv > /dev/null; then
    uv venv -q --python 3.12 "$venv"
    VIRTUAL_ENV=$venv uv pip install -q -r requirements-dev.txt
  else
    python3 -m venv "$venv"
    "$venv/bin/pip" install -q -r requirements-dev.txt
  fi
  touch "$stamp"
fi
exec "$venv/bin/basedpyright" -p pyproject.toml --pythonpath "$venv/bin/python" "$@"
