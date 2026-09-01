"""Notebook analyses for chapter 8 — disambiguated entities."""

from __future__ import annotations

import re
import sqlite3
import sys
from collections import Counter
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

import pandas as pd

NAME_TAGS = {"persName", "placeName", "orgName", "name", "title"}


def setup_scripts_path() -> None:
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


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def text_of(element: ET.Element) -> str:
    return "".join(element.itertext()).strip()


def parse_year(value: str | None) -> float | None:
    """Turn TEI @when or ISO-like strings into a numeric year (BCE negative)."""
    if not value:
        return None
    value = value.strip()
    match = re.match(r"^(-?\d{1,4})", value)
    if match:
        return float(match.group(1))
    return None


def _data_candidates() -> tuple[Path, ...]:
    return (
        Path("data"),
        Path("../data"),
        Path("../../data"),
        Path("../../../data"),
    )


def resolve_entities_path(xml_path: Path | None = None) -> Path | None:
    """Find the LJB SQLite entity database next to the TEI file or in data/."""
    candidates: list[Path] = []
    if xml_path is not None:
        candidates.append(xml_path.parent / "entities.sqlite")
    for base in _data_candidates():
        candidates.append(base / "entities.sqlite")
    for path in candidates:
        if path.is_file():
            return path
    return None


def load_root(xml_path: Path) -> ET.Element:
    return ET.parse(xml_path).getroot()


def iter_name_elements(root: ET.Element):
    for element in root.iter():
        if local_name(element.tag) in NAME_TAGS:
            yield element



def _build_parent_map(root: ET.Element) -> dict[ET.Element, ET.Element]:
    parent_map: dict[ET.Element, ET.Element] = {}
    for parent in root.iter():
        for child in parent:
            parent_map[child] = parent
    return parent_map


def _fix_load_entity_registry_birth_death(element: ET.Element) -> tuple[float | None, float | None]:
    birth = death = None
    for child in element:
        ln = local_name(child.tag)
        if ln == "birth":
            birth = parse_year(child.get("when"))
        elif ln == "death":
            death = parse_year(child.get("when"))
    return birth, death


def mention_year_with_map(
    element: ET.Element, parent_map: dict[ET.Element, ET.Element]
) -> float | None:
    year = parse_year(element.get("when"))
    if year is not None:
        return year
    for child in element:
        if local_name(child.tag) == "date":
            year = parse_year(child.get("when"))
            if year is not None:
                return year
    current: ET.Element | None = element
    for _ in range(10):
        current = parent_map.get(current) if current is not None else None
        if current is None:
            break
        year = parse_year(current.get("when"))
        if year is not None:
            return year
    return None


def all_name_records(xml_path: Path) -> list[dict[str, Any]]:
    root = load_root(xml_path)
    parent_map = _build_parent_map(root)
    rows: list[dict[str, Any]] = []
    for element in iter_name_elements(root):
        tag = local_name(element.tag)
        rows.append(
            {
                "tag": tag,
                "key": element.get("key") or "",
                "surface_form": text_of(element),
                "ref": element.get("ref", ""),
                "when": element.get("when", ""),
                "mention_year": mention_year_with_map(element, parent_map),
                "has_key": bool(element.get("key")),
            }
        )
    return rows


def keyed_mention_rows(xml_path: Path) -> list[dict[str, Any]]:
    return [row for row in all_name_records(xml_path) if row["key"]]


def leakage_summary(xml_path: Path) -> pd.DataFrame:
    """Counts keyed vs unkeyed mentions per tag."""
    rows = all_name_records(xml_path)
    if not rows:
        return pd.DataFrame(columns=["tag", "avec_key", "sans_key", "total", "pct_key"])
    df = pd.DataFrame(rows)
    grouped = (
        df.groupby("tag")
        .agg(
            avec_key=("has_key", "sum"),
            total=("has_key", "count"),
        )
        .reset_index()
    )
    grouped["sans_key"] = grouped["total"] - grouped["avec_key"]
    grouped["pct_key"] = (100 * grouped["avec_key"] / grouped["total"]).round(1)
    return grouped.sort_values("sans_key", ascending=False)


