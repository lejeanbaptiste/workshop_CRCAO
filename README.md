# Atelier XML — projet Jupyter

Projet pédagogique pour l'atelier XML. Les étudiants travaillent à partir de
leurs propres transcriptions XML/TEI et peuvent produire des statistiques,
des tables et des graphiques reproductibles.

## Démarrage rapide

```bash
python -m venv .venv
source .venv/bin/activate       # macOS/Linux
python -m pip install -r requirements.txt
```

Puis lancer Jupyter :

```bash
jupyter lab
```

## Ouvrir les notebooks dans un navigateur

Le dépôt contient aussi un site JupyterLite : Python et les notebooks
s'exécutent directement dans le navigateur, sans installation côté étudiant.
Après activation de GitHub Pages, le site sera disponible à l'adresse :

`https://lejeanbaptiste.github.io/workshop_CRCAO/`

Pour travailler avec un fichier XML personnel :

1. ouvrir le notebook voulu dans le site ;
2. déposer le fichier XML dans le dossier `data/` du navigateur ;
3. modifier `xml_path` dans la première cellule de code ;
4. exécuter les cellules avec `Shift+Enter`.

Les fichiers créés dans le navigateur sont conservés dans le stockage local du
navigateur. Pour récupérer un notebook ou un résultat, utiliser `Download`.
Le premier démarrage du noyau peut prendre quelques secondes, car Python est
chargé dans le navigateur.

Les notebooks servent de parcours guidé. Les scripts peuvent aussi être
exécutés directement :

```bash
python scripts/chapter_06_stats.py chemin/vers/mon-fichier.xml --output-dir outputs/chapter-06
python scripts/chapter_08_entities.py chemin/vers/mon-fichier.xml --output-dir outputs/chapter-08
```

Les scripts reconnaissent les documents TEI avec ou sans espace de noms XML.
Ils ne modifient jamais le fichier source.

## Organisation

- `course.md` — texte pédagogique de l'atelier.
- `notebooks/` — parcours Jupyter pour les étudiants.
- `scripts/` — analyses réutilisables en ligne de commande.
- `data/` — place pour des exemples XML anonymisés ou librement redistribuables.
- `outputs/` — résultats générés localement, ignorés par Git.

Le site JupyterLite est construit automatiquement par GitHub Actions à chaque
mise à jour de `main`. Dans les réglages du dépôt, sélectionner **GitHub
Actions** comme source de publication de GitHub Pages.

## Données et confidentialité

Ne pas déposer de clé API, de données personnelles ou de textes protégés par
le droit d'auteur dans le dépôt. Les étudiants travaillent sur une copie de
leurs fichiers XML et conservent les originaux séparément.
