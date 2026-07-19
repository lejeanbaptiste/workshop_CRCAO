#!/usr/bin/env python3
"""Replace markdown task lists in course notebooks with ipywidgets checklists."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path


ROOT = Path("Workshop/notebooks/course")


HELPER_SOURCE = [
    "import ipywidgets as widgets\n",
    "from IPython.display import display\n",
    "\n",
    "\n",
    "def render_checklist(sections):\n",
    "    blocks = []\n",
    "    for title, items in sections:\n",
    "        blocks.append(widgets.HTML(f\"<h4 style='margin:0.6em 0 0.3em 0'>{title}</h4>\"))\n",
    "        for item in items:\n",
    "            blocks.append(widgets.Checkbox(value=False, description=item, indent=False))\n",
    "    display(widgets.VBox(blocks))\n",
]


def code_cell(source: list[str]) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source,
    }


def widget_cell(sections: list[tuple[str, list[str]]]) -> dict:
    source = [
        "render_checklist([\n",
    ]
    for title, items in sections:
        source.append(f"    ({title!r}, [\n")
        for item in items:
            source.append(f"        {item!r},\n")
        source.append("    ]),\n")
    source.append("])\n")
    return code_cell(source)


def replace_text(text: str, old: str, new: str) -> str:
    if old not in text:
        raise ValueError(f"Expected snippet not found: {old[:80]!r}")
    return text.replace(old, new)


def update_00(nb: dict) -> dict:
    text = "".join(nb["cells"][0]["source"])
    replacements = {
        "## Matériel\n\n- [ ] Ordinateur portable\n- [ ] Smartphone\n": "## Matériel\n\nVoir la checklist interactive ci-dessous.\n",
        "## Compétences préalables\n\n- [ ] Être à l'aise dans un traitement de texte, comme Word\n- [ ] Télécharger et installer un logiciel\n- [ ] Créer un compte en ligne\n- [ ] Gérer ses mots de passe\n": "## Compétences préalables\n\nVoir la checklist interactive ci-dessous.\n",
        "Ce workshop part de votre projet, pas d'un exemple abstrait. Venez avec :\n\n- [ ] 2 à 5 transcriptions du type de source que vous souhaitez étudier\n- [ ] dont au moins une contenant des noms de personnes, de lieux, d'institutions ou des titres d'ouvrage\n": "Ce workshop part de votre projet, pas d'un exemple abstrait. Venez avec les éléments indiqués dans la checklist interactive ci-dessous.\n",
        "## Questions\n\n- [ ] Notez quelques questions de recherche concrètes : que voudriez-vous regrouper, compter, comparer, retrouver ou fabriquer ? Nous ne visons pas la magie technologique, mais de la **recherche scientifique**.\n": "## Questions\n\nNotez quelques questions de recherche concrètes : que voudriez-vous regrouper, compter, comparer, retrouver ou fabriquer ? Nous ne visons pas la magie technologique, mais de la **recherche scientifique**. La checklist interactive ci-dessous sert simplement à vérifier que c'est fait.\n",
        "## Listes\n\n- [ ] _Si vous en avez_, apportez aussi toute liste de noms ou de termes d'une catégorie précise, par exemple une liste de 1 000 personnages en pinyin et en chinois avec dates de naissance et de décès.\n": "## Listes\n\nSi vous en avez, apportez aussi toute liste de noms ou de termes d'une catégorie précise, par exemple une liste de 1 000 personnages en pinyin et en chinois avec dates de naissance et de décès.\n",
        "Vous allez créer un **compte [GitHub](https://github.com/)** pour trois raisons simples : avoir une présence dans cet espace, découvrir une autre manière de stocker et partager du travail, et activer une fonction importante de l'éditeur XML.\n\n- [ ] Créez un compte [ici](https://github.com/)\n- [ ] Installez l'application GitHub sur votre téléphone\n- [ ] [Activez l'authentification à deux facteurs](https://docs.github.com/fr/authentication/securing-your-account-with-two-factor-authentication-2fa/configuring-two-factor-authentication) afin de valider rapidement vos connexions\n": "Vous allez créer un **compte [GitHub](https://github.com/)** pour trois raisons simples : avoir une présence dans cet espace, découvrir une autre manière de stocker et partager du travail, et activer une fonction importante de l'éditeur XML. Les étapes à vérifier se trouvent dans la checklist interactive ci-dessous.\n",
        "Vous aurez aussi besoin d'un **éditeur XML** avec interface graphique. Il n'existe pas d'outil parfait, mais certains petits projets sur GitHub sont parfois plus utiles que des solutions commerciales plus lourdes.\n\n- [ ] Allez sur [ce dépôt](https://github.com/lejeanbaptiste/lejeanbaptiste)\n- [ ] Lisez rapidement la description pour vérifier qu'il s'agit bien d'un éditeur XML\n- [ ] Cliquez sur l'étiquette `v0.0...` sous `Releases` pour accéder aux installateurs\n- [ ] Téléchargez le paquet correspondant à votre système d'exploitation (Linux/macOS/Windows) et à votre puce (AMD/ARM)[^1]\n- [ ] Installez le paquet\n": "Vous aurez aussi besoin d'un **éditeur XML** avec interface graphique. Il n'existe pas d'outil parfait, mais certains petits projets sur GitHub sont parfois plus utiles que des solutions commerciales plus lourdes. Les étapes sont regroupées dans la checklist interactive ci-dessous.\n",
        "Une fois l'éditeur installé, ouvrez-le et paramétrez-le :\n\n- [ ] Votre nom, pour l'encoder dans les métadonnées des textes que vous éditez\n- [ ] Le dossier racine, où seront stockées votre base de données et les ressources téléchargées\n- [ ] L'API IA :\n": "Une fois l'éditeur installé, ouvrez-le et paramétrez-le. Les éléments à vérifier se trouvent dans la checklist interactive ci-dessous :\n",
    }
    for old, new in replacements.items():
        text = replace_text(text, old, new)
    nb["cells"][0]["source"] = text.splitlines(keepends=True)
    nb["cells"].insert(1, widget_cell([
        ("Matériel", ["Ordinateur portable", "Smartphone"]),
        ("Compétences préalables", [
            "Être à l'aise dans un traitement de texte, comme Word",
            "Télécharger et installer un logiciel",
            "Créer un compte en ligne",
            "Gérer ses mots de passe",
        ]),
        ("Textes", [
            "Apporter 2 à 5 transcriptions du type de source que vous souhaitez étudier",
            "Avoir au moins une transcription contenant des noms de personnes, de lieux, d'institutions ou des titres d'ouvrage",
        ]),
        ("Questions", [
            "Noter quelques questions de recherche concrètes à explorer pendant le workshop",
        ]),
        ("Listes", [
            "Apporter, si vous en avez, une liste de noms ou de termes d'une catégorie précise",
        ]),
        ("Comptes GitHub", [
            "Créer un compte GitHub",
            "Installer l'application GitHub sur votre téléphone",
            "Activer l'authentification à deux facteurs",
        ]),
        ("Éditeur XML", [
            "Ouvrir le dépôt de l'éditeur XML",
            "Vérifier rapidement qu'il s'agit bien d'un éditeur XML",
            "Ouvrir la page des Releases",
            "Télécharger le paquet adapté à votre système et à votre puce",
            "Installer le paquet",
        ]),
        ("Paramétrage", [
            "Renseigner votre nom",
            "Définir le dossier racine",
            "Configurer l'API IA si nécessaire",
        ]),
    ]))
    nb["cells"].insert(1, code_cell(deepcopy(HELPER_SOURCE)))
    return nb


def update_03(nb: dict) -> dict:
    text = "".join(nb["cells"][0]["source"])
    old = """## Exercices\n\n**Gestes de base**\n\n- [ ] Créez un document\n- [ ] Ouvrez et fermez des documents\n- [ ] Copiez-collez un texte dedans\n- [ ] Importez l'une de vos propres sources primaires\n- [ ] Parcourez les documents dans le panneau `Navigator`\n- [ ] Entrez le titre et d'autres informations dans `Document metadata`\n- [ ] Ajoutez quelques notes sur plusieurs paragraphes et retrouvez-les\n- [ ] Ouvrez `Find and replace` (panneau de gauche, `ctrl/cmd+f`) pour chercher des mots-clés dans la source primaire et dans vos traductions\n\n**Intégration**\n\n- [ ] Traduisez un petit paragraphe de l'une de vos sources en ajoutant des notes de bas de page et quelques références Zotero ou Juris-M\n"""
    new = """## Exercices\n\nUtilisez la checklist interactive ci-dessous.\n"""
    text = replace_text(text, old, new)
    nb["cells"][0]["source"] = text.splitlines(keepends=True)
    nb["cells"].insert(1, code_cell(deepcopy(HELPER_SOURCE)))
    nb["cells"].insert(2, widget_cell([
        ("Gestes de base", [
            "Créer un document",
            "Ouvrir et fermer des documents",
            "Copier-coller un texte dedans",
            "Importer l'une de vos propres sources primaires",
            "Parcourir les documents dans le panneau Navigator",
            "Entrer le titre et d'autres informations dans Document metadata",
            "Ajouter quelques notes sur plusieurs paragraphes et les retrouver",
            "Ouvrir Find and replace pour chercher des mots-clés dans la source primaire et dans vos traductions",
        ]),
        ("Intégration", [
            "Traduire un petit paragraphe de l'une de vos sources avec notes de bas de page et références Zotero ou Juris-M",
        ]),
    ]))
    return nb


