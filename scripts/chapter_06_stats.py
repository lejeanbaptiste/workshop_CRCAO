#!/usr/bin/env python3
"""Extract tagged strings and paragraph-level statistics from XML/TEI."""

from __future__ import annotations

import argparse
import csv
import re
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def text_of(element: ET.Element) -> str:
    return "".join(element.itertext()).strip()


def analyse(xml_path: Path) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    root = ET.parse(xml_path).getroot()
    tagged: list[dict[str, object]] = []
    paragraphs: list[dict[str, object]] = []

    for paragraph_number, paragraph in enumerate(
        (e for e in root.iter() if local_name(e.tag) in {"p", "ab"}), start=1
    ):
        tagged_in_paragraph = [
            e for e in paragraph.iter() if e is not paragraph and len(e) == 0
        ]
        # Include tagged elements that contain nested markup, while avoiding
        # double-counting descendants of another tagged element.
        tagged_in_paragraph = [
            e
            for e in paragraph.iter()
            if e is not paragraph and local_name(e.tag) in {
                "persName", "placeName", "orgName", "title", "date", "name"
            }
        ]
        for element in tagged_in_paragraph:
            value = text_of(element)
            if value:
                tagged.append({
                    "paragraph": paragraph_number,
                    "tag": local_name(element.tag),
                    "value": value,
                    "length": len(value),
                })
        paragraphs.append({
            "paragraph": paragraph_number,
            "characters": len(text_of(paragraph)),
            "words": len(re.findall(r"\S+", text_of(paragraph))),
            "tagged_items": len(tagged_in_paragraph),
        })

    return tagged, paragraphs


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_charts(output_dir: Path, tagged: list[dict[str, object]], paragraphs: list[dict[str, object]]) -> None:
    tag_counts = Counter(row["tag"] for row in tagged)
    if tag_counts:
        names, values = zip(*tag_counts.most_common())
        plt.figure(figsize=(8, 4.5))
        plt.bar(names, values)
        plt.ylabel("Nombre d'occurrences")
        plt.title("Occurrences par type de balise")
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()
        plt.savefig(output_dir / "tag_frequencies.png", dpi=150)
        plt.close()

    if paragraphs:
        numbers = [row["paragraph"] for row in paragraphs]
        values = [row["tagged_items"] for row in paragraphs]
        plt.figure(figsize=(10, 4.5))
        plt.bar(numbers, values)
        plt.xlabel("Paragraphe")
        plt.ylabel("Éléments balisés")
        plt.title("Éléments balisés par paragraphe")
        plt.tight_layout()
        plt.savefig(output_dir / "tagged_items_by_paragraph.png", dpi=150)
        plt.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("xml", type=Path, help="XML/TEI file to analyse")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/chapter-06"))
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    tagged, paragraphs = analyse(args.xml)
    counts = [
        {"tag": tag, "value": value, "count": count}
        for (tag, value), count in Counter((r["tag"], r["value"]) for r in tagged).most_common()
    ]
    write_csv(args.output_dir / "tagged_strings.csv", tagged, ["paragraph", "tag", "value", "length"])
    write_csv(args.output_dir / "tagged_string_counts.csv", counts, ["tag", "value", "count"])
    write_csv(args.output_dir / "paragraph_stats.csv", paragraphs, ["paragraph", "characters", "words", "tagged_items"])
    write_charts(args.output_dir, tagged, paragraphs)
    print(f"Éléments balisés : {len(tagged)}")
    print(f"Paragraphes analysés : {len(paragraphs)}")
    print(f"Résultats : {args.output_dir}")


if __name__ == "__main__":
    main()
