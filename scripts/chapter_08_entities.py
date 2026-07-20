#!/usr/bin/env python3
"""Summarise disambiguated XML entities and export tables for follow-up work."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path

from chapter_08_analyses import (
    keyed_mention_rows,
    leakage_summary,
    load_entity_registry,
    person_registry_table,
    setup_scripts_path,
)


def write_chart(output_dir: Path, summary: list[dict[str, object]]) -> None:
    import matplotlib.pyplot as plt

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


def analyse(xml_path: Path) -> list[dict[str, str]]:
    """Return keyed mention rows (compat with older notebook imports)."""
    rows = keyed_mention_rows(xml_path)
    return [
        {
            "tag": r["tag"],
            "key": r["key"],
            "surface_form": r["surface_form"],
            "type": "",
            "ref": r.get("ref", ""),
            "when": r.get("when", ""),
        }
        for r in rows
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("xml", type=Path, help="XML/TEI file with @key attributes")
    parser.add_argument("--entities", type=Path, help="entities.xml (optional)")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/chapter-08"))
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    setup_scripts_path()
    rows = analyse(args.xml)
    counts = Counter(row["key"] for row in rows)
    summary = [
        {
            "key": key,
            "mentions": count,
            "surface_forms": "; ".join(
                sorted({r["surface_form"] for r in rows if r["key"] == key})
            ),
        }
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
    leakage_summary(args.xml).to_csv(args.output_dir / "leakage_summary.csv", index=False)
    if args.entities and args.entities.is_file():
        person_registry_table(args.xml, args.entities).to_csv(
            args.output_dir / "person_registry.csv", index=False
        )
    write_chart(args.output_dir, summary)
    print(f"Mentions désambiguïsées : {len(rows)}")
    print(f"Entités distinctes : {len(counts)}")
    print(f"Résultats : {args.output_dir}")


if __name__ == "__main__":
    main()
