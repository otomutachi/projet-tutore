# Projet : génération de variantes de prompts

Ce projet sert à créer des variantes de prompts avec le même sens, mais une formulation différente. L’objectif est de tester des reformulations simples, comme des versions en Yoda, en anglais, en français ou avec de légères modifications de lettres, sans changer la compréhension globale du texte.

## Objectif

- générer des variantes de prompts lisibles et différentes,
- garder un sens similaire d’un prompt à l’autre,
- tester facilement ces variations dans un terminal,
- valider le comportement avec des tests automatisés.

## Structure du projet

```text
projet-tutore/
├── main.py
├── src/
│   └── prompt_generator.py
├── tests/
│   ├── test_prompt_mutations.py
│   └── test_terminal_llm_output.py
├── notebooks/
│   └── prompt_mutations_demo.py
└── README.md
```

## Utilisation rapide

### 1. Installer les dépendances

Dans l’environnement virtuel du projet :

```powershell
.
\.venv\Scripts\python.exe -m pip install pytest
```

### 2. Tester les mutations de prompts

```powershell
.
\.venv\Scripts\python.exe -m pytest -q tests/test_prompt_mutations.py
```

### 3. Tester l’affichage dans le terminal

```powershell
.
\.venv\Scripts\python.exe tests/test_terminal_llm_output.py
```

## Fonctionnement

Le module [src/prompt_generator.py](src/prompt_generator.py) contient plusieurs méthodes de mutation simples :

- synonymes,
- style Yoda,
- anglais,
- français,
- légère modification de lettres,
- variante de type fusion.

Chaque mutation conserve globalement le même sens, mais change la forme du texte.

## Exemple

Prompt de base :

```text
Replace the masked code with a secure fix.
```

Exemples de variantes possibles :

```text
A secure fix, the masked code replace.
Replace the masked code with a secure fix.
Remplace le code masqué par un correctif sécurisé.
R3pl4ce the m4sked c0d3 with a s3cur3 f1x.
```

## Notes

- Le projet est volontairement simple et léger.
- Il sert surtout de base pour tester des variantes de prompt sans ajouter beaucoup de fichiers ni de complexité.
- Les tests sont là pour vérifier que les mutations restent fonctionnelles.

