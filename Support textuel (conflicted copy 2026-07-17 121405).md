# 0. À préparer en amont

1. **Textes :** Veuillez repérer 2-5 transcriptions du type qui vous intéresse d'analyser, dont au moins une qui contient pas mal de noms propres (gens, toponymes, bureaux, titres d'ouvrage, ou bien des dates chinoises/japonaises).
2. **Éditeur XML :** il n'y a pas d'éditeur parfait, donc j'en ai pris un qui est pas mal et je l'ai amélioré selon ma propre vision de nos besoins. Veuillez l'installer en suivant les instructions pour votre système d'exploitation ici. 
3. **Plan B :** [XMLmind](https://www.xmlmind.com/products_fr.html), au cas où le mien bogue.
4. **Éditeur de texte brut avec expressions régulières :** gedit (Linux), [Notepad++](https://notepad-plus-plus.org/) (Windows), CotEditor (macOS)
5. **Clé API :** créez un compte gratuit chez [Groq](https://console.groq.com/) (≠ Groc), puis ouvre le truc dans le coin droit supérieur, créez une clé API, la notez, et l'entrez dans le panneau de configuration de l'éditeur XML:

```
Base URL: https://api.groq.com/openai/v1
API key: [votre clé API]
Model: qwen/qwen3.6-27b
```

---
# 1. Introduction au XML

**Qu'est-ce que c'est le XML ?** Le [XML](https://fr.wikipedia.org/wiki/Extensible_Markup_Language) (_eXtensible Markup Language_) est un langage informatique dont la but est la **structuration des données** afin de pouvoir les naviguer, extraire et transformer de manière rapide et reproducible. Il utilise des « balises » (par ex., `<p></p>` = paragraphe) pour identifier des « éléments » qui s'emboîte dans une arborescence. Voici un exemple :

```XML
<root>
	<body>
		<p>
			Cher collègue,
		</p>
		<p>
			Le XML, c'est <italics>génial</italics> !
		</p>
		<p>
			Bien cordialement,
		</p>
		<p>
			Daniel
		</p>
	</body>
</root>
```

**Qu'est que ça veut dire, et en quoi c'est utile ?** Imaginons que vous vouliez demander à un enfant d'aller chercher un objet précis dans une maison qu'il ne connaît pas. Vous pourriez lui dire :

> Dans la deuxième chambre, première bibliothèque à gauche, deuxième ou troisième étagère, il y a un panier de jouets, et dans ce panier il y a un paquet de cartes. Tu prends ça et le petit cahier bleu à côté.  

Le XML fournit à la machine les « balises » nécessaires de faire le même dans votre texte, en passant d'un « contentant » à l'autre: le paquet dans le panier dans l'étagère dans la bibliothèque... Ainsi, on peut demander à la machine, par exemple, « Va me trouver un paragraphe (`<p>`) qui utilise l'italique (`<italics>`), et donne moi l'ensemble du texte dans ce paragraphe ». 

La preuve que c'est utile : **vous travaillez déjà quasi-exclusivement en XML**. La suite Microsoft, c'est du XML, c'est le _x_ à la fin de vos `.docx` et de vos `.xlsx`. LibreOffice, OnlyOffice... tout est XML. Le traitement de texte traditionnel se sert du XML pour gérer les polices, la mise en page, l'ajout des notes, etc., mais on peut l'utiliser également dans un objectif scientifique, en particulier lorsque notre objet d'étude principal s'agit du texte. 

Ceci nécessite juste un petit changement de perspective et d'habitudes. 

En tant que « chercheur traditionnel », notre métier est l'écriture, et notre production textuelle relève principalement de deux catégories : d'abord, on écrit des notes, des listes, des résumés et des brouillons pour soi-même, puis on crée un texte qui a pour but de communiquer nos réflexions de manière compréhensible, accrocheuse et convaincante à un audience. **On écrit, dans les deux cas, pour un être humain**, et le gras, l'italique, la surbrilliance, l'indentation, les exposants... tout cela relève du « balisage » XML pour l'aider à s'orienter dans nos textes. **La question est de savoir comment écrire pour qu'une machine puisse les lire aussi.** En 2026, nous écrivons déjà pour les machines, qui représentent la première et la plus grande audience de tous nos documents, donc il faut l'assumer et nous adapter à cette nouvelle audience. 

**Qu'est-ce que l'on peut faire avec ça ?** Tout. Un corpus de transcriptions XML balisées avec métadonnées (titre, auteur, date, édition, etc.) s'agit fonctionnellement et par définition d'une base de données. Les limites principales sont votre imagination, le droit d'auteur et votre capacité de formuler de bonnes questions à poser à ses données.

Le XML, le TEI, le XPath, les _regex_... il est effectivement impossible de poser de bonnes questions à un corpus XML sans comprendre un peu les langages, les outils et le cadre conceptuel de l'informatique, mais on va le faire au fur et à mesure dans le contexte d'un flux de travail traditionnel légèrement modifié.

---
# 2. Préparation et traduction d'une source primaire « à la ancienne »

## Pratique traditionnelle

Le travail d'un sinologue consiste avant tout à lire et à traduire des sources primaires. Nous sommes peut-être vieux-jeu, mais c'est parce que notre civilisation est tellement vielle, glorieuse et centrale, et c'est de la folie d'aller changer ce qui a résisté à l'épreuve du temps. Ce n'est pas la japonologie enfin. Voici à quoi ça ressemble:

- Allumer une bougie.
- Faire une prière aux ancêtres. 
- Copier-coller une transcription trouvée en ligne dans Word.
- Consulter [Zdic](https://zdic.net/) et [Le Grand Ricci Online](https://brill.com/display/db/lgr) pour les mots difficiles, ou même un PDF de 故訓匯纂 s'il faut vraiment aller dans des livres.
- Mettre en surbrillance des passages important sans aucune explication de pourquoi vous avez fait ça – vous vous en souviendrez un jour, et ça va être incroyable. 
- Taper sa traduction et ses notes après le paragraphe étudié.
- Sauvegarder le fichier sous le nom `nouveau projet.docx` dans le dossier `sans titre` quelque part avec vos documents d'impôts.

## Pratique modifiée

Nous allons reproduire ce flux de travail dans LJB:

- Ouvrir l'éditeur.
- Ouvrir un nouveau projet.
- Choisir le schéma « TEI ALL »
- Dans `Project settings`:
	- choisir la langue de vos sources primaires
	- choisir la langue de vos traductions
	- laisser les défauts : central database, Paragraph (1:1)
- Créer un nouveau document.
- Coller votre transcription dans « paragraph text ».
- Ouvrir le panneau « Translation » à droite.
- Cliquer sur le paragraphe qui vous intéresse et taper une traduction dans le panneau « Translation ».

Dans le panneau « Translation », vous pouvez ajouter des notes de bas de page, insérer des références Zotero, etc. Cette traduction est liée au paragraphe mais dans un autre fichier pour que l'on ne mélange pas les deux textes. 

Si vous avez fourni une clé API, vous pouvez auto-générer une traduction à retravailler, en sachant que la qualité dépend du modèle, et que les APIs gratuites n'ont pas les meilleurs modèles.

## Devoirs

Essayez le suivant pour vous habituer à l'interface :

- [ ] Créer des documents
- [ ] Ouvrir et fermer des documents
- [ ] Copier-coller
- [ ] Parcourir vos document dans le panneau « Navigator »
- [ ] Entrer le titre et d'autre informations sur le document dans le panel « Document metadata »
- [ ] Ajouter quelques notes sur plusieurs paragraphes et les retrouver
- [ ] Ouvrir « Find and replace » (panel gauche, `ctrl/cmd+f`) pour chercher des mots clés dans la source primaire et dans vos traductions.
- [ ] Faire quelques minutes de vrai travail dedans.

Surtout, faites-moi signe s'il y a un bug ou une fonctionnalité manquante : c'est en version bêta, et vous jouez le double-rôle de bêta-testeur.

---

# 3. Styles et la surbrillance utile

## Pratique traditionnelle 

Vous avez sans doute constaté que je vous ai enlevé votre chère surbrillance dans l'éditeur de source primaire. C'est fini la surbrillance, mais ne vous inquiétez pas : je l'ai remplacé avec quelque chose de meilleur.

## Pratique modifiée

- Allez trouver une personne dans votre texte. 
- Sélectionnez-la. 
- Appuyez sur la touche `Entrée`. 
- Sélectionnez `persName`.
- Ouvrir le panneau « Attributes » à droite.
- Changez la couleur de la surbrillance et de la police.

Faîtes-le encore, pour une deuxième et une troisième personne, et vous allez découvrir qu'elle apparaissent toutes dans le même style. Félicitations : vous venez de faire du « balisage » et de modifier le CSS ([Cascading Style Sheet](https://fr.wikipedia.org/wiki/Feuilles_de_style_en_cascade)) qui gère le rendu graphique du code.

Ceci est _très utile_ pour vous orienter dans un texte, en particulier lorsque l'on met les personnes, les lieux, les organisations, les dates, etc., tous en différents couleurs. Et lorsque ça fait trop, on peut enlever la surbrillance pour revenir à un texte net. 

Par contre, ce n'est pas la vraie utilité de cette démarche : si l'on balise de manière homogène chaque occurence d'une catégorie de choses (`persName` = nom de personne), on aura des « données structurées » (= base de données) à exploiter.

## Devoirs

- Baliser d'autre `persName`.
- Cliquer sur `Show tags` pour une aperçu de vos balises.
- Basculer entre les vues `Visual` et `Source` pour voir le vrai code que l'éditeur vous permets d'écrire sans tapper tous les `</>` sans faute.
- Ouvrir le panneau « Validation » pour voir s'il y a des erreurs dans votre code. Il n'y en a pas ? C'est parce que la mode `Visual` vous empêche de faire des bêtises.
- Ouvrir le panneau « Markup » pour découvrir l'arborescence dont j'ai parlé. Essayez de naviguer dedans.
- Cliquez sur des choses dans la source primaire et voyez que vous vous déplacez dans l'arborescence. 
- Regardez aussi **l'adresse Xpath** (par ex. `TEI/text/body/div/p/persName`) affiché juste au-dessus de la source primaire – voici où se trouve l'élément sélectionné dans l'arborescence.  

---

# 4. Balisage : allez vite, 差不多就行了

## Pratique traditionnelle

> **Question :** Donc il faut que je mets TOUS les noms en surbrillance comme ça ? Mais c'est relou, et ça va prendre une éternité !
> **Réponse :** Pas si tu triches.  

## Pratique modifiée

**Paradigme :** Vous êtes sans doute un philologue sérieux, qui peut consacrer deux pages à l'analyse d'un seul mot, mais quant au balisage, comme la dit Staline, « la quantité a une qualité qui lui est propre ». Il faut aller vite, et ce n'est pas grave si l'on fait deux ou trois bêtises sur mille balises – on peut toujours les corriger après. 

### Stratégie de triche 1 : copier-coller

Si l'on balise la première occurence de « Laetitia » en tant que `persName`, on peut copier le texte baliser puis le coller sur les autres occurrences, n'est-ce pas ? Oui[1], mais encore mieux : 

- Sélectionner « Laetitia »
- Appuyer sur la touche `Entrée`.
- Sélectionner `persName`
- Appuyer sur les touches `Maj.+Entrée` pour baliser **toutes les occurences**.

^[1] En fait non, car il peut avoir des balises et des attributs cachés que l'on colle avec de façon erronée.

### Stratégie de triche 2 : regex

Si un élément se trouve toujours « au même endroit » et on sait formuler la configuration exacte, on peut baliser à l'aide de _regex_ ([regular expressions](https://fr.wikipedia.org/wiki/Expression_r%C3%A9guli%C3%A8re)). Prenons pour exemple le texte suivant : 

**《開元占經·卷二十四·歲星占二》：**

>石氏曰：「歲星犯左角，天下之道皆不通；犯右角，天下王使絕滅。」《荊州占》曰：「歲星犯角，天下有兵，將相有憂；犯右角，右將憂。」石氏曰：「歲星入角，天下有兵；其行疾，六十日；行遲，百二十日，遠百八十日。」《黃帝占》曰：「歲星出中道，天下太平；出陽道，旱；出陰道，多雨。」陳卓曰：「歲星出陰道，多陰謀。」甘氏曰：「歲星逆行入角，人主出入不時，若有急事，千里之行；一曰女子多死。」《孝經右秘》曰：「歲星在角，天下大病。」石氏曰：「歲星乘左角，法官誅；乘右角，大將軍死。」郗萌曰：「歲星乘左角，為旱；乘右角，為水，為兵。」《荊州占》曰：「歲星乘右角，為後族家，若將相有坐法死者。」郗萌曰：「歲星居角，歲大熟。」

C'est facile : les titres d'ouvrage se trouve entre 《 et 》; les noms de personne se trouve avant 曰 et après une fermeture de citation (」), sans les guillemets. 

Alors, les _regex_ sont le langage pour communiquer cela à un ordinateur en code. Ce n'est pas votre langue maternelle, mais ça s'apprend par des guides ([lien](https://www.freecodecamp.org/news/practical-regex-guide-with-real-life-examples/)) ou par l'IA. Dans ce cas-là, on s'appuie sur les expressions suivantes :

- `\w` : une « lettre » de mot (**w**ord) quelconque
- `+` : « ou plusieurs »
- `()`: « capturer pour le reproduire dans le résultat »
- `\1`: « reproduire la première chaîne capturée »

Pour les personnes, 

- chercher :  `」(\w+)曰` 
- remplacer par : `」<persName>\1</persName>曰`

Pour les ouvrages,

- chercher :  `《(\w+)》` 
- remplacer par : `《<title>\1</title>》`

Avec ces quatre lines de code on peut correctement baliser 90% des noms et des ouvrages qui apparaissent dans les 120 _juan_ de l'encyclopédie divinatoire _Kaiyuan zhanjing_ 開元占經 sans comprendre un mot de ce qu'il raconte.

**Devoirs:** numéros de page.

### Stratégie de triche 3 : « balisage automatique  » (regex en masse)

Apprendre le codage, c'est surtout apprendre à formuler des tâches que vous ne confériez jamais à un être humain, car elles sont à la fois trop bêtes et chronophages. Voici la manière dont il faut penser :

> Si l'on a un outil qui peut remplacer `Laetitia` par `<persName>Laetitia</persName>`, il faut simplement une liste complète des noms des millions de personages historiques pour les passer un par un dans cette outil. 

J'ai extrait de telles listes pour le chinois, le japonais et le tibétain de [Wikidata](https://www.wikidata.org/wiki/Wikidata:Main_Page), [VIAF](https://viaf.org/), la [NDL](https://www.ndl.go.jp/en/), [CBDB](https://cbdb.hsites.harvard.edu/), [DILA](https://authority.dila.edu.tw/) et [CHGIS](https://chgis.fas.harvard.edu/) , et je les ai intégrées dans la fonction `Auto-tagging` de l'éditeur. 

LJB établit et alimente une base d'_entities_ pour l'utilisateur (voir ci-dessous), et on peut importer les « [chaînes de caractères](https://fr.wikipedia.org/wiki/Cha%C3%AEne_de_caract%C3%A8res) », ou « chaînes », de celle-ci, ou même fournir une liste en forme de tableur de calcul.

### Stratégie de triche 4 : IA

Votre tante qui ne comprend rien vous rappelle depuis quelques années que la solution à tout est de « demander à l'IA » et que vous devrez faire ça. « Oui », on se dit, « mais l'IA hallucine, elle se trompe, et elle risque de corrompre le texte ». Votre tante a raison, c'est vous qui ne savez pas vous servir correctement de cet outil.

On ne demande évidement pas à l'IA « Balise ça pour moi rapido ». On lui en donne une copie dans un prompte très précis et structuré afin de lui demander où dans cette copie il mettrait des balises et pourquoi. Elle est gentile, donc on lui laisse la copie comme souvenir. Cela s'appele « JSON prompting » d'après le format de données utilisé pour garantir une réponse structurée.

LJB met en place les outils « AI suggest » et « AI audit » pour ceux qui ont une clé API à une IA, et vous vous êtes normalement inscrits pour une clé gratuite chez Groq.

### Validation

Peu importe votre méthode préférée de triche, le rôle de l'humain n'est pas de baliser le texte en soi mais plutôt de valider ce qu'a fait la machine et de faire le ménage derrière.

Pour faciliter la validation, LJB ouvre un panneau « Validation » après le balisage automatique, où vous pouvez accepter et rejeter chaque suggestion. Comme dans le balisage manuel, `Maj.+Entrée` applique le balisage à chaque occurence d'une chaîne donnée, et `Maj.+Retour arrière` le rejette pour tout.

C'est après avoir validé les résultats du processus automatisé que l'on se met au balisage manuel, et il restera normalement assez peu à faire. 

## Devoirs

- Essayer `Maj.+Entrée`, `Maj.+Retour arrière` lors du balisage manuel et de la validation.
- Repérer une configuration qui est exploitable par _regex_ et demander à une IA les deux lignes de code nécessaire pour baliser l'élément concerné.
- Essayer les différentes options et le filtrage dans `Auto-tagging`
- Voir comment l'IA se débrouille avec les noms propres cachés dans votre texte.
- Valider les résultats.

---
# 5. Exploitation de vos données structurées

## XPath : le langage pour naviguer dans votre base de données 

Les balises que vous venez d'ajouter au texte nous permet d'y naviguer. En sélectionnez-une, notez l'adresse Xpath en haut du panneau d'édition, ouvrez le panneau `XPath`, et entrez l'adresse. Par exemple :
```
TEI/body/div/p/persName
```
S'il y a plus qu'un paragraphe, et une personne, vous allez découvrir que toutes les personnes sont mises en surbrillances et que vous pouvez sauter de l'une à l'autre. C'est cool, Word ne fait pas ça.

Si l'on veut être précis, on peut utiliser des **index**. Si l'on veut la deuxième personne dans le premier paragraphe :
```
TEI/body/div/p[1]/persName[2]
```
Si l'on veut la première personne dans _chaque paragraphe_ :
```
TEI/body/div/p/persName[1]
```
Et si l'on s'en fiche d'où se trouvent les personnes exactement :
```
TEI//persName
```
Il suffit de comprendre le principe. C'est un langage informatique pour la machine, et l'IA peut vous aider à traduire, mais on ne sait pas quelle question formuler si l'on ignore la structure derrière. 

## Python et l'extraction des données

Extraction: list of strings, count of strings. (I can't do collab for this, right? Maybe jupyter?)
Problem: we've only got strings, these are just words, one or more might refer to the same person...
Lesson: we don't know who's who, and the data doesn't necessarily mean anything.

---
# 6. Désambiguïsation

## Théorie 

Avant d'avancer, il faut rentrer un peu dans la philosophie de la langue et réfléchir sur notre vocabulaire conceptuel.

D'abord, on utilise `persName` jusqu'à présent, car il n'y a pas de 'person' dans un document. Il n'y a que des _mots_ qui font référence à des choses extérieurs – des « entités ». 

Pire encore, la relation entre _person_ et _name_ n'est pas simple. Une personne a plusieurs noms (Daniel Patrick Morgan) et « formes de surface » (Daniel, Danny, Dan ; Morgan/Morgane`[sic.]`). Il y a aussi plusieurs personnes qui portent le même nom – [Daniel Morgan](https://danielmorgan.eu/) (Paris 3) et [Daniel Morgan](https://www.crcao.fr/membre/daniel-patrick-morgan/) (CNRS) –, sans parler de _prénom_ ou de _nom de famille_.  

La solution en informatique est de substituer l'entité par un identifiant unique, comme `p00045`. C'est pourquoi on utilise les ORCID, les DOI, les ISBN, etc. – pour _désambiguïser_ les [2725 auteurs qui portent le même nom que moi](https://orcid.org/orcid-search/search?searchQuery=Daniel%20Morgan) . 

Ceci entraîne un problème logistique : si l'on monte dans des chiffres comme [0000-0001-9115-3931](https://orcid.org/0000-0001-9115-3931), vous être sur de ne jamais vous tromper ? Et si moi je donne des identifiants à chacun présent aujourd'hui, et Jean-Baptiste attribue les mêmes à Jeremy et à ses beaux-parents, comment faire ?

Pour nous assurer que nous ne nous trompions pas avec les numéros, on a besoin d'une [base de données relationnelle](https://fr.wikipedia.org/wiki/Base_de_donn%C3%A9es_relationnelle) qui attribue des identifiants uniques de manière fiable et qui regroupe les relations entre formes de surface et entités : 'Marina' appartient à la catégorie 'prénom'; 'Marina' appartient à `p007623` (Marina Pandolfino); 'Marina' appartient à `p79006` (# Marina Lambrini Diamandis)... Il n'y a parmi nous qu'Armelle et moi qui avons nos propres bases de données [SQL](https://fr.wikipedia.org/wiki/Structured_Query_Language), et Armelle pourrait vous expliquer à quel point c'est chiant.

Sur la question de _l'autorité_, il y a ce que l'on appelle des « autorités », comme le [Buddhist Studies Authority Database Project](https://authority.dila.edu.tw/), qui sont énormes, fiables et répandues. Que ça soit le National Diet Library, le Chinese Biographical Database ou bien Wikipédia, il n'y a par contre aucune autorité qui est _complète_, et chacune a ses propres identifiants. En plus, ce n'est pas comme si vous aller ajouter une page Wikipédia pour chaque nouveau personage historique sur lequel vous tombez juste pour avoir un identifiant à lui attribuer... 

Pour vous dépanner, notre éditeur XML crée une petite base de données relationnelle dans le fichier `entities.xml` qui sert à quatre choses : 

- Attribuer à chaque entité que vous créez un identifiant unique.
- Regrouper les « chaînes de caractères » ou « formes de surface » qui lui appartiennent afin de faciliter le balisage.
- Établir une **concordance** entre vos identifiants et ceux de vos autorités de préférence.
- Retenir quelques informations qui sont utiles pour le filtrage. 

Idéalement, l'utilisateur pourrait intégrer sa propre base de données SQL, mais chacun a son infrastructure... À voir.
## Pratique : faire le lien _persName -> person_

Après avoir balisé votre texte, vous allez lancer le panneau `Disambiguate`. Pour chaque chaîne de caractères balisée, l'éditeur va vous proposer toutes les entités qui y sont associées dans les autorités activées dans le panneau de configuration. 

Il faut réfléchir : parfois les autorités se réfèrent l'une à l'autre par concordance, donc trois ou quatre indiquent tous une seule est même personne, qui est la bonne ; parfois il y a des doublons idiots, à regrouper si vous le souhaitez ; et parfois il n'y a rien, donc il faut créer une nouvelle entité. 

Comment faire le lien _persName_ -> _person_, concrètement ? On ajoute un « attribut » dans la balise :

```XML
... J'ai dit à <persName key="person-76296">Jeremy</persName> que son aptitude...
```

Il y a beaucoup d'attributs que l'on pourrait penser à ajouter à un `<persName>` : `@type` (prénom, surnom, etc.), `@cert` (certitude que le nom correspond à l'entité), etc. [La feuille de stile TEI](https://www.tei-c.org/release/doc/tei-p5-doc/fr/html/ref-persName.html) (vois ci-dessous) en propose de dizaines avec des définitions précises. On peut ajouter un attribut soit dans le panneau `Attributes`, soit avec `alt/option+Entrée`. On peut aussi propager des attributs aux chaînes identiques portant la même balise. 

Quel attribut et pourquoi ? Je ne peut pas dire : ça dépend de vos intérêts. Mais la désambiguïsation de personnes, lieux, roles et dates c'est la base. 

## Devoirs

- [ ] Sélectionner une balise, ouvrir le panel `Attributes`, et voir si elle à déjà été désambiguïsée. 
- [ ] Avec une balise non-désambiguïsée, lancer une recherche et l'identifie avec une entité dans l'une des autorités.
- [ ] Essayer l'outil `Disambiguate` pour le faire en masse.
- [ ] Consulter les entités dans votre base de données dans le panel `Entities`. 
- [ ] Ouvrir l'une des entrées, modifier les contenus et  

Attributes, this again is slow, and To deal with that, you give each an identifier... this is a relational database, like CBDB, DILA, But you don't have a relational database, right? LJB set one up for you!

Disambiguation...

Schemas - thinking up what you want to track.