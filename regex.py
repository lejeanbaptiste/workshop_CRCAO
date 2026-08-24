#!/usr/bin/env python3
"""
Batch TEI tagging / re-keying / unnesting for LJB XML.

Pipeline (each step optional)
-----------------------------
0. FIX ESCAPED — turn &amp;lt;persName …&amp;gt;…&amp;lt;/persName&amp;gt; back into real tags
   (damage from earlier versions that put markup into .text).
1. REKEY — existing <persName> whose string() equals SURFACE → set @key.
2. TAG — wrap untagged SURFACE by inserting real elements (not escaped text).
3. UNNEST — flatten same-name nests.

  python regex.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    from lxml import etree
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Install lxml: python -m pip install lxml") from exc

# ---------------------------------------------------------------------------
# CONFIG — edit these
# ---------------------------------------------------------------------------

DIRECTORY = Path("/Users/daniel/ShareDocs/@Home/ljb_test_project")
# Crawl these folders under DIRECTORY (empty list → scan DIRECTORY itself).
SUBDIRS: list[str] = ["annals", "bios", "ethno", "monographs"]
ONLY_FILES: list[str] = []

SURFACE = "江祏"
IDENT = "person-29f670ff-f416-47a6-a7c7-004ae48ca49e"
NAME_TAG = "persName"

# --- Step 0: repair escaped-as-text tags -----------------------------------
DO_FIX_ESCAPED = True
# Local names that may appear as &amp;lt;tag …&amp;gt;…&amp;lt;/tag&amp;gt; in files.
FIX_ESCAPED_TAGS: list[str] = [
    "persName",
    "placeName",
    "orgName",
    "roleName",
    "title",
    "rs",
    "note",
    "date",
]

# --- Step 1: rekey ---------------------------------------------------------
DO_REKEY = True
REKEY_REQUIRE_EXISTING_KEY = False

# --- Step 2: wrap untagged text (real elements) ----------------------------
DO_TAG = True

EXTRA_TAG_RULES: list[tuple[str, str]] = []
TAG_FLAGS = 0

# --- Step 3: unnest --------------------------------------------------------
DO_UNNEST = True
UNNEST_TAGS: list[str] = [
    "roleName",
    "persName",
    "placeName",
    "orgName",
    "title",
    "rs",
]
UNNEST_PASSES = 8

# --- Safety / I/O ----------------------------------------------------------
APPLY = True  # dry-run first; set True to write
CHECK_WELL_FORMED = True
RECURSIVE = False

TEI_NS = "http://www.tei-c.org/ns/1.0"
NS = {"tei": TEI_NS}
SKIP_NAMES = {"entities.xml"}

# ---------------------------------------------------------------------------
# XML I/O
# ---------------------------------------------------------------------------


def split_leading_pis(xml_text: str) -> tuple[str, str]:
    match = re.match(r"(?:\s*<\?[\s\S]*?\?>)*\s*", xml_text)
    if not match:
        return "", xml_text
    return xml_text[: match.end()], xml_text[match.end() :]


def parse_tei(xml_text: str) -> tuple[str, etree._Element]:
    leading, body = split_leading_pis(xml_text)
    root = etree.fromstring(body.encode("utf-8"))
    return leading, root


def serialize_tei(leading: str, root: etree._Element) -> str:
    body = etree.tostring(root, encoding="unicode")
    return f"{leading}{body}" if leading else body


def qname(local: str) -> str:
    return f"{{{TEI_NS}}}{local}"


def is_name_tag(node: etree._Element, local: str = NAME_TAG) -> bool:
    return node.tag in {qname(local), local}


# ---------------------------------------------------------------------------
# Step 0 — fix escaped tags in the raw XML string
# ---------------------------------------------------------------------------

# Matches &lt;tag…&gt;…&lt;/tag&gt; and &amp;lt;tag…&amp;gt;…&amp;lt;/tag&amp;gt; (any amp depth).
_ESC = r"&(?:amp;)*lt;"
_ESC_GT = r"&(?:amp;)*gt;"


def fix_escaped_elements(xml_text: str) -> tuple[str, int]:
    """
    Turn escaped-as-text start/end tags into real markup.

    Example (as stored on disk):
      &amp;lt;persName key="person-…"&amp;gt;太祖&amp;lt;/persName&amp;gt;
    →  <persName key="person-…">太祖</persName>
    """
    if not FIX_ESCAPED_TAGS:
        return xml_text, 0

    tags = "|".join(re.escape(t) for t in FIX_ESCAPED_TAGS)
    pattern = re.compile(
        rf"{_ESC}({tags})((?:\s[^&]*)?){_ESC_GT}(.*?){_ESC}/\1{_ESC_GT}",
        flags=re.DOTALL,
    )

    total = 0
    for _ in range(20):  # peel nested escaped layers if any
        xml_text, n = pattern.subn(r"<\1\2>\3</\1>", xml_text)
        total += n
        if n == 0:
            break
    return xml_text, total


# ---------------------------------------------------------------------------
# File iteration / rekey / tag / unnest
# ---------------------------------------------------------------------------


def iter_xml_files(directory: Path) -> list[Path]:
    glob = "**/*.xml" if RECURSIVE else "*.xml"
    roots = (
        [directory / name for name in SUBDIRS]
        if SUBDIRS
        else [directory]
    )
    out: list[Path] = []
    for root in roots:
        if not root.is_dir():
            print(f"Skipping missing folder: {root}")
            continue
        for path in sorted(root.glob(glob)):
            if path.name.lower() in SKIP_NAMES:
                continue
            if ONLY_FILES and path.name not in ONLY_FILES:
                continue
            out.append(path)
    return out


def element_string(node: etree._Element) -> str:
    return "".join(node.itertext())


def rekey_matching_names(root: etree._Element) -> int:
    xpath = (
        f"//tei:{NAME_TAG}[@key]"
        if REKEY_REQUIRE_EXISTING_KEY
        else f"//tei:{NAME_TAG}"
    )
    changed = 0
    for node in root.xpath(xpath, namespaces=NS):
        if element_string(node) != SURFACE:
            continue
        if node.get("key") == IDENT:
            continue
        node.set("key", IDENT)
        changed += 1
    return changed


def _make_name_element(following_text: str) -> etree._Element:
    el = etree.Element(qname(NAME_TAG))
    el.set("key", IDENT)
    el.text = SURFACE
    el.tail = following_text
    return el


def _wrap_surface_in_node_text(node: etree._Element) -> int:
    """Replace SURFACE in node.text by inserting real child elements."""
    raw = node.text
    if not raw or SURFACE not in raw:
        return 0
    parts = raw.split(SURFACE)
    count = len(parts) - 1
    node.text = parts[0]
    # Insert just after existing leading text, before any prior children.
    for i in range(count):
        node.insert(i, _make_name_element(parts[i + 1]))
    return count


def _wrap_surface_in_node_tail(node: etree._Element) -> int:
    """Replace SURFACE in node.tail by inserting real following siblings."""
    raw = node.tail
    if not raw or SURFACE not in raw:
        return 0
    parent = node.getparent()
    if parent is None:
        return 0
    parts = raw.split(SURFACE)
    count = len(parts) - 1
    node.tail = parts[0]
    idx = list(parent).index(node)
    for i in range(count):
        parent.insert(idx + 1 + i, _make_name_element(parts[i + 1]))
    return count


def tag_untagged_surface(root: etree._Element) -> int:
    """
    Wrap SURFACE outside existing NAME_TAG by creating real elements.

    Important: never assign '<persName>…</persName>' to .text/.tail — lxml
    would escape that into &lt;persName&gt; (or worse, &amp;lt; after a re-save).
    """
    total = 0
    # Snapshot: tree mutates as we insert.
    for node in list(root.iter()):
        inside = is_name_tag(node) or any(
            is_name_tag(a) for a in node.iterancestors()
        )

        if inside:
            total += _wrap_surface_in_node_tail(node)
            continue

        total += _wrap_surface_in_node_text(node)
        total += _wrap_surface_in_node_tail(node)
    return total


def apply_extra_regex_rules(text: str) -> tuple[str, int]:
    total = 0
    for pattern, replacement in EXTRA_TAG_RULES:
        text, n = re.compile(pattern, TAG_FLAGS).subn(replacement, text)
        total += n
    return text, total


def unnest_same_tag(text: str, tag: str) -> tuple[str, int]:
    pattern = re.compile(
        rf"<{tag}(\s[^>]*)?>\s*"
        rf"<{tag}(\s[^>]*)?>"
        rf"(.*?)"
        rf"</{tag}>\s*"
        rf"</{tag}>",
        flags=re.DOTALL,
    )
    return pattern.subn(rf"<{tag}\1>\3</{tag}>", text)


def unnest_all(text: str) -> tuple[str, int]:
    tag_list = list(UNNEST_TAGS) or sorted(
        set(re.findall(r"<([A-Za-z_][\w.-]*)\b[^>]*>\s*<\1\b", text))
    )
    total = 0
    for _ in range(UNNEST_PASSES):
        pass_count = 0
        for tag in tag_list:
            text, n = unnest_same_tag(text, tag)
            pass_count += n
        total += pass_count
        if pass_count == 0:
            break
    return text, total


def is_well_formed(xml_text: str) -> tuple[bool, str]:
    try:
        etree.fromstring(xml_text.encode("utf-8"))
        return True, ""
    except etree.XMLSyntaxError as exc:
        return False, str(exc)


def process_file(path: Path) -> dict[str, int | bool | str]:
    original = path.read_text(encoding="utf-8")
    text = original
    fixed = rekeyed = tagged = extra = unnested = 0

    if DO_FIX_ESCAPED:
        text, fixed = fix_escaped_elements(text)

    if DO_REKEY or DO_TAG:
        leading, root = parse_tei(text)
        if DO_REKEY:
            rekeyed = rekey_matching_names(root)
        if DO_TAG:
            tagged = tag_untagged_surface(root)
        text = serialize_tei(leading, root)

    if EXTRA_TAG_RULES:
        text, extra = apply_extra_regex_rules(text)

    if DO_UNNEST:
        text, unnested = unnest_all(text)

    changed = text != original
    ok, err = (True, "")
    if CHECK_WELL_FORMED and changed:
        ok, err = is_well_formed(text)

    if APPLY and changed and ok:
        path.write_text(text, encoding="utf-8")

    return {
        "path": path,
        "fixed": fixed,
        "rekeyed": rekeyed,
        "tagged": tagged + extra,
        "unnested": unnested,
        "changed": changed,
        "written": bool(APPLY and changed and ok),
        "well_formed": ok,
        "error": err,
    }


def main() -> None:
    directory = DIRECTORY.expanduser().resolve()
    if not directory.is_dir():
        sys.exit(f"Directory not found: {directory}")

    files = iter_xml_files(directory)
    if not files:
        sys.exit(f"No XML files to process in {directory}")

    mode = "APPLY (writing files)" if APPLY else "DRY-RUN (no writes)"
    print(f"{mode}")
    print(f"Directory: {directory}")
    if SUBDIRS:
        print(f"Subdirs: {', '.join(SUBDIRS)}")
    print(f"Files: {len(files)}")
    print(f"SURFACE={SURFACE!r} IDENT={IDENT} TAG={NAME_TAG}")
    print(
        f"fix_escaped={'on' if DO_FIX_ESCAPED else 'off'} "
        f"rekey={'on' if DO_REKEY else 'off'} "
        f"tag={'on' if DO_TAG else 'off'} "
        f"unnest={'on' if DO_UNNEST else 'off'}"
    )
    print()

    totals = {
        "fixed": 0,
        "rekeyed": 0,
        "tagged": 0,
        "unnested": 0,
        "changed": 0,
        "written": 0,
        "bad": 0,
    }
    for path in files:
        result = process_file(path)
        try:
            label = path.relative_to(directory)
        except ValueError:
            label = path.name
        for key in ("fixed", "rekeyed", "tagged", "unnested"):
            totals[key] += int(result[key])
        if result["changed"]:
            totals["changed"] += 1
        if result["written"]:
            totals["written"] += 1
        if result["changed"] and not result["well_formed"]:
            totals["bad"] += 1
            print(f"❌ {label}: not well-formed — {result['error']}")
        elif result["changed"]:
            flag = "wrote" if result["written"] else "would write"
            print(
                f"✔ {label}: fixed={result['fixed']} "
                f"rekeyed={result['rekeyed']} tagged={result['tagged']} "
                f"unnested={result['unnested']} ({flag})"
            )
        else:
            print(f"· {label}: no change")

    print()
    print(
        f"Done. changed={totals['changed']} written={totals['written']} "
        f"fixed={totals['fixed']} rekeyed={totals['rekeyed']} "
        f"tagged={totals['tagged']} unnested={totals['unnested']} "
        f"ill_formed={totals['bad']}"
    )
    if not APPLY:
        print("Dry-run only. Set APPLY = True to save.")
        if totals["fixed"] > 0:
            print(
                f"NOTE: found {totals['fixed']} escaped-as-text tag(s) "
                "(&lt;persName&gt; …). Re-run with APPLY = True to repair them."
            )


if __name__ == "__main__":
    main()
