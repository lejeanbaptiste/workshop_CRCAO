#!/usr/bin/env python3
"""Replace chapter 5 notebook code with simpler workshop scripts."""

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
        """import glob
import os
import re
from bs4 import BeautifulSoup


input_dir = "taiping_yulan_xml"
output_dir = "outputs/chapter-05/titles-demo"
os.makedirs(output_dir, exist_ok=True)

# Remplacez ce motif par votre propre regex.
pattern = r"《([^》]+)》"
replacement = r"<title>《\\1》</title>"

for input_path in sorted(glob.glob(f"{input_dir}/*.xml")):
    with open(input_path, "r", encoding="utf-8") as f:
        xml = f.read()

    new_xml = re.sub(pattern, replacement, xml)

    # BeautifulSoup reparcourt le XML pour vérifier que le résultat reste lisible.
    soup = BeautifulSoup(new_xml, "xml")

    output_path = os.path.join(output_dir, os.path.basename(input_path))
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(str(soup))

print("Terminé :", output_dir)
"""
    )

    nb["cells"][4] = markdown_cell(
        "Maintenant, ouvrons chaque fichier de sortie et comptons le nombre d'éléments `<title>` :"
    )

    nb["cells"][5] = code_cell(
        """import glob
from bs4 import BeautifulSoup


counts = []

for path in sorted(glob.glob("outputs/chapter-05/titles-demo/*.xml")):
    with open(path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "xml")

    title_count = len(soup.find_all("title"))
    counts.append((path, title_count))
    print(path, title_count)

counts[:5]
"""
    )

    NOTEBOOK.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"updated {NOTEBOOK}")


if __name__ == "__main__":
    main()