def leakage_inconsistent_surfaces(xml_path: Path, top_n: int = 15) -> pd.DataFrame:
    """Surface forms that appear both with and without @key."""
    rows = all_name_records(xml_path)
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    keyed = set(df.loc[df["has_key"], "surface_form"])
    unkeyed = set(df.loc[~df["has_key"], "surface_form"])
    both = sorted(keyed & unkeyed)
    records = []
    for surface in both[:top_n]:
        sub = df[df["surface_form"] == surface]
        records.append(
            {
                "surface_form": surface,
                "avec_key": int(sub["has_key"].sum()),
                "sans_key": int((~sub["has_key"]).sum()),
            }
        )
    return pd.DataFrame(records)


def load_entity_registry(entities_path: Path) -> pd.DataFrame:
    """Load LJB entities from SQLite into a flat registry."""
    return load_entity_registry_clean(entities_path)


def load_entity_registry_clean(entities_path: Path) -> pd.DataFrame:
    records: list[dict[str, Any]] = []
    with sqlite3.connect(entities_path) as connection:
        entities = connection.execute(
            "SELECT id, kind, description FROM entities WHERE deleted_at IS NULL"
        ).fetchall()
        names = connection.execute(
            "SELECT entity_id, text FROM entity_names "
            "WHERE status = 'active' ORDER BY is_primary DESC, id"
        ).fetchall()
        dates = connection.execute(
            "SELECT entity_id, date_kind, start_year FROM entity_dates "
            "WHERE status = 'active' AND date_kind IN ('birth', 'death') "
            "ORDER BY id"
        ).fetchall()

    names_by_id: dict[str, list[str]] = {}
    for entity_id, name in names:
        names_by_id.setdefault(entity_id, []).append(name)
    dates_by_id: dict[str, dict[str, float | None]] = {}
    for entity_id, date_kind, year in dates:
        dates_by_id.setdefault(entity_id, {})[date_kind] = float(year) if year is not None else None

    for key, kind, description in entities:
        entity_names = names_by_id.get(key, [])
        entity_dates = dates_by_id.get(key, {})
        records.append(
            {
                "key": key,
                "entity_type": kind,
                "label": entity_names[0] if entity_names else (description or key),
                "birth_year": entity_dates.get("birth"),
                "death_year": entity_dates.get("death"),
                "alt_names": "; ".join(entity_names[1:]),
            }
        )

    if not records:
        return pd.DataFrame(
            columns=["key", "entity_type", "label", "birth_year", "death_year", "alt_names"]
        )
    return pd.DataFrame(records)


def form_counts_string(rows: list[dict[str, Any]], key: str) -> str:
    counter = Counter(r["surface_form"] for r in rows if r["key"] == key)
    return "; ".join(f"{form} ({n})" for form, n in counter.most_common())


def person_registry_table(
    xml_path: Path, entities_path: Path, entity_type: str = "person"
) -> pd.DataFrame:
    keyed = keyed_mention_rows(xml_path)
    registry = load_entity_registry_clean(entities_path)
    registry = registry[registry["entity_type"] == entity_type].copy()
    mention_counts = Counter()
    if entity_type == "person":
        mention_counts = Counter(r["key"] for r in keyed if r["tag"] == "persName")
    elif entity_type == "place":
        mention_counts = Counter(r["key"] for r in keyed if r["tag"] == "placeName")

    rows_out = []
    for _, ent in registry.iterrows():
        key = ent["key"]
        rows_out.append(
            {
                "key": key,
                "label": ent["label"],
                "mentions": mention_counts.get(key, 0),
                "formes_dans_le_texte": form_counts_string(keyed, key) if mention_counts.get(key, 0) else "",
                "birth_year": ent["birth_year"],
                "death_year": ent["death_year"],
                "alt_names_db": ent["alt_names"],
            }
        )
    df = pd.DataFrame(rows_out)
    if df.empty:
        return df
    return df.sort_values(["mentions", "label"], ascending=[False, True], ignore_index=True)


