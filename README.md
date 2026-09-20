# Projet tutoré — Outil de mutation de prompts

Ce projet a pour objectif de concevoir un outil de mutation capable de produire des variantes de prompts afin d’évaluer la robustesse de modèles de langage, d’outils d’IA ou de systèmes de traitement de texte face à des perturbations lexicales, syntaxiques et sémantiques.

Le projet ne se limite pas à un simple générateur de texte altéré : il formalise une architecture de mutations réutilisables, paramétrables et composables, avec gestion des probabilités, des graines aléatoires et de l’application contrôlée sur des phrases ou des prompts.

Le code est organisé autour d’une base abstraite de mutations et de plusieurs familles de transformations :

- mutations orthographiques,
- mutations syntaxiques,
- mutations sémantiques,
- gestion de probabilités et de graines aléatoires,
- application contrôlée de mutations sur des phrases ou des prompts.

---

## 1. Objectif du projet

Le vrai but du projet est la conception d’un outil de mutation : un moteur qui applique des perturbations structurées à un prompt afin d’étudier comment le système cible réagit à des variations de forme, de syntaxe ou de sens.

Cette approche permet de simuler différentes formes de dégradation de texte :

Exemples de perturbations prises en charge :

- erreurs de frappe,
- accents supprimés,
- substitutions visuelles (lettres grecques, chiffres à la place de lettres),
- permutations de lettres ou de mots,
- reformulations de phrase,
- synonymes et traductions anglaises,
- ajout de contexte parasite.

L’objectif n’est donc pas seulement de produire des prompts altérés, mais de concevoir une bibliothèque de mutations réutilisables, testables et extensibles, destinée à l’évaluation de la robustesse d’un système d’IA face à des variations réalistes d’expression.

---

## 2. Architecture de l’outil de mutation

La logique du projet repose sur des classes héritant d’une base commune `Mutation` définie dans [src/mutation_base.py](src/mutation_base.py).

Chaque mutation suit une API simple :

```python
mutation.appliquer(chaine, proba)
```

ou encore, selon les cas :

```python
mutation.apply(chaine, proba, seed)
```

Les fonctions de compatibilité exposent des wrappers comme :

```python
remplacement_synonymes(chaine, proba, seed)
traduction_anglais(chaine, proba, seed)
faute_de_frappe(chaine, proba)
```

Une couche applicative dans [src/runner.py](src/runner.py) permet ensuite :

- choisir des mutations selon un nom,
- appliquer une mutation avec une probabilité donnée,
- appliquer plusieurs mutations en séquence,
- protéger certains mots de la mutation,
- contrôler le nombre de mots mutés,
- nettoyer la sortie et présenter le résultat de manière claire.

Cette partie est centrale dans la philosophie du projet : il s’agit d’un outil configurable, et non d’une simple suite de fonctions isolées.

- nettoyer les résultats,
- analyser une entrée,
- appliquer des mutations contrôlées,
- présenter les mutations de manière lisible,
- choisir des mutations au hasard.

---

## 3. Structure du projet

```text
.
├── data/                          # données de test / ressources
├── src/                          # code source principal
│   ├── mutation_base.py          # classe abstraite Mutation
│   ├── mutations_orthographiques.py
│   ├── mutations_semantiques.py
│   ├── mutations_syntaxiques.py
│   ├── runner.py                 # moteur d’application des mutations
│   ├── helpers.py               # utilitaires de gestion des prompts
│   ├── pydict_wrapper.py        # accès aux synonymes / traductions
│   ├── journal.py               # journalisation éventuelle
│   ├── utils.py                 # utilitaires généraux
│   ├── struct_compat.py         # compatibilité d’API
│   ├── generer_traductions.py   # génération de données de traduction
│   └── ...
├── tests/                        # tests unitaires
│   └── test_mutations.py
├── main.py                       # démonstration du projet
├── Makefile                      # raccourcis de lancement
├── requirements.txt              # dépendances Python
├── dataset1_of_prompts.json       # jeu de prompts de base
├── prompts_cve.json              # prompts liés à des CVE
├── mutations.csv                 # données de mutations exportées
├── resultats.json                # résultats de démonstration
├── resultats.csv                 # export CSV des résultats
├── .gitignore
├── README.md                     # documentation du projet
└── ...
```

---

## 4. Les familles de mutations

### 4.1 Mutations orthographiques

Fichier : [src/mutations_orthographiques.py](src/mutations_orthographiques.py)

Ces mutations modifient l’orthographe ou la forme visuelle d’un mot sans changer le texte principal.

Exemples :

- `RemplacementEPar3`
- `RemplacementAccents`
- `FauteDeFrappe`
- `AlphabetGrec`
- `DoublerPonctuation`
- `InsererVirguleAleatoire`
- `CasseApresPonctuation`
- `RemplacerPonctuationAleatoire`

