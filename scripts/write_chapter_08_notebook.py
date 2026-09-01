#!/usr/bin/env python3
"""Write chapter 8 course notebook."""

import json
from pathlib import Path

NOTEBOOK = Path("notebooks/course/part-1-les-bases/08_exploiter_entites.ipynb")


def md(source: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": source.splitlines(keepends=True)}


def code(source: str, *, hidden: bool = False) -> dict:
    meta = {"jupyter": {"source_hidden": True}} if hidden else {}
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": meta,
        "outputs": [],
        "source": source.splitlines(keepends=True),
    }


cells = [
    md(
        """# 8. Exploitation des données désambiguïsées

Au chapitre 7, vous avez relié des formes de surface à des entités stables (`@key`) et à votre base SQLite. Ce chapitre montre **pourquoi** ce travail compte : d'abord en vérifiant que rien n'a « fuité » (mentions balisées mais pas désambiguïsées), puis en produisant des tableaux et graphiques impossibles à obtenir en comptant seulement des chaînes de caractères.

Comme au chapitre 6, tout s'exécute dans cette page JupyterLite. Téléversez votre transcription XML balisée et votre base SQLite ci-dessous.

Les résultats doivent toujours pouvoir être **ramenés aux passages sources** dans l'éditeur : ce sont des outils de contrôle et d'argumentation, pas une vérité automatique.
"""
    ),
    code(
        """%pip install -q --disable-pip-version-check ipywidgets lxml pandas matplotlib tqdm

from pathlib import Path
import sys

scripts_dir = next(
    candidate
    for candidate in (Path("scripts"), Path("../scripts"), Path("../../scripts"), Path("../../../scripts"))
    if candidate.exists()
)
sys.path.insert(0, str(scripts_dir.resolve()))

from xml_upload import show_upload

show_upload()
""",
        hidden=True,
    ),
    code(
        """from chapter_08_analyses import resolve_entities_path, setup_scripts_path
from xml_upload import get_xml_path

setup_scripts_path()

XML_PATH = get_xml_path()
ENTITIES_PATH = resolve_entities_path(XML_PATH)

print(f"Texte : {XML_PATH}")
print(f"Base d'entités : {ENTITIES_PATH or '(non trouvée — certaines sections seront ignorées)'}")
""",
    ),
    md(
        """## Exemple 1 : Contrôle des fuites (« leakage »)

Avant toute statistique, vérifiez la **couverture** de la désambiguïsation : pour chaque type de balise (`persName`, `placeName`, …), combien de mentions ont un `@key` et combien n'en ont pas ?

Objectif : un tableau de bord honnête. S'il reste des mentions sans clé, vos graphiques suivants ne représentent qu'une **partie** du texte.
"""
    ),
    code(
        """from IPython.display import display

from chapter_08_analyses import leakage_inconsistent_surfaces, leakage_summary

display(leakage_summary(XML_PATH))

inconsistent = leakage_inconsistent_surfaces(XML_PATH)
if inconsistent.empty:
    print("Aucune forme à la fois avec et sans @key.")
else:
    print("Formes à corriger (même chaîne, parfois désambiguïsée, parfois non) :")
    display(inconsistent)
""",
    ),
    md(
        """## Exemple 2 : Avant / après désambiguïsation

Comparez le **top des chaînes** (`persName` bruts) au **top des personnages** (regroupés par `@key`). Sans clé, les homonymes et les variantes (nom complet vs prénom seul) faussent le classement.
"""
    ),
    code(
        """from IPython.display import display

from chapter_08_analyses import before_after_top_names

by_surface, by_key = before_after_top_names(XML_PATH)

print("Top des formes de surface (persName)")
display(by_surface)

print("Top des personnages (par @key)")
display(by_key)
""",
    ),
    md(
        """## Exemple 3 : Personnages dans la base et dans le texte

On croise la **base SQLite** (toutes les personnes que vous avez préparées) avec les mentions **@key** du texte. La colonne `formes_dans_le_texte` liste chaque variante et son effectif. Les lignes à **0 mention** ne sont pas une erreur : elles signalent des entités prêtes pour le projet mais absentes de ce fichier (ou pas encore citées).
"""
    ),
    code(
        """from IPython.display import display

from chapter_08_analyses import person_registry_table

if ENTITIES_PATH is None:
    print("Ajoutez la base SQLite dans data/ pour afficher ce tableau.")
else:
    registry_df = person_registry_table(XML_PATH, ENTITIES_PATH, entity_type="person")
    display(registry_df)
""",
    ),
    md(
        """## Exemple 4 : Personnages dans le temps

Pour chaque personne dans la **base SQLite**, on calcule une **position biographique** : la moyenne des années de naissance et de décès lorsque les deux sont connues, sinon l'unique date disponible. L'axe horizontal du graphique regroupe ainsi les personnages dans le temps ; l'axe vertical compte leurs mentions désambiguïsées dans **votre** texte.

La **ligne verticale** indique la date du document, lue dans les métadonnées TEI (`teiHeader`, balises `<date when="…">`). Elle permet de situer d'un coup d'œil si le texte traite surtout de contemporains, d'ancêtres, etc. Si aucune date n'est trouvée dans l'en-tête, le graphique s'affiche sans cette ligne — vérifiez alors le balisage des métadonnées dans l'éditeur.
"""
    ),
    code(
        """from IPython.display import display

from chapter_08_analyses import (
    person_life_timeline_table,
    plot_person_life_grouping,
    tei_document_year,
)

if ENTITIES_PATH is None:
    print("Ajoutez la base SQLite dans data/ pour cette analyse.")
else:
    life_df = person_life_timeline_table(XML_PATH, ENTITIES_PATH)
    display(life_df[["label", "birth_year", "death_year", "mean_life_year", "mentions"]])

    doc_year = tei_document_year(XML_PATH)
    if doc_year is None:
        print("Aucune date de document trouvée dans teiHeader — ligne verticale omise.")
    else:
        print(f"Date du texte (métadonnées) : {doc_year:g}")

    plot_person_life_grouping(life_df, document_year=doc_year)
""",
    ),
    md(
        """## Prolongements

- **Lieux** : reprenez `person_registry_table(..., entity_type=\"place\")` ; les coordonnées peuvent être exportées en KML pour Google Earth.
- **Site de lecture** : votre TEI + base SQLite suffisent pour générer une page HTML (plan du texte à gauche, liens `@ref` vers les autorités) — voir le chapitre 10 pour l'autonomie sur ce type de livrable.
- **Ligne de commande** : `python scripts/chapter_08_entities.py votre-texte.xml --entities entities.sqlite --output-dir outputs/chapter-08` exporte les CSV.

## Exercices

- [ ] Interpréter votre tableau de fuites : quel type de balise reste le moins désambiguïsé ?
- [ ] Propager `@key` pour une forme listée comme incohérente, puis relancer l'exemple 1.
- [ ] Expliquer une ligne à 0 mention dans le tableau registry (personnage absent ? autre volume ?).
- [ ] Comparer la ligne « date du texte » aux nuages de points : le corpus est-il cohérent chronologiquement ?
- [ ] Repérer un personnage loin du groupe principal : homonyme, mauvaise clé, ou intérêt historique réel ?
- [ ] Imaginer une colonne ou un filtre utile pour **votre** question de recherche (rôle, certitude `@cert`, dynastie, etc.).
"""
    ),
]

nb = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "pygments_lexer": "ipython3"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

NOTEBOOK.write_text(json.dumps(nb, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"wrote {NOTEBOOK}")
