#!/usr/bin/env python3
"""Apply a user-supplied regex substitution to each XML volume.

The script reads every `.xml` file in an input directory, applies
`re.sub(pattern, replacement, text, flags=flags)` to the file contents,
and writes the result to a parallel output folder.

By default, each regex run gets its own output subdirectory so different
users/patterns do not overwrite one another.
"""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path


def run_id(pattern: str, replacement: str, flags: int) -> str:
    digest = hashlib.sha1(f"{pattern}\0{replacement}\0{flags}".encode("utf-8")).hexdigest()
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
            raise SystemExit(f"Unknown regex flag: {name}")
        flags |= flag_map[key]
    return flags


def process_file(src: Path, dst: Path, pattern: re.Pattern[str], replacement: str) -> int:
    text = src.read_text(encoding="utf-8")
    updated, count = pattern.subn(replacement, text)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(updated, encoding="utf-8")
    return count


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pattern", help="Regex pattern to apply")
    parser.add_argument("replacement", help="Replacement text for re.sub")
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path("taiping_yulan_xml"),
        help="Directory containing source XML files",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path("outputs/chapter-05"),
        help="Root directory for transformed copies",
    )
    parser.add_argument(
        "--flag",
        action="append",
        default=[],
        help="Regex flag to enable: ignorecase, multiline, dotall, verbose",
    )
    parser.add_argument(
        "--run-name",
        default="",
        help="Optional label for the run; defaults to a hash of pattern/replacement/flags",
    )
    args = parser.parse_args()

    flags = compile_flags(args.flag)
    compiled = re.compile(args.pattern, flags)
    label = args.run_name.strip() or run_id(args.pattern, args.replacement, flags)
    output_dir = args.output_root / label
    output_dir.mkdir(parents=True, exist_ok=True)

    source_files = sorted(args.input_dir.glob("*.xml"))
    if not source_files:
        raise SystemExit(f"No XML files found in {args.input_dir}")

    changed_total = 0
    copied_total = 0
    for src in source_files:
        dst = output_dir / src.name
        changed_total += process_file(src, dst, compiled, args.replacement)
        copied_total += 1

    print(f"Files processed: {copied_total}")
    print(f"Total substitutions: {changed_total}")
    print(f"Output directory: {output_dir}")


if __name__ == "__main__":
    main()