def update_04(nb: dict) -> dict:
    text = "".join(nb["cells"][0]["source"])
    old = """## Exercices et observations\n\n- [ ] Balisez un toponyme (`placeName`), un titre d'ouvrage (`title`), un titre de fonction (`roleName`) ou une organisation (`org`) à proximité d'un nom de personne\n- [ ] Changez la surbrillance de l'un indépendamment de l'autre pour créer un contraste entre catégories\n\nNotre éditeur XML offre trois présentations d'un même fichier :\n"""
    new = """## Exercices et observations\n\nCommencez par la checklist interactive ci-dessous.\n\nNotre éditeur XML offre trois présentations d'un même fichier :\n"""
    text = replace_text(text, old, new)
    old2 = """- [ ] Retrouver un même élément balisé dans les trois modes\n- [ ] Dans le mode `Source`, essayez de changer un `persName` en `placeName` et observez ce qui se passe\n- [ ] Observez le résultat dans le mode `Visual`\n- [ ] Sauvegardez le document et essayez de casser volontairement le XML dans le mode `Source`\n"""
    new2 = "Poursuivez ensuite avec la deuxième checklist interactive.\n"
    text = replace_text(text, old2, new2)
    nb["cells"][0]["source"] = text.splitlines(keepends=True)
    nb["cells"].insert(1, code_cell(deepcopy(HELPER_SOURCE)))
    nb["cells"].insert(2, widget_cell([
        ("Balises et contraste", [
            "Baliser un toponyme, un titre d'ouvrage, un titre de fonction ou une organisation à proximité d'un nom de personne",
            "Changer la surbrillance d'une catégorie indépendamment de l'autre pour créer un contraste",
        ]),
    ]))
    nb["cells"].insert(3, widget_cell([
        ("Modes d'affichage", [
            "Retrouver un même élément balisé dans les trois modes",
            "Dans Source, changer un persName en placeName et observer le résultat",
            "Observer le résultat dans le mode Visual",
            "Sauvegarder puis casser volontairement le XML dans le mode Source",
        ]),
    ]))
    return nb


