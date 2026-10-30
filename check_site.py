"""Browser check for the deployed static pages and their real watch links.

Start `python -m http.server 8788` in this directory, then run this script.
Screenshots and report are written outside the Git checkout.
"""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlsplit

from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8788/"
OUT = Path(__file__).resolve().parent.parent / "laughmyway_site_qa"
OUT.mkdir(exist_ok=True)
expected_ids = {"IWxNrUUVN2g", "qyPXSNvSQA4", "nYghXrOrBaI", "il8YnHuqrxA", "XUfRmhWa7Rc", "YhDe1e3aIIA", "3QzF7v3I-uY", "kWx9wcoKhnE", "xxJkpsT1tPM", "hd8rXPjgIZ0"}

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    results = {}
    for width, height, name in ((1440, 900, "desktop"), (390, 844, "phone"), (320, 720, "small-phone")):
        page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        response = page.goto(BASE, wait_until="networkidle")
        assert response and response.status == 200
        assert page.locator("h1").count() == 1
        assert page.locator(".film").count() == 5
        assert page.locator(".short").count() == 5
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), f"horizontal overflow: {name}"
        assert not errors, errors
        page.locator("img").evaluate_all("els => els.forEach(e => e.loading = 'eager')")
        page.wait_for_function("[...document.images].every(e => e.complete && e.naturalWidth > 0)")
        hrefs = page.locator("a[href]").evaluate_all("els => els.map(e => e.href)")
        present_ids = {i for href in hrefs for i in expected_ids if i in href}
        assert expected_ids == present_ids, expected_ids - present_ids
        for href in hrefs:
            parsed = urlsplit(href)
            if parsed.netloc == "127.0.0.1:8788" and not parsed.fragment:
                assert page.request.get(href).status == 200, href
        if name == "phone":
            page.get_by_role("link", name="The films", exact=True).click()
            assert page.evaluate("location.hash") == "#films"
            page.goto(BASE, wait_until="networkidle")
        page.screenshot(path=str(OUT / f"home-{name}.png"), full_page=True)
        results[name] = {"status": response.status, "width": width, "overflow": False, "images": page.locator("img").count(), "javascript_errors": errors}
        page.close()
    page = browser.new_page(viewport={"width": 390, "height": 844})
    for path in ("privacy/", "terms/", "publisher/"):
        response = page.goto(BASE + path, wait_until="networkidle")
        assert response and response.status == 200, path
        assert page.locator("h1").count() == 1
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), f"horizontal overflow: {path}"
        page.screenshot(path=str(OUT / f"{path.strip('/')}-phone.png"), full_page=True)
        results[path] = {"status": response.status, "overflow": False}
    browser.close()

(OUT / "report.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
print(json.dumps(results, indent=2))