Ces mutations sont utiles pour simuler des erreurs de frappe, de saisie ou des variations typographiques.

### 4.2 Mutations sémantiques

Fichier : [src/mutations_semantiques.py](src/mutations_semantiques.py)

Ces mutations remplacent ou reformulent des mots en gardant une signification proche.

Classes présentes :

- `ReformulationPhrase`
- `RemplacementSynonymes`
- `TraductionGenerique`
- `TraductionAnglais` (alias de `TraductionGenerique`)

Fonctions de compatibilité :

- `reformuler_phrase(...)`
- `remplacement_synonymes(...)`
- `traduction_vers(...)`
- `traduction_anglais(...)`

Le projet utilise `stopwordsiso` et des dictionnaires de synonymes / traductions via [src/pydict_wrapper.py](src/pydict_wrapper.py).

### 4.3 Mutations syntaxiques

Fichier : [src/mutations_syntaxiques.py](src/mutations_syntaxiques.py)

Ces mutations modifient la structure ou l’ordre des mots, sans forcément altérer le sens global.

Exemples :

- `PermutationLettres`
- `PermutationMots`
- `DilutionContexte`
- `MutationArgumentaire`
- `MutationStructureInversee`
- `MutationAleatoire`

Elles servent à tester la robustesse d’un prompt lorsque sa structure est légèrement déformée.

---

## 5. Dépendances

Les dépendances Python sont listées dans [requirements.txt](requirements.txt) :

```text
wn
argos-translate
stopwordsiso
```

Le projet dépend également de plusieurs bibliothèques externes utiles à la génération de synonymes et de traductions.

---

## 6. Installation

### Avec venv (recommandé)

Sous Windows PowerShell :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Sous Linux / macOS :

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 7. Lancement du projet

Le projet peut être exécuté directement avec :

```bash
python main.py
```

ou via le Makefile :

```bash
make run
```

Cela lance une démonstration avec plusieurs mutations sur des prompts d’exemple.

---

## 8. Exemple d’utilisation Python

```python
from src.mutations_semantiques import RemplacementSynonymes
from src.runner import appliquer_mutation

texte = "Génère un code sécurisé pour cette fonction."
resultat = RemplacementSynonymes().appliquer(texte, 0.8, seed=42)
print(resultat)

resultat2 = appliquer_mutation(texte, "synonyme", 0.5)
print(resultat2)
```

Autre exemple avec traduction :

```python
from src.mutations_semantiques import TraductionAnglais

phrase = "projet tutoré"
print(TraductionAnglais().appliquer(phrase, 1.0, seed=7))
```

---

## 9. Tests

Le dépôt contient une suite de tests dans [tests/test_mutations.py](tests/test_mutations.py).

Pour lancer les tests :

```bash
python -m pytest -q
```

ou, si la suite est utilisée via unittest :

```bash
python -m unittest discover -s tests
```

Les tests couvrent notamment :

- synonymes,
- traduction,
- structure des mutations,
- probabilités nulles et complètes,
- cas de prompts réels.

---

## 10. Données du projet

Le dossier racine contient plusieurs fichiers importants :

- `dataset1_of_prompts.json` : prompts de référence,
- `prompts_cve.json` : prompts liés à des problèmes de sécurité / CVE,
- `resultats.json` : sorties générées lors des démonstrations,
- `mutations.csv` et `resultats.csv` : export de données pour analyse.

---

## 11. Cas d’usage

Ce projet est particulièrement utile dans les contextes suivants :

- évaluation de robustesse de prompts,
- tests de résilience d’outils LLM,
- génération de données adversariales,
- étude de dégradation de langage naturel,
- benchmarking de modèles de génération.

---

## 12. Points d’attention

- Les mutations sont probabilistes : la même entrée peut donner des résultats différents selon la graine aléatoire.
- Certaines transformations sont dépendantes de dictionnaires externes de synonymes / traduction.
- La qualité du résultat dépend fortement des données disponibles dans les modules de dictionnaires et de traitements linguistiques.

---

## 13. Conclusion

Ce projet fournit une base simple et extensible pour générer des variations de prompts afin d’étudier la sensibilité des systèmes à des changements subtils mais réels du langage naturel.

Il combine :

- des mutations de surface,
- des mutations de structure,
- des mutations de sens,
- une gestion centralisée des probabilités et des graines.

C’est une base idéale pour approfondir les tests de robustesse ou créer des jeux de données adversariaux.

---

## 14. Auteurs / contexte

Ce dépôt correspond à un projet tutoré de semestre, dans le cadre de l’étude des prompts et des perturbations linguistiques applicables à des systèmes d’IA ou d’analyse automatique de texte.