def update_05(nb: dict) -> dict:
    text0 = "".join(nb["cells"][0]["source"])
    replacements = {
        "## Entraînement psychologique\n\n- [ ] Sélectionnez une chaîne de caractères qui n'est absolument pas un nom de personne\n- [ ] Balisez-la en `persName`\n- [ ] Ouvrez le panneau `Attributes`, ajoutez une certitude (`cert`) et sauvegardez le document\n- [ ] Donnez à l'instructeur une description convaincante de la sérénité que vous devriez ressentir face à l'imperfection\n": "## Entraînement psychologique\n\nUtilisez la checklist interactive ci-dessous.\n",
        "### 1. Copier-coller\n\nSi l'on balise la première occurrence de « Laetitia » comme `persName`, on peut copier le texte balisé puis le coller sur les autres occurrences, exactement comme dans Word. Oui.\n\n- [ ] Dans le mode `Visual`, copiez-collez un élément et observez que la copie porte bien la même surbrillance\n- [ ] Dans le mode `Source`, copiez-collez `<persName>NOM</persName>` et observez que les balises sont aussi reproduites\n": "### 1. Copier-coller\n\nSi l'on balise la première occurrence de « Laetitia » comme `persName`, on peut copier le texte balisé puis le coller sur les autres occurrences, exactement comme dans Word. Oui.\n\nUtilisez la checklist interactive ci-dessous.\n",
        "Dans `Source` :\n\n- [ ] Sélectionnez une chaîne de caractères\n- [ ] Appuyez sur `ctrl+f` ou `cmd+f` pour ouvrir `Find and replace`\n- [ ] Remplacez `NOM` par `<persName>NOM</persName>`\n\nDans `Visual` :\n\n- [ ] Sélectionnez une chaîne de caractères\n- [ ] Choisissez une balise\n- [ ] Appuyez sur `Maj.+Entrée` / `Shift+Enter`\n": "Dans `Source` et dans `Visual`, utilisez la checklist interactive ci-dessous pour suivre les étapes.\n",
        "C'est parfait pour les expressions régulières.\n\n- [ ] Copiez-collez le passage dans votre éditeur\n- [ ] Basculez en mode `Source`\n- [ ] Ouvrez `Find and replace`\n- [ ] Expérimentez avec des regex dans `Find` pour retrouver tous les titres d'ouvrage d'un coup\n- [ ] Essayez de les baliser en une seule opération, en capturant puis en reproduisant la partie variable\n- [ ] Notez le temps qu'il a fallu à l'ordinateur pour exécuter l'opération\n": "C'est parfait pour les expressions régulières. Suivez la checklist interactive ci-dessous.\n",
    }
    for old, new in replacements.items():
        text0 = replace_text(text0, old, new)
    nb["cells"][0]["source"] = text0.splitlines(keepends=True)

    text4 = "".join(nb["cells"][4]["source"])
    text4 = replace_text(
        text4,
        "Exercices :\n\n- [ ] Essayez les différentes options et les filtres dans `Auto-tagging`\n- [ ] Essayez de valider les candidats : `Entrée` pour cette occurrence, `Maj.+Entrée` pour toutes les occurrences, `Backspace` pour rejeter, `Maj.+Backspace` pour toutes les rejeter\n",
        "Exercices : utilisez la checklist interactive ci-dessous.\n",
    )
    text4 = replace_text(
        text4,
        "Exercices :\n\n- [ ] Importez un nouveau document non balisé\n- [ ] Essayez `AI suggest` dans `Auto-tagging`\n",
        "Exercices : utilisez la checklist interactive ci-dessous.\n",
    )
    nb["cells"][4]["source"] = text4.splitlines(keepends=True)

    nb["cells"].insert(1, code_cell(deepcopy(HELPER_SOURCE)))
    nb["cells"].insert(2, widget_cell([
        ("Entraînement psychologique", [
            "Sélectionner une chaîne qui n'est pas un nom de personne",
            "La baliser en persName",
            "Ajouter une certitude cert puis sauvegarder",
            "Décrire à l'instructeur la sérénité que vous devriez ressentir face à l'imperfection",
        ]),
        ("Copier-coller", [
            "Dans Visual, copier-coller un élément et vérifier que la surbrillance suit",
            "Dans Source, copier-coller <persName>NOM</persName> et vérifier que les balises sont reproduites",
        ]),
        ("Chercher et remplacer", [
            "Dans Source, sélectionner une chaîne de caractères",
            "Ouvrir Find and replace avec ctrl+f ou cmd+f",
            "Remplacer NOM par <persName>NOM</persName>",
            "Dans Visual, sélectionner une chaîne de caractères",
            "Choisir une balise",
            "Appuyer sur Maj.+Entrée / Shift+Enter",
        ]),
        ("Regex", [
            "Copier-coller le passage dans l'éditeur",
            "Basculer en mode Source",
            "Ouvrir Find and replace",
            "Expérimenter avec des regex dans Find pour retrouver tous les titres d'ouvrage d'un coup",
            "Essayer de baliser en une seule opération en capturant puis en reproduisant la partie variable",
            "Noter le temps qu'il a fallu à l'ordinateur pour exécuter l'opération",
        ]),
    ]))
    nb["cells"].insert(6, widget_cell([
        ("Auto-tagging", [
            "Essayer les différentes options et les filtres dans Auto-tagging",
            "Valider ou rejeter les candidats avec Entrée, Maj.+Entrée, Backspace et Maj.+Backspace",
        ]),
        ("IA", [
            "Importer un nouveau document non balisé",
            "Essayer AI suggest dans Auto-tagging",
        ]),
    ]))
    return nb


def main() -> None:
    updates = {
        "00_a_preparer.ipynb": update_00,
        "part-1-les-bases/03_preparer_traduire.ipynb": update_03,
        "part-1-les-bases/04_styles_surbrillance.ipynb": update_04,
        "part-1-les-bases/05_balisage_rapide.ipynb": update_05,
    }
    for name, fn in updates.items():
        path = ROOT / name
        nb = json.loads(path.read_text(encoding="utf-8"))
        nb = fn(nb)
        path.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"updated {path}")


if __name__ == "__main__":
    main()
