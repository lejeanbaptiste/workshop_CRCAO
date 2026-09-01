"""Notebook analyses for chapter 6 — tagged XML exploration."""

from __future__ import annotations

import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from bs4 import BeautifulSoup
from matplotlib import font_manager


def setup_scripts_path() -> None:
    """Make the scripts/ folder importable from course notebooks."""
    scripts_dir = next(
        candidate
        for candidate in (
            Path("scripts"),
            Path("../scripts"),
            Path("../../scripts"),
            Path("../../../scripts"),
        )
        if candidate.exists()
    )
    resolved = str(scripts_dir.resolve())
    if resolved not in sys.path:
        sys.path.insert(0, resolved)


def load_soup(xml_path: Path) -> BeautifulSoup:
    with xml_path.open(encoding="utf-8") as handle:
        return BeautifulSoup(handle.read(), "xml")


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def configure_cjk_font() -> str | None:
    """Select an installed font with Chinese glyphs when one is available."""
    preferred = (
        "Noto Sans CJK SC",
        "Noto Sans CJK TC",
        "PingFang SC",
        "PingFang TC",
        "Songti SC",
        "Microsoft YaHei",
        "Arial Unicode MS",
        "WenQuanYi Zen Hei",
    )
    available = {font.name for font in font_manager.fontManager.ttflist}
    for name in preferred:
        if name in available:
            plt.rcParams["font.family"] = name
            plt.rcParams["font.sans-serif"] = [name]
            return name
    return None


def tagged_records(soup: BeautifulSoup) -> pd.DataFrame:
    """Collect every tagged element inside a paragraph (XPath: //p//*)."""
    rows: list[dict[str, object]] = []
    for paragraph_number, paragraph in enumerate(soup.find_all("p"), start=1):
        for node in paragraph.find_all(True):
            value = node.get_text(strip=True)
            if not value:
                continue
            rows.append(
                {
                    "paragraph": paragraph_number,
                    "tag": local_name(node.name),
                    "value": value,
                }
            )
    return pd.DataFrame(rows)


def frequent_strings_table(soup: BeautifulSoup, min_count: int = 4) -> pd.DataFrame:
    """Return tag/value counts kept only when count is greater than min_count."""
    tagged_df = tagged_records(soup)
    if tagged_df.empty:
        return pd.DataFrame(columns=["tag", "value", "count"])

    counts = (
        tagged_df.groupby(["tag", "value"])
        .size()
        .reset_index(name="count")
        .query("count > @min_count")
        .sort_values(["count", "tag", "value"], ascending=[False, True, True])
        .reset_index(drop=True)
    )
    return counts


def plot_tags_by_paragraph(soup: BeautifulSoup) -> None:
    """Bar chart of //p//* tag counts from the first paragraph to the last."""
    paragraph_counts = [
        {"paragraph": index, "tag_count": len(paragraph.find_all(True))}
        for index, paragraph in enumerate(soup.find_all("p"), start=1)
    ]
    paragraph_df = pd.DataFrame(paragraph_counts)

    if paragraph_df.empty:
        print("Aucun paragraphe <p> trouvé.")
        return

    plt.figure(figsize=(10, 4.5))
    plt.bar(paragraph_df["paragraph"], paragraph_df["tag_count"])
    plt.xlabel("Paragraphe")
    plt.ylabel("Nombre de balises (//p//*)")
    plt.title("Balises par paragraphe, du début à la fin")
    plt.tight_layout()
    plt.show()


def plot_cooccurrence_network(
    soup: BeautifulSoup,
    min_count: int = 4,
    max_nodes: int = 40,
) -> None:
    """Network of unique strings that appear in the same paragraph."""
    tagged_df = tagged_records(soup)
    if tagged_df.empty:
        print("Aucune balise trouvée dans les paragraphes.")
        return

    frequent_values = set(
        tagged_df.groupby("value")
        .size()
        .loc[lambda counts: counts > min_count]
        .index
    )
    if len(frequent_values) < 2:
        print("Pas assez de formes fréquentes pour tracer un réseau.")
        return

    edge_weights: Counter[tuple[str, str]] = Counter()
    for _, group in tagged_df.groupby("paragraph"):
        values = sorted(set(group["value"]) & frequent_values)
        for left, right in combinations(values, 2):
            edge_weights[(left, right)] += 1

    graph = nx.Graph()
    for (left, right), weight in edge_weights.items():
        graph.add_edge(left, right, weight=weight)

    if graph.number_of_nodes() == 0:
        print("Aucune cooccurrence dans un même paragraphe.")
        return

    if configure_cjk_font() is None:
        print(
            "Aucune police CJK installée : les étiquettes chinoises peuvent "
            "ne pas s'afficher. Installez Noto Sans CJK ou PingFang."
        )

    if graph.number_of_nodes() > max_nodes:
        keep_nodes = sorted(
            graph.nodes,
            key=lambda node: graph.degree(node, weight="weight"),
            reverse=True,
        )[:max_nodes]
        graph = graph.subgraph(keep_nodes).copy()

    plt.figure(figsize=(11, 8))
    positions = nx.spring_layout(graph, seed=0, weight="weight")
    edge_widths = [1 + graph[u][v]["weight"] for u, v in graph.edges]
    nx.draw_networkx_edges(graph, positions, width=edge_widths, alpha=0.35)
    nx.draw_networkx_nodes(graph, positions, node_size=700, alpha=0.9)
    labels = {node: node if len(node) <= 10 else f"{node[:10]}…" for node in graph.nodes}
    nx.draw_networkx_labels(graph, positions, labels=labels, font_size=8)
    plt.title("Chaînes uniques trouvées dans le même paragraphe")
    plt.axis("off")
    plt.tight_layout()
    plt.show()


def find_titles_corpus_dir() -> Path:
    """Locate the Taiping yulan corpus tagged in chapter 5."""
    candidates = [
        Path("outputs/chapter-05/titles-demo"),
        Path("../outputs/chapter-05/titles-demo"),
        Path("../../outputs/chapter-05/titles-demo"),
        Path("../../../outputs/chapter-05/titles-demo"),
        Path("data/taiping-yulan-full"),
        Path("../data/taiping-yulan-full"),
        Path("../../data/taiping-yulan-full"),
        Path("../../../data/taiping-yulan-full"),
        Path("data/taiping-yulan-titles"),
        Path("../data/taiping-yulan-titles"),
        Path("../../data/taiping-yulan-titles"),
        Path("../../../data/taiping-yulan-titles"),
    ]
    for candidate in candidates:
        if candidate.exists() and any(candidate.glob("*.xml")):
            return candidate
    raise FileNotFoundError(
        "Corpus introuvable. Exécutez d'abord le chapitre 5, "
        "ou placez des fichiers XML dans data/taiping-yulan-titles/."
    )


def taiping_title_counts(corpus_dir: Path | None = None) -> pd.DataFrame:
    """Table of the most cited titles in the chapter 5 Taiping yulan corpus."""
    corpus_path = corpus_dir or find_titles_corpus_dir()
    rows: list[dict[str, str]] = []

    for xml_path in sorted(corpus_path.glob("*.xml")):
        soup = load_soup(xml_path)
        for title in soup.find_all("title"):
            value = title.get_text(strip=True)
            if value:
                rows.append({"title": value})

    if not rows:
        return pd.DataFrame(columns=["title", "count"])

    return (
        pd.DataFrame(rows)
        .groupby("title")
        .size()
        .reset_index(name="count")
        .sort_values(["count", "title"], ascending=[False, True])
        .reset_index(drop=True)
    )
