#!/usr/bin/env python3
"""Polish the French markdown cells for course notebooks 00-05."""

from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent


ROOT = Path("Workshop/notebooks/course")


def lines(text: str) -> list[str]:
    text = dedent(text).strip("\n") + "\n"
    return text.splitlines(keepends=True)


UPDATES: dict[str, dict[int, str]] = {
    "00_a_preparer.ipynb": {
        0: """
        # 0. À préparer en amont

        ## Matériel

        - [ ] Ordinateur portable
        - [ ] Smartphone

        ## Compétences préalables

        - [ ] Être à l'aise dans un traitement de texte, comme Word
        - [ ] Télécharger et installer un logiciel
        - [ ] Créer un compte en ligne
        - [ ] Gérer ses mots de passe

        Si vous avez bien créé un compte mais que le mot de passe est resté sur un autre ordinateur, dans un carnet introuvable ou dans un coin de votre mémoire, je vous remettrai un magnifique chapeau d'âne et vous regarderai recréer le compte pendant que nous nous amuserons.

        ## Textes

        Ce workshop part de votre projet, pas d'un exemple abstrait. Venez avec :

        - [ ] 2 à 5 transcriptions du type de source que vous souhaitez étudier
        - [ ] dont au moins une contenant des noms de personnes, de lieux, d'institutions ou des titres d'ouvrage

        ## Questions

        - [ ] Notez quelques questions de recherche concrètes : que voudriez-vous regrouper, compter, comparer, retrouver ou fabriquer ? Nous ne visons pas la magie technologique, mais de la **recherche scientifique**.

        Par exemple :

        - « Je veux voir s'il y a une logique dans les listes de textes reçus dans des biographies tibétaines. »
        - « J'aimerais constituer une base de données de toutes les citations de Confucius dans les manuscrits des Royaumes combattants, avec tri par source, date ou contexte. »
        - « Je souhaite extraire des formules dispersées comme "_A_ est le maître de _B_" ou "_C_ est le fils de _D_" afin de reconstruire un réseau de relations. »

        ## Listes

        - [ ] _Si vous en avez_, apportez aussi toute liste de noms ou de termes d'une catégorie précise, par exemple une liste de 1 000 personnages en pinyin et en chinois avec dates de naissance et de décès.

        ## Comptes

        Vous allez créer un **compte [GitHub](https://github.com/)** pour trois raisons simples : avoir une présence dans cet espace, découvrir une autre manière de stocker et partager du travail, et activer une fonction importante de l'éditeur XML.

        - [ ] Créez un compte [ici](https://github.com/)
        - [ ] Installez l'application GitHub sur votre téléphone
        - [ ] [Activez l'authentification à deux facteurs](https://docs.github.com/fr/authentication/securing-your-account-with-two-factor-authentication-2fa/configuring-two-factor-authentication) afin de valider rapidement vos connexions

        Vous allez aussi créer un compte développeur gratuit chez [Groq](https://console.groq.com/), qui fournit une **clé API pour des LLM**. En clair, c'est un moyen pour que votre ordinateur puisse parler directement à une IA hébergée sur leur serveur.

        1. Créez un compte
        2. Ouvrez le menu en haut à droite de la page d'accueil
        3. Créez une clé API
        4. Notez-la quelque part de manière sûre

        ## Logiciels

        Vous aurez besoin d'un **éditeur de texte brut avec regex** :

        - Linux : `gedit` (`sudo apt-get install gedit`)
        - macOS : [CotEditor](https://coteditor.com/)
        - Windows : [Notepad++](https://notepad-plus-plus.org/)

        Vous aurez aussi besoin d'un **éditeur XML** avec interface graphique. Il n'existe pas d'outil parfait, mais certains petits projets sur GitHub sont parfois plus utiles que des solutions commerciales plus lourdes.

        - [ ] Allez sur [ce dépôt](https://github.com/lejeanbaptiste/lejeanbaptiste)
        - [ ] Lisez rapidement la description pour vérifier qu'il s'agit bien d'un éditeur XML
        - [ ] Cliquez sur l'étiquette `v0.0...` sous `Releases` pour accéder aux installateurs
        - [ ] Téléchargez le paquet correspondant à votre système d'exploitation (Linux/macOS/Windows) et à votre puce (AMD/ARM)[^1]
        - [ ] Installez le paquet

        Une fois l'éditeur installé, ouvrez-le et paramétrez-le :

        - [ ] Votre nom, pour l'encoder dans les métadonnées des textes que vous éditez
        - [ ] Le dossier racine, où seront stockées votre base de données et les ressources téléchargées
        - [ ] L'API IA :

        ```
        Base URL: https://api.groq.com/openai/v1
        API key: [votre clé API, voir ci-dessus]
        Model: qwen/qwen3.6-27b
        ```

        Si cet éditeur bogue ou refuse de s'installer, vous pouvez utiliser [XMLmind](https://www.xmlmind.com/products_fr.html) comme solution de secours.
        """,
    },
    "01_objectifs_et_strategie.ipynb": {
        0: """
        # 1. Objectifs et stratégie

        Vous êtes ici parce que votre projet implique déjà, directement ou indirectement, du XML. Je connais vos objets de recherche, je sais que vous voulez les faire avancer, et j'ai quelques compétences qui peuvent peut-être vous être utiles. J'ai donc conçu cette séance et l'outil principal à partir de vos besoins concrets, chacun à votre manière.

        Nous partons d'**un flux de travail familier** : lire une source, la traduire, prendre des notes, repérer des motifs. L'objectif n'est ni de remplacer ce flux ni de le bouleverser, mais de le modifier légèrement pour pouvoir faire « d'une pierre deux coups » au service de **l'efficacité**.

        Le balisage XML demande souvent un investissement important en amont pour un bénéfice qui paraît lointain et abstrait. Pour que cela vaille le coup dès aujourd'hui, nous allons montrer ce que _cela peut produire_ et chercher des **récompenses concrètes et immédiates**.

        Enfin, **nous mettrons la pratique avant la théorie** : on essaie, on observe, on maîtrise un geste, puis on lui donne un nom et une explication.

        « Pourquoi tu fais tout cela pour nous, Daniel ? » Mais non, vous n'avez rien compris : j'ai promis une formation au XML afin de recruter une équipe de bêta-testeurs, répartis sur plusieurs systèmes d'exploitation et architectures de puce, qui va œuvrer gratuitement sous ma surveillance pendant toute une journée. Chaque fois que vous rencontrez un problème, vous allez [ouvrir une issue sur GitHub](https://github.com/lejeanbaptiste/lejeanbaptiste/issues). Si en plus vous apprenez quelque chose, tant mieux.
        """,
    },
    "02_introduction_xml.ipynb": {
        0: """
        # 2. Introduction au XML

        Le [XML](https://fr.wikipedia.org/wiki/Extensible_Markup_Language) est un langage de structuration. Il utilise des **balises** pour décrire des éléments qui s'emboîtent dans une arborescence.

        ```xml
        <root>
          <body>
            <p>Cher collègue,</p>
            <p>Le XML, c'est <em>génial</em> !</p>
          </body>
        </root>
        ```

        **À quoi cela sert-il ?** Imaginez que vous demandiez à un enfant d'aller chercher un objet précis dans une maison qu'il ne connaît pas. Vous pourriez dire :

        > Dans la deuxième chambre, première bibliothèque à gauche, deuxième ou troisième étagère, il y a un panier de jouets ; dans ce panier, il y a un paquet de cartes. Tu prends cela et le petit cahier bleu à côté.

        Le XML donne à la machine les repères nécessaires pour faire la même chose dans un texte, en passant d'un « contenant » à l'autre : le paquet dans le panier, le panier dans l'étagère, l'étagère dans la bibliothèque. On peut alors lui demander, par exemple : « Trouve-moi un paragraphe (`<p>`) qui contient de l'italique (`<em>`) et renvoie-moi tout le texte de ce paragraphe. »

        La preuve que c'est utile, c'est que **vous travaillez déjà presque exclusivement en XML**. Dans Microsoft Office, le `x` de `.docx` ou `.xlsx` signifie précisément cela. LibreOffice, OnlyOffice et bien d'autres reposent aussi sur du XML. Le traitement de texte classique s'en sert pour gérer les polices, la mise en page, les notes et d'autres effets visuels ; nous pouvons, nous, l'utiliser pour une finalité scientifique, surtout lorsque notre objet principal est le texte.

        Cela demande simplement un petit déplacement de perspective. En tant que chercheurs, nous écrivons surtout deux types de textes : d'un côté des notes, des listes, des résumés et des brouillons pour nous-mêmes ; de l'autre, des textes destinés à présenter une réflexion de manière claire, intéressante et convaincante à un public. **Dans les deux cas, nous écrivons pour des humains**, et le gras, l'italique, la surbrillance, l'indentation ou les appels de note relèvent déjà d'un balisage. **La question devient donc : comment écrire pour qu'une machine puisse lire elle aussi ?**

        En 2026, nous écrivons déjà pour les machines, qui constituent souvent la première et la plus vaste audience de nos documents. Il vaut donc mieux l'assumer et s'adapter à cette nouvelle audience.

        **Que peut-on en faire ?** Presque tout. Un corpus de transcriptions XML avec métadonnées (titre, auteur, date, édition, etc.) fonctionne déjà, par définition, comme une base de données. Les limites principales sont votre imagination, le droit d'auteur et votre capacité à formuler de bonnes questions.

        Le XML, la [TEI](https://tei-c.org/), le XPath, les _regex_ : il est vrai qu'on ne pose pas de bonnes questions à un corpus XML sans apprendre un peu de langage, d'outillage et de cadre conceptuel informatique. Mais nous allons le faire progressivement, dans le contexte d'un flux de travail traditionnel à peine modifié.
        """,
    },
    "03_preparer_traduire.ipynb": {
        0: """
        # 3. Préparation et traduction d'une source primaire « à l'ancienne »

        ## Pratique traditionnelle

        Le travail d'un sinologue consiste d'abord à lire et à traduire des sources primaires. Voici notre flux de travail traditionnel, presque inchangé depuis l'époque des Qing :

        - Allumer une bougie
        - Faire une prière aux ancêtres
        - Copier-coller une transcription trouvée en ligne dans Word
        - Consulter [Zdic](https://zdic.net/), [Le Grand Ricci Online](https://brill.com/display/db/lgr) ou même un PDF de 故訓匯纂 quand il faut vraiment fouiller
        - Mettre des passages en surbrillance sans noter pourquoi, convaincu que l'on s'en souviendra plus tard
        - Taper une traduction et des notes après le paragraphe étudié
        - Sauvegarder le fichier sous le nom `nouveau projet.docx` dans un dossier `sans titre`, entre deux déclarations d'impôts

        ## Petite modification

        - Ouvrez l'éditeur XML
        - Créez un nouveau projet
        - Choisissez le schéma `TEI ALL`
        - Dans `Project settings` :
          - entrez la langue de vos sources primaires
          - sélectionnez la langue de vos traductions
          - laissez le reste par défaut (`central database`, `Paragraph (1:1)`)
        - Pour l'importation :
          - soit créez un nouveau document et collez votre transcription dans `Paragraph text`
          - soit importez un document (`File > Import`)
        - Ouvrez le panneau `Translation` à droite
        - Cliquez sur le paragraphe qui vous intéresse et tapez votre traduction dans le panneau `Translation`

        Dans `Translation`, vous pouvez aussi ajouter des notes de bas de page, insérer des références Zotero ou Juris-M, etc. La traduction est liée au paragraphe sélectionné depuis un fichier séparé, ce qui évite de mélanger la source primaire et vos traductions. Vous pouvez donc rattacher plusieurs traductions, dans plusieurs langues, à une seule transcription, les afficher ou les masquer, puis exporter la transcription avec la traduction de votre choix.

        Si vous avez fourni une clé API, vous pouvez aussi générer une première traduction automatiquement. Soyons clairs : la qualité dépend du modèle, et les API gratuites n'offrent pas toujours les meilleurs modèles. En revanche, cela peut déjà aider à lire rapidement une source difficile et à lancer l'interprétation.

        Enfin, exportez votre document en format Word, avec ou sans la traduction de votre choix.

        On reste donc proche de votre flux de travail habituel. La différence, c'est que l'outil unifie les transcriptions et sépare proprement les traductions. Il a aussi ses limites, notamment pour certaines options de mise en forme. Mais je suis le développeur, et ceci n'est encore qu'une version bêta.

        ## Exercices

        **Gestes de base**

        - [ ] Créez un document
        - [ ] Ouvrez et fermez des documents
        - [ ] Copiez-collez un texte dedans
        - [ ] Importez l'une de vos propres sources primaires
        - [ ] Parcourez les documents dans le panneau `Navigator`
        - [ ] Entrez le titre et d'autres informations dans `Document metadata`
        - [ ] Ajoutez quelques notes sur plusieurs paragraphes et retrouvez-les
        - [ ] Ouvrez `Find and replace` (panneau de gauche, `ctrl/cmd+f`) pour chercher des mots-clés dans la source primaire et dans vos traductions

        **Intégration**

        - [ ] Traduisez un petit paragraphe de l'une de vos sources en ajoutant des notes de bas de page et quelques références Zotero ou Juris-M

        ## Point de vigilance

        Ne paniquez pas : rien n'est perdu. Si une traduction semble avoir disparu, il faut souvent simplement rouvrir le panneau qui lui est dédié.
        """,
    },
    "04_styles_surbrillance.ipynb": {
        0: """
        # 4. Styles et surbrillance utile

        ## Pratique traditionnelle

        Vous avez chacun vos habitudes en matière de surbrillance. Quand je lis un article, je mets les faits intéressants en jaune, les personnes et les ouvrages en orange, les éléments structurels et argumentatifs en vert, et les bêtises en bleu. L'objectif est de me repérer rapidement et de _baliser_ le texte pour une relecture efficace.

        Le balisage XML, c'est exactement cela, mais de manière précise, systématique et exploitable.

        ## Petite modification

        1. Repérez un nom de personne dans votre texte.
        2. Sélectionnez-le et appuyez sur `Entrée`.
        3. Choisissez `persName`.
        4. Dans le panneau `Attributes`, à droite, changez la couleur de la balise et du texte.
        5. Faites la même chose pour deux autres personnes.

        C'est _très utile_ pour se repérer dans un texte, surtout si l'on met les personnes, les lieux, les organisations et les dates dans des couleurs différentes. Mais cette opération visuelle n'est qu'un effet secondaire de ce que vous venez de faire.

        **Vous avez balisé.** Dans le code, vous avez repéré une [chaîne de caractères](https://fr.wikipedia.org/wiki/Cha%C3%AEne_de_caract%C3%A8res) comme `Daniel` et vous l'avez remplacée par `<persName>Daniel</persName>`. Même chose pour `Jeremy`, etc. Cliquez sur `Show tags` et vous le verrez immédiatement. Vous avez non seulement indiqué qu'il s'agit de noms de personne, mais aussi qu'ils appartiennent à la même catégorie.

        Dans un site web ou un traitement de texte, l'apparence du texte est pilotée par une [feuille de style CSS](https://developer.mozilla.org/fr/docs/Web/CSS), qui définit par exemple que les paragraphes commencent sur une nouvelle ligne ou que les titres ont une taille particulière. De la même manière, **vous avez modifié la feuille de style** pour donner une apparence particulière à un élément XML.

        ## Exercices et observations

        - [ ] Balisez un toponyme (`placeName`), un titre d'ouvrage (`title`), un titre de fonction (`roleName`) ou une organisation (`org`) à proximité d'un nom de personne
        - [ ] Changez la surbrillance de l'un indépendamment de l'autre pour créer un contraste entre catégories

        Notre éditeur XML offre trois présentations d'un même fichier :

        1. `Visual` : la version « Word », pour les humains
        2. `Show tags` : un pseudo-XML qui montre les balises principales
        3. `Source` : le XML brut, pour les machines

        La version humaine est produite à partir de la version machine par la feuille de style, et vos interactions avec le texte passent elles aussi par un intermédiaire.

        - [ ] Retrouver un même élément balisé dans les trois modes
        - [ ] Dans le mode `Source`, essayez de changer un `persName` en `placeName` et observez ce qui se passe
        - [ ] Observez le résultat dans le mode `Visual`
        - [ ] Sauvegardez le document et essayez de casser volontairement le XML dans le mode `Source`

        À partir du moment où vous modifiez le code brut d'un document XML, vous êtes officiellement en train de coder.
        """,
    },
    "05_balisage_rapide.ipynb": {
        0: """
        # 5. Balisage : allez vite, 差不多就行了

        Objectif : maintenant, il faut baliser _tous les noms propres_.

        ## Pratique traditionnelle

        Vous êtes un philologue sérieux, capable de consacrer deux pages à l'analyse d'un seul mot. S'il faut baliser _tous les noms propres_ dans un document de 10 000 signes, cela peut donc prendre un mois : il faudrait consulter les ouvrages de référence, relire les derniers articles du domaine et établir un argumentaire au cas par cas. Et si un toponyme porte aussi le nom d'une ère politique ou d'une étoile, il faudra encore reconstituer l'ordre chronologique de toutes ces couches de sens.

        ## Changement de paradigme : l'imperfection et l'erreur statistique acceptable

        Comme l'a dit Staline, « la quantité a une qualité qui lui est propre ». L'objectif du balisage XML est de produire une masse de données homogène, suffisamment cohérente pour permettre un traitement informatique. La bonne méthode est donc la suivante :

        1. Balisez aussi vite que possible. Il vaut mieux _terminer_ un fichier que le _perfectionner_ à l'infini.
        2. Repassez ensuite pour corriger les bêtises évidentes et indiquer le degré de certitude des balises problématiques.
        3. Passez au fichier suivant.

        Vous allez vous tromper ici ou là, peut-être dans trois à dix cas sur mille. Il faut l'assumer.

        ## Entraînement psychologique

        - [ ] Sélectionnez une chaîne de caractères qui n'est absolument pas un nom de personne
        - [ ] Balisez-la en `persName`
        - [ ] Ouvrez le panneau `Attributes`, ajoutez une certitude (`cert`) et sauvegardez le document
        - [ ] Donnez à l'instructeur une description convaincante de la sérénité que vous devriez ressentir face à l'imperfection

        ## Nouvelle pratique

        Votre objectif principal est d'aller vite, et il existe plusieurs formes de triche tout à fait honorables pour y parvenir. Commençons par la plus familière.

        ### 1. Copier-coller

        Si l'on balise la première occurrence de « Laetitia » comme `persName`, on peut copier le texte balisé puis le coller sur les autres occurrences, exactement comme dans Word. Oui.

        - [ ] Dans le mode `Visual`, copiez-collez un élément et observez que la copie porte bien la même surbrillance
        - [ ] Dans le mode `Source`, copiez-collez `<persName>NOM</persName>` et observez que les balises sont aussi reproduites

        ### 2. Chercher et remplacer

        Comme dans Word, on peut remplacer toutes les occurrences d'une chaîne de caractères par une autre, soit d'un coup, soit une par une. Le principe est identique ici, mais le comportement dépend du mode de visualisation.

        Dans `Source` :

        - [ ] Sélectionnez une chaîne de caractères
        - [ ] Appuyez sur `ctrl+f` ou `cmd+f` pour ouvrir `Find and replace`
        - [ ] Remplacez `NOM` par `<persName>NOM</persName>`

        Dans `Visual` :

        - [ ] Sélectionnez une chaîne de caractères
        - [ ] Choisissez une balise
        - [ ] Appuyez sur `Maj.+Entrée` / `Shift+Enter`

        ### 3. Regex

        Dans l'exemple précédent, j'ai écrit `<persName>NOM</persName>` et vous avez compris qu'il ne faut pas taper littéralement « NOM », mais la chaîne de caractères qui vous intéresse. Cette partie variable peut être décrite très précisément à la machine grâce aux _regex_ ([expressions régulières](https://fr.wikipedia.org/wiki/Expression_r%C3%A9guli%C3%A8re)). Si vous voulez vous entraîner ailleurs, [regex101](https://regex101.com/) est aussi très pratique.

        Voici cinq éléments simples à retenir :

        - `\\w` : une lettre ou un caractère de mot quelconque
        - `\\n` : un saut de ligne
        - `+` : « un ou plusieurs »
        - `()` : « capturer pour réutiliser »
        - `\\1` : « réutiliser la première chaîne capturée »

        Les _regex_ sont très utiles. Prenons par exemple le passage suivant :

        **《太平御覽·夏下》：**

        >《易說》曰：立夏清明風至而暑，鶴鳴博穀飛，電見龍升天。〈龍，心星名。〉
        >《易通卦驗》曰：立夏雨，螻蛄鳴。
        >《三禮義宗》曰：四月立夏爲節者，夏，大也，至此之時，物已長大，故以爲名。小滿爲中者，物之生長小得幷滿，故以小滿爲名也。
        >《孝經緯》曰：穀雨後十五日，鬥指辰東南維爲立夏，後十五日，鬥指巳爲小滿。
        >《續漢書·禮儀志》曰：立夏之日，夜漏未盡五刻，京師百官皆衣赤，至季夏衣黃。
        >《抱樸子》曰：或問不熱之道。答曰：「立夏之日，或服玄冰丸，或服飛霜散及六壬六癸之符，則不熱。幼伯子、王仲都，此二人衣之以重裘，曝之于夏日之中，周以十爐之火，口不稱熱，身不流汗，蓋用此方者也。」

        Le _Taiping yulan_ 太平御覽 est une encyclopédie chinoise en 1 000 volumes. Même si vous n'en comprenez strictement rien, vous voyez que le format est très régulier :

        > 《TITRE》曰：CITATION 〈COMMENTAIRE〉 NOUVELLE LIGNE

        C'est parfait pour les expressions régulières.

        - [ ] Copiez-collez le passage dans votre éditeur
        - [ ] Basculez en mode `Source`
        - [ ] Ouvrez `Find and replace`
        - [ ] Expérimentez avec des regex dans `Find` pour retrouver tous les titres d'ouvrage d'un coup
        - [ ] Essayez de les baliser en une seule opération, en capturant puis en reproduisant la partie variable
        - [ ] Notez le temps qu'il a fallu à l'ordinateur pour exécuter l'opération

        Maintenant, faisons la même chose à l'échelle avec [Python](https://fr.wikipedia.org/wiki/Python_(langage)), le langage le plus répandu dans les humanités numériques. J'ai écrit le code pour vous, et j'expliquerai chaque ligne à l'aide de commentaires marqués par `#`. Une fois les regex manquantes complétées, cliquez sur la flèche pour lancer le script.
        """,
        2: """
        Maintenant, comptons le nombre de titres que vous venez de baliser :
        """,
        4: """
        C'est déjà très bien si vous arrivez à reconnaître un langage régulier dans vos sources et à en formuler les règles en _regex_. N'oubliez pas que vous pouvez demander de l'aide à une IA. Pour refaire cela chez vous, il suffit d'installer [Python](https://www.python.org/downloads/) et un éditeur comme [VS Code](https://code.visualstudio.com/), puis d'exécuter quelques scripts sur votre propre machine. L'important, à ce stade, est surtout de comprendre le principe.

        ### 4. « Balisage automatique » (= chercher et remplacer en masse)

        Sans _regex_, le « chercher-remplacer » ne permet de baliser qu'une chaîne à la fois. Cela reste pourtant utile, car on peut demander à l'ordinateur d'appliquer l'opération à partir d'une liste.

        J'ai extrait ce type de listes pour le chinois, le japonais et le tibétain à partir de [Wikidata](https://www.wikidata.org/wiki/Wikidata:Main_Page), [VIAF](https://viaf.org/), de la [NDL](https://www.ndl.go.jp/en/), de [CBDB](https://cbdb.hsites.harvard.edu/), de [DILA](https://authority.dila.edu.tw/) et de [CHGIS](https://chgis.fas.harvard.edu/), puis je les ai intégrées dans la fonction `Auto-tagging` de l'éditeur.

        LJB construit et alimente pour l'utilisateur une base d'_entities_ ; on peut donc importer les [chaînes de caractères](https://fr.wikipedia.org/wiki/Cha%C3%AEne_de_caract%C3%A8res) qui s'y trouvent, ou fournir sa propre liste sous forme de tableau.

        Exercices :

        - [ ] Essayez les différentes options et les filtres dans `Auto-tagging`
        - [ ] Essayez de valider les candidats : `Entrée` pour cette occurrence, `Maj.+Entrée` pour toutes les occurrences, `Backspace` pour rejeter, `Maj.+Backspace` pour toutes les rejeter

        ### 5. IA

        Vous avez probablement déjà constaté que l'IA peut être dangereuse si on lui laisse réécrire librement des sources primaires. Le problème n'est pas son existence, mais l'absence d'encadrement. Le principe est donc simple :

        - on donne une copie du texte à l'IA et on lui demande de remplir une sorte de formulaire décrivant précisément les modifications proposées
        - on soumet ensuite ces propositions à la validation de l'utilisateur
        - on applique enfin les modifications validées de manière mécanique, sans laisser l'IA toucher directement au texte source

        Pour cela, il faut que l'éditeur parle directement à l'IA via une [API](https://fr.wikipedia.org/wiki/Interface_de_programmation). Quelle IA choisir ? À vous de voir : vous pouvez en faire tourner une en local avec [Ollama](https://ollama.com/), utiliser une API gratuite comme celle de [Groq](https://console.groq.com/), ou payer une clé chez [Mistral](https://chat.mistral.ai/), [OpenAI](https://platform.openai.com/) ou ailleurs.

        Exercices :

        - [ ] Importez un nouveau document non balisé
        - [ ] Essayez `AI suggest` dans `Auto-tagging`

        ## Quelle approche choisir ?

        C'est à vous de choisir l'approche adaptée à votre corpus et à vos questions de recherche. L'idéal est de ne pas faire tant le balisage que le _ménage_ : préparer une structure propre, répétable et suffisamment bonne pour devenir utile à grande échelle.
        """,
    },
}


def main() -> None:
    for filename, updates in UPDATES.items():
        path = ROOT / filename
        notebook = json.loads(path.read_text(encoding="utf-8"))
        for cell_index, content in updates.items():
            notebook["cells"][cell_index]["source"] = lines(content)
        path.write_text(
            json.dumps(notebook, ensure_ascii=False, indent=1) + "\n",
            encoding="utf-8",
        )
        print(f"updated {path}")


if __name__ == "__main__":
    main()
