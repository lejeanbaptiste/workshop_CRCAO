#!/usr/bin/env python3
"""Count title elements in a directory of XML files."""

from __future__ import annotations

import argparse
import csv
import xml.etree.ElementTree as ET
from pathlib import Path


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def count_titles(xml_path: Path) -> dict[str, object]:
    root = ET.parse(xml_path).getroot()
    title_elements = [e for e in root.iter() if local_name(e.tag) == "title"]
    return {
        "file": xml_path.name,
        "title_count": len(title_elements),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "input_dir",
        type=Path,
        help="Directory containing the transformed XML files",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/chapter-06"),
        help="Directory for the summary CSV",
    )
    args = parser.parse_args()

    xml_files = sorted(args.input_dir.glob("*.xml"))
    if not xml_files:
        raise SystemExit(f"No XML files found in {args.input_dir}")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    rows = [count_titles(path) for path in xml_files]
    total = sum(int(row["title_count"]) for row in rows)

    with (args.output_dir / "title_counts.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["file", "title_count"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Files analysed: {len(rows)}")
    print(f"Total title elements: {total}")
    print(f"Results: {args.output_dir}")


if __name__ == "__main__":
    main()
