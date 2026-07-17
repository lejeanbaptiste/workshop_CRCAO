#!/usr/bin/env python3
"""Summarise disambiguated XML entities and export a table for follow-up work."""

from __future__ import annotations

import argparse
import csv
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt


TAGS = {"persName", "placeName", "orgName", "name", "title"}


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def text_of(element: ET.Element) -> str:
    return "".join(element.itertext()).strip()


def analyse(xml_path: Path) -> list[dict[str, str]]:
    root = ET.parse(xml_path).getroot()
    rows: list[dict[str, str]] = []
    for element in root.iter():
        if local_name(element.tag) not in TAGS or not element.get("key"):
            continue
        rows.append({
            "tag": local_name(element.tag),
            "key": element.get("key", ""),
            "surface_form": text_of(element),
            "type": element.get("type", ""),
            "ref": element.get("ref", ""),
            "when": element.get("when", ""),
        })
    return rows


def write_chart(output_dir: Path, summary: list[dict[str, object]]) -> None:
    top = summary[:20]
    if not top:
        return
    labels = [str(row["key"]) for row in reversed(top)]
    values = [int(row["mentions"]) for row in reversed(top)]
    plt.figure(figsize=(8, max(4.5, len(top) * 0.28)))
    plt.barh(labels, values)
    plt.xlabel("Mentions")
    plt.title("Entités désambiguïsées les plus fréquentes")
    plt.tight_layout()
    plt.savefig(output_dir / "top_entities.png", dpi=150)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("xml", type=Path, help="XML/TEI file with @key attributes")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/chapter-08"))
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    rows = analyse(args.xml)
    counts = Counter(row["key"] for row in rows)
    summary = [
        {"key": key, "mentions": count, "surface_forms": "; ".join(sorted({r["surface_form"] for r in rows if r["key"] == key}))}
        for key, count in counts.most_common()
    ]
    fields = ["tag", "key", "surface_form", "type", "ref", "when"]
    with (args.output_dir / "entity_mentions.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    with (args.output_dir / "entity_summary.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["key", "mentions", "surface_forms"])
        writer.writeheader()
        writer.writerows(summary)
    write_chart(args.output_dir, summary)
    print(f"Mentions désambiguïsées : {len(rows)}")
    print(f"Entités distinctes : {len(counts)}")
    print(f"Résultats : {args.output_dir}")


if __name__ == "__main__":
    main()
