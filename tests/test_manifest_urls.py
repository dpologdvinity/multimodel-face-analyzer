"""Check that every downloadable model URL in models/manifest.json is still reachable.

Opt-in because it needs the network: set FACE_ANALYZER_NETWORK_TESTS=1. Each URL gets a one-byte
range request, so nothing is downloaded. A scheduled CI job runs it to catch upstream link rot
(a deleted repo or file breaks every Docker build that selects the model).
"""

import importlib.util
import os
import urllib.error
import urllib.request
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
_SPEC = importlib.util.spec_from_file_location(
    "fetch_models", ROOT / "tools" / "fetch_models.py"
)
assert _SPEC is not None and _SPEC.loader is not None
fetch_models = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(fetch_models)

_DOWNLOADABLE = [
    entry for entry in fetch_models.load_manifest() if entry["source"] != "manual"
]

pytestmark = pytest.mark.skipif(
    os.environ.get("FACE_ANALYZER_NETWORK_TESTS") != "1",
    reason="network test; set FACE_ANALYZER_NETWORK_TESTS=1",
)


@pytest.mark.parametrize(
    "entry", _DOWNLOADABLE, ids=[entry["path"] for entry in _DOWNLOADABLE]
)
def test_download_url_is_reachable(entry):
    """Request the first byte of each downloadable file and expect a success status."""
    request = urllib.request.Request(
        entry["url"],
        headers={"User-Agent": fetch_models.USER_AGENT, "Range": "bytes=0-0"},
    )
    try:
        with urllib.request.urlopen(
            request, timeout=fetch_models.TIMEOUT_SECONDS
        ) as response:
            status = response.status
    except urllib.error.HTTPError as exc:
        pytest.fail(
            f"HTTP {exc.code} for {entry['url']} (upstream: {entry.get('upstream')})"
        )
    assert status in (200, 206), f"HTTP {status} for {entry['url']}"
