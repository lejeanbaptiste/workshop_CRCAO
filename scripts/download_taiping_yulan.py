#!/usr/bin/env python3
"""Download and convert the Taiping Yulan Wikisource volumes to simple TEI.

The output intentionally matches the small corpus used by the workshop:
one TEI file per volume, one ``<p>`` per source entry, and ``<title>`` around
book titles written between the Chinese corner brackets 《 and 》.

The source is Wikisource's public API.  The downloader is conservative about
Wikisource markup: it removes navigation/editorial templates and links while
preserving the Chinese source text.  It is a demonstration corpus, not a
critical scholarly edition.
"""

from __future__ import annotations

import argparse
import json
import re
import time
import urllib.parse
import urllib.request
from urllib.error import HTTPError
from pathlib import Path
from xml.etree import ElementTree as ET

API_URL = "https://zh.wikisource.org/w/api.php"
USER_AGENT = "WorkshopCorpusDownloader/1.0 (educational corpus preparation)"
DEFAULT_OUTPUT = Path("data/taiping-yulan-full")


def api_query(params: dict[str, str], attempts: int = 6) -> dict:
    url = API_URL + "?" + urllib.parse.urlencode(params)
    for attempt in range(attempts):
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return json.load(response)
        except HTTPError as error:
            if error.code not in {429, 500, 502, 503, 504} or attempt == attempts - 1:
                raise
            delay = min(60, 2 ** attempt * 2)
            print(f"API returned HTTP {error.code}; retrying in {delay}s")
            time.sleep(delay)
    raise RuntimeError("API request failed")


def fetch_pages(
    volume_numbers: list[int],
    on_batch: callable | None = None,
    batch_size: int = 20,
) -> dict[str, str]:
    pages: dict[str, str] = {}
    for start in range(0, len(volume_numbers), batch_size):
        batch = volume_numbers[start : start + batch_size]
        titles = "|".join(f"太平御覽/{number:04d}" for number in batch)
        data = api_query(
            {
                "action": "query",
                "titles": titles,
                "prop": "revisions",
                "rvprop": "content",
                "rvslots": "main",
                "format": "json",
                "formatversion": "2",
            }
        )
        for page in data.get("query", {}).get("pages", []):
            revisions = page.get("revisions", [])
            if revisions:
                content = revisions[0].get("slots", {}).get("main", {}).get("content")
                if content is not None:
                    pages[page["title"]] = content
        if on_batch:
            on_batch(pages)
        print(f"Downloaded {min(start + batch_size, len(volume_numbers))}/{len(volume_numbers)} volumes")
        time.sleep(1.0)
    return pages


def strip_templates(text: str) -> str:
    """Remove nested ``{{...}}`` templates without damaging surrounding text."""
    while "{{" in text:
        starts = [m.start() for m in re.finditer(r"{{", text)]
        replaced = False
        for start in reversed(starts):
            end = text.find("}}", start + 2)
            if end >= 0:
                text = text[:start] + text[end + 2 :]
                replaced = True
        if not replaced:
            break
    return text


def clean_wikitext(text: str) -> list[str]:
    """Turn a Wikisource page into source-entry strings."""
    text = strip_templates(text)
    text = re.sub(r"<ref\b[^>]*>.*?</ref\s*>", "", text, flags=re.I | re.S)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\[https?://[^\s\]]+\s*([^\]]*)\]", r"\1", text)

    def link(match: re.Match[str]) -> str:
        target, label = match.group(1), match.group(2)
        return label or target.split("#", 1)[0]

    text = re.sub(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", link, text)
    text = re.sub(r"'{2,5}", "", text)

    entries: list[str] = []
    for raw in re.split(r"\n\s*\n+", text):
        raw = raw.strip()
        if not raw or re.match(r"^(=+|\*|\#|;|:)", raw):
            continue
        raw = re.sub(r"\s+", " ", raw)
        raw = re.sub(r"《([^《》]+)》", r"<title>《\1》</title>", raw)
        raw = raw.replace("&", "&amp;")
        raw = re.sub(r"<title>(.*?)</title>", lambda m: m.group(0).replace("&amp;", "&"), raw)
        if raw:
            entries.append(raw)
    return entries


def make_tei(entries: list[str]) -> bytes:
    root = ET.Element("TEI", {"xmlns": "http://www.tei-c.org/ns/1.0"})
    body = ET.SubElement(ET.SubElement(root, "text"), "body")
    div = ET.SubElement(body, "div")
    for entry in entries:
        paragraph = ET.SubElement(div, "p")
        # Parse the title markers as XML while keeping all other text literal.
        parts = re.split(r"(<title>.*?</title>)", entry)
        for part in parts:
            if not part:
                continue
            match = re.fullmatch(r"<title>(.*?)</title>", part)
            if match:
                title = ET.SubElement(paragraph, "title")
                title.text = match.group(1)
            else:
                if len(paragraph) == 0:
                    paragraph.text = (paragraph.text or "") + part
                else:
                    paragraph[-1].tail = (paragraph[-1].tail or "") + part
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--end", type=int, default=1000)
    args = parser.parse_args()
    if not 1 <= args.start <= args.end <= 1000:
        raise SystemExit("Volume range must be within 0001–1000")

    numbers = list(range(args.start, args.end + 1))
    args.output.mkdir(parents=True, exist_ok=True)

    def save_batch(pages: dict[str, str]) -> None:
        for page_title, content in pages.items():
            number = int(page_title.rsplit("/", 1)[1])
            output = args.output / f"{number:04d}.xml"
            if not output.exists():
                output.write_bytes(make_tei(clean_wikitext(content)))

    pages = fetch_pages(numbers, on_batch=save_batch)
    missing: list[str] = []
    for number in numbers:
        page_title = f"太平御覽/{number:04d}"
        content = pages.get(page_title)
        if content is None:
            missing.append(page_title)
            continue
        output = args.output / f"{number:04d}.xml"
        if not output.exists():
            output.write_bytes(make_tei(clean_wikitext(content)))

    print(f"Converted: {len(numbers) - len(missing)} volumes")
    print(f"Output: {args.output}")
    if missing:
        print("Missing pages:")
        print("\n".join(missing))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
