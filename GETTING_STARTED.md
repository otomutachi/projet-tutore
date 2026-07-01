"""
GUIDE DE DÉMARRAGE - LLM Security Evaluation Project
"""

# 📦 INSTALLATION

## Option 1: Installation Simple (Recommandé)

```bash
# 1. Naviguer au dossier
cd "e:\2025 info\semestre 6\projet tutoré"

# 2. Lancer le setup
python setup.py

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer les API keys
# Éditer .env et ajouter:
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...
```

## Option 2: Installation Manuelle

```bash
# Créer un virtual env (optionnel mais recommandé)
python -m venv venv
venv\Scripts\activate  # Windows

# Installer dépendances
pip install -r requirements.txt

# Créer les dossiers
mkdir -p data\cves data\prompts data\results notebooks

# Copier le template .env
copy .env.example .env
```

---

# 🚀 PREMIÈRE EXÉCUTION

```bash
# 1. Vérifier l'installation
python examples.py

# Cela devrait afficher 3 exemples:
# - Génération de prompts
# - Analyse AST
# - Évaluation

# 2. Ajouter vos CVE JSON
# Placer dans data/cves/votre_fichier.json

# 3. Lancer la pipeline
python main.py

# Les résultats seront en data/results/evaluation_results.json
```

---

# 📊 UTILISATION

## Cas 1: Tester avec les exemples CVE

```bash
# Les exemples CVE sont en data/cves/example_cves.json
# Modifier main.py pour utiliser ce fichier:

python main.py
```

## Cas 2: Charger votre JSON de 127 prompts

```python
# Dans src/orchestrator.py, adapter:
pipeline.run_all(
    cve_file="votre_fichier.json",  # Chemin du fichier
    max_cves=5,                      # Nombre de CVEs
    max_prompts_per_cve=10          # Prompts par CVE
)
```

## Cas 3: Mode développement (sans API réelle)

```python
from src.llm_caller import MockLLM

# Dans config.py, utiliser MockLLM pour tester sans coûts API
llm_models = {"mock": "mock"}
```

---

# 🔑 CONFIGURATION DES API KEYS

## OpenAI (ChatGPT/GPT-4)

1. Créer compte: https://platform.openai.com
2. Créer une clé API
3. Ajouter à .env:
   ```
   OPENAI_API_KEY=sk-proj-xxxxx...
   ```

## Anthropic (Claude)

1. Créer compte: https://console.anthropic.com
2. Créer une clé API
3. Ajouter à .env:
   ```
   ANTHROPIC_API_KEY=sk-ant-xxxxx...
   ```

---

# 📁 STRUCTURE DES FICHIERS

## Format CVE JSON attendu

```json
[
  {
    "id": "CVE-2018-20548",
    "cwe": "CWE-190",
    "description": "Description de la vulnérabilité",
    "vulnerable_code": "code avec la vulnérabilité",
    "patch_code": "code corrigé sécurisé"
  }
]
```

## Format des résultats d'évaluation

```json
{
  "timestamp": "2025-06-27T...",
  "statistics": {
    "total_evaluations": 100,
    "average_combined_score": 0.75,
    "stats_by_llm": {...}
  },
  "results": [
    {
      "prompt_id": "prompt_0001",
      "cve_id": "CVE-2018-20548",
      "llm_provider": "claude",
      "correctness_score": 1.0,
      "security_score": 0.8,
      "combined_score": 0.94,
      ...
    }
  ]
}
```

---

# 🧪 TESTS

## Tester les composants individuels

```python
# Test prompt generation
python -c "from src.prompt_generator import PromptGenerator; PromptGenerator().generate_all_variations()"

# Test AST analyzer
python -c "from src.ast_analyzer import ASTComparator; ASTComparator().compare('int x;', 'size_t x;')"

# Test evaluator
python -c "from src.evaluator import SecurityEvaluator; SecurityEvaluator().evaluate_single(...)"
```

## Exécuter les exemples complets

```bash
python examples.py
```

---

# 📈 OPTIMISATION POUR LARGE SCALE

Pour traiter les 127 prompts complètement:

```python
# Modifier main.py:
pipeline.run_all(
    max_cves=None,              # Tous les CVEs
    max_prompts_per_cve=None    # Tous les prompts
)

# Ou en parallèle (Advanced):
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=4) as executor:
    # Traiter plusieurs CVEs en parallèle
    futures = [executor.submit(pipeline.run_single_cve, cve) for cve in cves]
```

---

# 🐛 TROUBLESHOOTING

## Erreur: "OPENAI_API_KEY non définie"
```
Solution: Créer/éditer .env avec votre clé API
```

## Erreur: "Aucun fichier CVE trouvé"
```
Solution: Ajouter un fichier JSON dans data/cves/
         Format: voir section "Format CVE JSON"
```

## Erreur: "Module not found: anthropic"
```
Solution: pip install anthropic
```

## Lent (API calls prend du temps)
```
Solution: Commencer petit (max_cves=1, max_prompts_per_cve=3)
         Augmenter progressivement une fois confirmé
```

---

# 📚 RESSOURCES

- **README.md** - Vue d'ensemble du projet
- **examples.py** - Exemples d'utilisation
- **src/config.py** - Configuration centrale
- **data/cves/example_cves.json** - Exemple de données CVE

---

# ✅ CHECKLIST DE DÉMARRAGE

- [ ] Python 3.8+ installé
- [ ] Dépendances installées (`pip install -r requirements.txt`)
- [ ] Dossiers créés (ou `python setup.py`)
- [ ] .env configuré avec les clés API
- [ ] Fichier CVE JSON ajouté
- [ ] `python examples.py` réussit
- [ ] `python main.py` peut être exécuté

---

**Prêt à démarrer? Exécutez: `python main.py`** 🚀
