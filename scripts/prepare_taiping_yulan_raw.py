#!/usr/bin/env python3
"""Make an untagged Chapter 5 input corpus from the converted TEI corpus."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("data/taiping-yulan-full"))
    parser.add_argument("--output", type=Path, default=Path("data/taiping-yulan-raw"))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    for source in sorted(args.input.glob("*.xml")):
        target = args.output / source.name
        text = source.read_text(encoding="utf-8")
        text = re.sub(r"<title>(.*?)</title>", r"\1", text, flags=re.S)
        target.write_text(text, encoding="utf-8")

    print(f"Prepared {len(list(args.output.glob('*.xml')))} raw XML files in {args.output}")


if __name__ == "__main__":
    main()
