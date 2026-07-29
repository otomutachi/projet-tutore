# Documentation du projet

## Vue d'ensemble

Ce projet sert à tester la robustesse de petits prompts envoyés à des modèles de langage, surtout pour voir comment ils réagissent quand on change un peu le texte. L'idée est de faire des mutations simples sur des phrases pour créer des versions légèrement différentes, puis observer ce qui se passe. C'est un projet tutoré, donc le but n'est pas d'avoir un outil parfait, mais d'avoir un exemple clair de transformation de texte et de validation de comportement. On travaille surtout avec des mots, des fautes de frappe, des permutations et quelques substitutions de synonymes.

## Structure du projet

Voici la structure actuelle du projet, telle qu'elle se présente dans le dossier principal :

- main.py
- Makefile
- prompts.json
- prompts_cve.json
- resultats.json
- resultats.csv
- mutations.csv
- src/
  - journal.py
  - mutation_base.py
  - mutations_orthographiques.py
  - mutations_semantiques.py
  - mutations_syntaxiques.py
  - struct.py
  - utils.py
- tests/
  - test_mutations.py
- data/
  - synonymes.json
  - README.md
- header/

## Fichiers de code (src/)

### struct.py
Ce fichier sert à définir une structure de base pour les données utilisées par les mutations. Il contient des classes ou objets simples qui permettent de garder un peu d'ordre dans les informations manipulées par le programme.

- struct : structure de base utilisée pour stocker les informations importantes du projet.

### utils.py
Ce fichier sert à regrouper les petites fonctions utiles partagées par plusieurs parties du projet. Il y a notamment des fonctions pour charger des fichiers JSON, charger des prompts et afficher des résultats de manière simple.

- charger_dictionnaire_json : charge un fichier JSON de synonymes et retourne le dictionnaire. Si le fichier est absent ou invalide, il renvoie un dictionnaire vide avec un message simple.
- charger_prompts : lit un fichier JSON contenant des prompts et retourne une liste de chaînes de caractères.
- charger_prompts_cve : lit un fichier JSON de prompts liés à des contraintes CVE et reformate les données pour qu'elles soient plus faciles à utiliser.
- sauvegarder_prompts : enregistre les résultats des mutations dans un fichier JSON.
- afficher_resultats : affiche proprement les versions originales et mutées d'un prompt pour comparer visuellement.

### mutation_base.py
Ce fichier sert de base pour toutes les mutations. Il donne une interface simple, donc chaque mutation peut être utilisée de la même façon dans le programme principal.

- Mutation : classe de base avec la logique minimale attendue pour une mutation.

### mutations_orthographiques.py
Ce fichier contient les mutations qui jouent sur l'écriture des mots, par exemple des fautes de frappe ou des remplacements de lettres. C'est la partie la plus simple à comprendre du projet.

- AlphabetGrec : remplace certaines lettres par leur version grecque, pour créer une variation visible.
- FauteDeFrappe : introduit une erreur d'orthographe simple sur un mot.
- RemplacementAccents : remplace des accents ou des caractères proches.
- RemplacementEPar3 : remplace certains "e" par le chiffre "3".

### mutations_semantiques.py
Ce fichier contient les mutations qui changent le sens ou le vocabulaire d'un texte. C'est là que les synonymes sont utilisés pour rendre les prompts un peu plus différents.

- RemplacementSynonymes : remplace certains mots par des synonymes issus du dictionnaire JSON.
- TraductionAnglais : remplace quelques mots par leur traduction en anglais pour créer une variation plus marquée.
- remplacement_synonymes : fonction simple qui appelle la mutation de remplacement de synonymes.
- traduction_anglais : fonction simple qui appelle la mutation de traduction.

### mutations_syntaxiques.py
Ce fichier contient les mutations qui jouent sur l'ordre des mots ou la structure du texte. L'objectif est de garder un prompt compréhensible, mais un peu plus perturbé.

- DilutionContexte : ajoute un peu de bruit autour du sens principal du prompt.
- PermutationLettres : permute certaines lettres pour casser un peu la forme du mot.
- PermutationMots : permute l'ordre de quelques mots dans la phrase.

### main.py
Ce fichier sert de point d'entrée du projet. C'est lui qui charge les prompts, applique toutes les mutations et affiche les résultats.

- appliquer_mutations : applique une liste de mutations à une chaîne de texte.
- main : lance la démonstration complète avec les prompts de base et les résultats sauvegardés.

## Fichiers de données (data/)

### data/synonymes.json
Ce fichier contient le grand dictionnaire de synonymes utilisé par la mutation sémantique. Il est écrit sous forme de fichier JSON simple avec des paires clé/valeur. Le fichier a été rempli avec beaucoup de mots, en partant du vocabulaire déjà présent dans le projet puis en ajoutant d'autres mots techniques et courants autour de la génération de code, de la sécurité et de la qualité logicielle.

Le contenu vient d'abord du vocabulaire déjà utilisé dans le code et dans les prompts du projet, puis il a été élargi à partir de mots techniques retrouvés dans les prompts CVE. Ce dictionnaire est chargé par la fonction de chargement dans utils.py, puis utilisé par la classe RemplacementSynonymes dans mutations_semantiques.py.

### data/README.md
Ce fichier sert juste à expliquer rapidement le format du dictionnaire JSON et la provenance du vocabulaire. Comme JSON ne permet pas de mettre des commentaires directement, ce petit README permet de garder une trace simple pour la personne qui ouvre le dossier.

## Tests (tests/ ou test_mutations.py)

La batterie de tests sert à vérifier que les mutations gardent un comportement cohérent. Chaque test vérifie un cas précis, souvent avec une assertion simple sur le résultat attendu. L'idée est d'avoir des tests indépendants, pour voir rapidement si une modification a cassé quelque chose.

Les tests couvrent surtout des cas simples et des limites importantes, par exemple :
- probabilité de mutation égale à 0
- probabilité de mutation égale à 1
- chaîne vide
- prompts de test simples
- prompts plus proches de ceux qu'on retrouve dans la vie réelle

## Comment lancer le projet

Pour lancer la démonstration principale :

- python main.py


## Historique des évolutions

- Début du projet avec des fonctions simples et un compteur de substitutions.
- Passage à une logique plus probabiliste pour rendre les mutations moins régulières.
- Refactoring vers une approche orientée objet avec des classes de mutation séparées.
- Ajout d'un chargement de données depuis des fichiers JSON.
- Ajout de tests pour sécuriser les comportements de base.
- Élargissement du vocabulaire de synonymes pour rendre les mutations plus riches.
