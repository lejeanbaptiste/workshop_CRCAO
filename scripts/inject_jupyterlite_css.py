#!/usr/bin/env python3
"""Copy workshop CSS into the JupyterLite build and link it from app pages."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
SOURCE_CSS = ROOT / "static" / "custom.css"
TARGET_CSS = DIST / "custom.css"
LINK_TAG = '<link rel="stylesheet" href="../custom.css">\n'


def inject_link(html_path: Path) -> None:
    html = html_path.read_text(encoding="utf-8")
    if "custom.css" in html:
        return
    if "</head>" not in html:
        raise RuntimeError(f"Could not find </head> in {html_path}")
    html_path.write_text(html.replace("</head>", f"{LINK_TAG}</head>", 1), encoding="utf-8")


def main() -> None:
    if not SOURCE_CSS.exists():
        raise FileNotFoundError(SOURCE_CSS)
    if not DIST.exists():
        raise FileNotFoundError(f"Build output not found: {DIST}")

    TARGET_CSS.write_text(SOURCE_CSS.read_text(encoding="utf-8"), encoding="utf-8")

    for app in ("lab", "notebook", "repl", "consoles", "tree", "edit"):
        html_path = DIST / app / "index.html"
        if html_path.exists():
            inject_link(html_path)


if __name__ == "__main__":
    main()
