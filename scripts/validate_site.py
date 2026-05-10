#!/usr/bin/env python3
"""Local validation for the static Step3D GitHub Pages site.

Checks:
- HTML files are parseable by Python's HTMLParser;
- local href/src links point to existing files or directories with index.html;
- inline JavaScript from index.html passes `node --check` when Node is available.
"""
from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        value = data.get("href") or data.get("src")
        if value:
            self.links.append(value)


def html_files() -> list[Path]:
    ignored = {ROOT / ".git"}
    files = []
    for path in ROOT.rglob("*.html"):
        if any(parent in ignored for parent in path.parents):
            continue
        files.append(path)
    return sorted(files)


def is_external(link: str) -> bool:
    return link.startswith(("http://", "https://", "mailto:", "tel:", "data:", "#"))


def validate_html_and_links() -> list[str]:
    errors: list[str] = []
    for file in html_files():
        parser = LinkParser()
        try:
            parser.feed(file.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"HTML parse failed: {file.relative_to(ROOT)}: {exc}")
            continue

        for link in parser.links:
            if is_external(link):
                continue
            clean = link.split("#", 1)[0].split("?", 1)[0]
            if not clean:
                continue
            target = (file.parent / unquote(clean)).resolve()
            try:
                target.relative_to(ROOT)
            except ValueError:
                continue
            if clean.endswith("/"):
                exists = (target / "index.html").exists()
            else:
                exists = target.exists() or (target / "index.html").exists()
            if not exists:
                errors.append(
                    f"Broken local link in {file.relative_to(ROOT)}: {link} -> {target.relative_to(ROOT)}"
                )
    return errors


def validate_canonical_urls() -> list[str]:
    errors: list[str] = []
    canonical_tag_re = re.compile(r'<link[^>]+rel=["\']canonical["\'][^>]*>|<link[^>]+href=["\'][^"\']+["\'][^>]+rel=["\']canonical["\'][^>]*>', re.I)
    href_re = re.compile(r'href=["\']([^"\']+)["\']', re.I)
    for file in html_files():
        text = file.read_text(encoding="utf-8")
        tag_match = canonical_tag_re.search(text)
        if not tag_match:
            continue
        href_match = href_re.search(tag_match.group(0))
        if not href_match:
            errors.append(f"Canonical tag without href: {file.relative_to(ROOT)}")
            continue
        canonical = href_match.group(1)
        if canonical.endswith("/index.html"):
            errors.append(
                f"Canonical should use trailing slash, not /index.html: {file.relative_to(ROOT)} -> {canonical}"
            )
    return errors


def validate_index_js() -> list[str]:
    index = ROOT / "index.html"
    if not index.exists():
        return ["index.html not found"]
    text = index.read_text(encoding="utf-8")
    if "<script>" not in text or "</script>" not in text:
        return []
    js = text[text.index("<script>") + len("<script>") : text.rindex("</script>")]
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as tmp:
        tmp.write(js)
        tmp_path = Path(tmp.name)
    try:
        result = subprocess.run(["node", "--check", str(tmp_path)], text=True, capture_output=True)
        if result.returncode != 0:
            return ["node --check failed for index.html inline script:\n" + result.stderr.strip()]
    except FileNotFoundError:
        return ["node not found; skipped JS syntax validation"]
    finally:
        tmp_path.unlink(missing_ok=True)
    return []


def main() -> int:
    errors = validate_html_and_links() + validate_canonical_urls() + validate_index_js()
    if errors:
        print("Step3D validation failed:\n")
        for error in errors:
            print("-", error)
        return 1
    print(f"Step3D validation ok: {len(html_files())} HTML files checked, local links ok, JS ok.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
