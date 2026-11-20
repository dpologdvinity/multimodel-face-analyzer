"""Drive a running app in a real browser: load it, analyze the sample photo, switch themes.

Opt-in because it needs a served app and Playwright's Chromium: set FACE_ANALYZER_E2E_URL to the
app's address. CI serves the public demo, streamlit_app.py, after a plain
`pip install -r requirements.txt` (the same install Streamlit Community Cloud does), and a daily
job points it at the deployed demo itself: a sleeping Community Cloud app is woken first, and
the app is driven inside the iframe Community Cloud serves it in. Set FACE_ANALYZER_E2E_SHOTS to
a directory to keep a screenshot of each theme.
"""

import os
import re
from collections.abc import Iterator
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from playwright.sync_api import Frame, Page

E2E_URL = os.environ.get("FACE_ANALYZER_E2E_URL", "")

pytestmark = pytest.mark.skipif(
    not E2E_URL, reason="browser test; set FACE_ANALYZER_E2E_URL to a running app"
)

# The first analysis loads every demo model, which takes a while on a cold CI runner.
FIRST_ANALYSIS_MS = 180_000
# Waking a sleeping Community Cloud app restarts its container and reinstalls nothing, ~1 min.
WAKE_MS = 300_000
# Community Cloud serves the app itself at this path, inside an iframe on the app's page.
CLOUD_APP_PATH = "/~/+/"
# Consecutive idle readings, 0.5 s apart, that count as a finished run.
IDLE_CHECKS = 6
# The NASA Expedition 59 crew portrait (ui/sample_photo.jpg) shows six people.
SAMPLE_FACES = 6


def _app_frame(page: "Page") -> "Frame":
    """Return the frame the Streamlit app runs in, waking a sleeping Community Cloud app first."""
    wake = page.get_by_role("button", name=re.compile("get this app back up"))
    for _ in range(WAKE_MS // 1000):
        # Served locally, the page is the app; on Community Cloud it is an iframe in the page.
        if page.get_by_test_id("stMain").count():
            return page.main_frame
        for frame in page.frames:
            if CLOUD_APP_PATH in frame.url:
                return frame
        if wake.is_visible():
            wake.click()
        page.wait_for_timeout(1000)
    raise AssertionError(f"no Streamlit app at {E2E_URL} after {WAKE_MS // 1000} s")


@pytest.fixture(scope="module")
def page() -> Iterator["Page"]:
    """Open one browser page on the app, shared by the tests in order."""
    sync_api = pytest.importorskip("playwright.sync_api")
    with sync_api.sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={"width": 1400, "height": 1000})
        page.goto(E2E_URL)
        yield page
        browser.close()


@pytest.fixture(scope="module")
def app(page: "Page") -> "Frame":
    """Return the frame the app renders in (the page itself unless on Community Cloud)."""
    return _app_frame(page)


def _settle(app: "Frame") -> None:
    """Wait until the app has been idle (no run in progress, no spinner) for a few seconds."""
    # A rerun starts a moment after the click that causes it, and Community Cloud hides the
    # status widget from viewers, so one idle reading can come before the run; require several.
    busy = app.get_by_test_id("stStatusWidget").or_(app.get_by_test_id("stSpinner"))
    quiet = 0
    for _ in range(FIRST_ANALYSIS_MS // 500):
        quiet = 0 if busy.count() else quiet + 1
        if quiet >= IDLE_CHECKS:
            return
        app.page.wait_for_timeout(500)
    pytest.fail("the app was still busy after the analysis timeout")


def _shot(page: "Page", name: str) -> None:
    """Save a screenshot when FACE_ANALYZER_E2E_SHOTS names a directory."""
    shots = os.environ.get("FACE_ANALYZER_E2E_SHOTS")
    if shots:
        Path(shots).mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(Path(shots) / f"{name}.png"))


def _assert_no_exception(app: "Frame") -> None:
    """Fail on any Streamlit exception box, showing its text."""
    errors = app.locator("[data-testid=stException]")
    assert errors.count() == 0, errors.first.inner_text()


def test_app_loads_with_the_responsible_use_notice(app: "Frame") -> None:
    """Render the app and the appearance-not-identity notice without an exception."""
    sync_api = pytest.importorskip("playwright.sync_api")
    main = app.get_by_test_id("stMain")
    sync_api.expect(main.get_by_text("not who a person is")).to_be_visible(
        timeout=WAKE_MS
    )
    _assert_no_exception(app)


def test_sample_photo_finds_every_face(page: "Page", app: "Frame") -> None:
    """Analyze the bundled sample photo end to end and find each crew member."""
    sync_api = pytest.importorskip("playwright.sync_api")
    app.get_by_role("button", name="No photo? Try a sample").click()
    summary = app.get_by_text(re.compile(r"faces? found"))
    sync_api.expect(summary).to_be_visible(timeout=FIRST_ANALYSIS_MS)
    _settle(app)
    count = app.get_by_test_id("stMain").inner_text()
    assert re.search(rf"\b{SAMPLE_FACES}\s+faces found", count), count
    _assert_no_exception(app)
    _shot(page, "night")


def test_day_theme_switches_the_page(page: "Page", app: "Frame") -> None:
    """Pick the Day theme in the sidebar and see its marker class reach the page."""
    sync_api = pytest.importorskip("playwright.sync_api")
    expand = app.get_by_test_id("stExpandSidebarButton")
    if expand.is_visible():
        expand.click()
    sidebar = app.get_by_test_id("stSidebar")
    sidebar.get_by_test_id("stSelectbox").filter(has_text="Theme").click()
    app.get_by_role("option", name="Day (light)").click()
    sync_api.expect(app.locator("body:has(.theme-day)")).to_have_count(
        1, timeout=60_000
    )
    _settle(app)
    sync_api.expect(app.get_by_text(re.compile(r"faces? found"))).to_be_visible()
    _assert_no_exception(app)
    _shot(page, "day")
