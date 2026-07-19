#!/usr/bin/env python3
"""Embed the regex-replace and title-count scripts into chapter 5 notebook."""

from __future__ import annotations

import json
from pathlib import Path


NOTEBOOK = Path("Workshop/notebooks/course/05_balisage_rapide.ipynb")


def code_cell(source: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source.splitlines(keepends=True),
    }


def markdown_cell(source: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source.splitlines(keepends=True),
    }


def main() -> None:
    nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))

    nb["cells"][3] = code_cell(
        """from __future__ import annotations

import hashlib
import re
from pathlib import Path


def run_id(pattern: str, replacement: str, flags: int) -> str:
    digest = hashlib.sha1(f"{pattern}\\0{replacement}\\0{flags}".encode("utf-8")).hexdigest()
    return digest[:12]


def compile_flags(names: list[str]) -> int:
    flag_map = {
        "ignorecase": re.IGNORECASE,
        "multiline": re.MULTILINE,
        "dotall": re.DOTALL,
        "verbose": re.VERBOSE,
    }
    flags = 0
    for name in names:
        key = name.lower()
        if key not in flag_map:
            raise ValueError(f"Unknown regex flag: {name}")
        flags |= flag_map[key]
    return flags


def process_file(src: Path, dst: Path, pattern: re.Pattern[str], replacement: str) -> int:
    text = src.read_text(encoding="utf-8")
    updated, count = pattern.subn(replacement, text)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(updated, encoding="utf-8")
    return count


def regex_replace_directory(
    pattern: str,
    replacement: str,
    input_dir: Path = Path("taiping_yulan_xml"),
    output_root: Path = Path("outputs/chapter-05"),
    flag_names: list[str] | None = None,
    run_name: str = "",
) -> Path:
    flags = compile_flags(flag_names or [])
    compiled = re.compile(pattern, flags)
    label = run_name.strip() or run_id(pattern, replacement, flags)
    output_dir = output_root / label
    output_dir.mkdir(parents=True, exist_ok=True)

    source_files = sorted(input_dir.glob("*.xml"))
    if not source_files:
        raise FileNotFoundError(f"No XML files found in {input_dir}")

    changed_total = 0
    for src in source_files:
        dst = output_dir / src.name
        changed_total += process_file(src, dst, compiled, replacement)

    print(f"Files processed: {len(source_files)}")
    print(f"Total substitutions: {changed_total}")
    print(f"Output directory: {output_dir}")
    return output_dir


# Exemple : baliser tous les titres entre 《...》 comme <title>...</title>.
output_dir = regex_replace_directory(
    pattern=r"《([^》]+)》",
    replacement=r"<title>《\\1》</title>",
    input_dir=Path("taiping_yulan_xml"),
    output_root=Path("outputs/chapter-05"),
    run_name="titles-demo",
)
"""
    )

    nb["cells"][4] = markdown_cell(
        """Maintenant, comptons le nombre de titres que vous venez de baliser avec le dossier produit ci-dessus :"""
    )

    nb["cells"][5] = code_cell(
        """from __future__ import annotations

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


def count_titles_in_directory(
    input_dir: Path,
    output_dir: Path = Path("outputs/chapter-06"),
) -> list[dict[str, object]]:
    xml_files = sorted(input_dir.glob("*.xml"))
    if not xml_files:
        raise FileNotFoundError(f"No XML files found in {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)
    rows = [count_titles(path) for path in xml_files]
    total = sum(int(row["title_count"]) for row in rows)

    with (output_dir / "title_counts.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["file", "title_count"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Files analysed: {len(rows)}")
    print(f"Total title elements: {total}")
    print(f"Results: {output_dir}")
    return rows


title_rows = count_titles_in_directory(output_dir, Path("outputs/chapter-06/titles-demo"))
title_rows[:5]
"""
    )

    NOTEBOOK.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"updated {NOTEBOOK}")


if __name__ == "__main__":
    main()