def person_mean_life_year(birth: Any, death: Any) -> float | None:
    """Midpoint of birth and death when both exist; otherwise the single date available."""
    has_b = birth is not None and pd.notna(birth)
    has_d = death is not None and pd.notna(death)
    if has_b and has_d:
        return (float(birth) + float(death)) / 2
    if has_b:
        return float(birth)
    if has_d:
        return float(death)
    return None


def tei_document_year(xml_path: Path) -> float | None:
    """Best-effort document date from TEI metadata (numeric year, BCE negative)."""
    root = load_root(xml_path)
    patterns = (
        ".//{*}teiHeader/{*}fileDesc/{*}sourceDesc//{*}date[@when]",
        ".//{*}teiHeader/{*}profileDesc/{*}creation/{*}date[@when]",
        ".//{*}teiHeader/{*}fileDesc//{*}date[@when]",
    )
    for pattern in patterns:
        for element in root.findall(pattern):
            year = parse_year(element.get("when"))
            if year is not None:
                return year
    return None


def person_life_timeline_table(xml_path: Path, entities_path: Path) -> pd.DataFrame:
    """Persons from SQLite with a biographical year and mention counts from the text."""
    base = person_registry_table(xml_path, entities_path, entity_type="person")
    if base.empty:
        return base
    base = base.copy()
    base["mean_life_year"] = base.apply(
        lambda row: person_mean_life_year(row["birth_year"], row["death_year"]),
        axis=1,
    )
    return base.sort_values(
        ["mean_life_year", "mentions"],
        ascending=[True, False],
        na_position="last",
        ignore_index=True,
    )


def plot_person_life_grouping(
    life_df: pd.DataFrame,
    document_year: float | None = None,
    *,
    figsize: tuple[float, float] = (10, 5.5),
) -> "plt.Figure":
    """Scatter: biographical mean year vs mention count; vertical line = text metadata date."""
    import matplotlib.pyplot as plt

    subset = life_df.dropna(subset=["mean_life_year"])
    fig, ax = plt.subplots(figsize=figsize)
    if subset.empty:
        ax.text(
            0.5,
            0.5,
            "Aucune date biographique dans la base SQLite",
            ha="center",
            va="center",
        )
        ax.set_axis_off()
        return fig

    sizes = 36 + 18 * subset["mentions"].clip(upper=12)
    ax.scatter(
        subset["mean_life_year"],
        subset["mentions"],
        s=sizes,
        alpha=0.75,
        c="#2563eb",
        edgecolors="white",
        linewidths=0.5,
    )
    for _, row in subset.iterrows():
        ax.annotate(
            row["label"],
            (row["mean_life_year"], row["mentions"]),
            textcoords="offset points",
            xytext=(4, 4),
            fontsize=8,
        )
    if document_year is not None:
        ax.axvline(
            document_year,
            color="#dc2626",
            linestyle="--",
            linewidth=1.5,
            label=f"Date du texte ({document_year:g})",
        )
        ax.legend(loc="upper right")
    ax.set_xlabel("Position biographique (moyenne naissance–décès, ou date unique)")
    ax.set_ylabel("Mentions dans le texte (@key)")
    ax.set_title("Personnages dans le temps (d'après la base SQLite)")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig


def before_after_top_names(xml_path: Path, top_n: int = 10) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Compare persName counts by surface string vs by @key."""
    rows = all_name_records(xml_path)
    pers = [r for r in rows if r["tag"] == "persName"]
    by_surface = Counter(r["surface_form"] for r in pers)
    by_key = Counter(r["key"] for r in pers if r["key"])
    surface_df = pd.DataFrame(
        [{"surface_form": k, "mentions": v} for k, v in by_surface.most_common(top_n)]
    )
    key_df = pd.DataFrame([{"key": k, "mentions": v} for k, v in by_key.most_common(top_n)])
    return surface_df, key_df
