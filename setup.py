#!/usr/bin/env python3
"""
Script de setup initial du projet.
Initialise les dossiers, télécharge les dépendances, etc.
"""

import os
import sys
from pathlib import Path


def setup():
    """Effectue le setup initial."""
    
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║      Setup Projet - Security Evaluation LLMs              ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    project_root = Path(__file__).parent
    
    # 1. Créer les dossiers
    print("📁 Création des dossiers...")
    for folder in [
        project_root / "data" / "cves",
        project_root / "data" / "prompts",
        project_root / "data" / "results",
        project_root / "notebooks",
        project_root / "logs",
    ]:
        folder.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {folder.relative_to(project_root)}")
    
    # 2. Créer .env s'il n'existe pas
    print("\n⚙️  Configuration...")
    env_file = project_root / ".env"
    if not env_file.exists():
        with open(project_root / ".env.example", 'r') as src:
            with open(env_file, 'w') as dst:
                dst.write(src.read())
        print(f"  ✓ .env créé (configurez vos clés API)")
    else:
        print(f"  ✓ .env existe déjà")
    
    # 3. Installer les dépendances
    print("\n📦 Installation des dépendances...")
    print("  (Vous pouvez ignorer ceci si déjà fait)")
    print(f"  Exécutez: pip install -r requirements.txt\n")
    
    # 4. Afficher les prochaines étapes
    print("="*60)
    print("🚀 SETUP TERMINÉ!")
    print("="*60)
    print("""
Prochaines étapes:

1️⃣  CONFIGURER LES API KEYS:
   - Éditer .env
   - Ajouter OPENAI_API_KEY et/ou ANTHROPIC_API_KEY

2️⃣  AJOUTER VOS DONNÉES:
   - Copier vos CVE JSON dans data/cves/
   - Ou utiliser l'exemple: data/cves/example_cves.json

3️⃣  TESTER L'INSTALLATION:
   - python examples.py
   
4️⃣  LANCER LA PIPELINE PRINCIPALE:
   - python main.py

💡 Pour plus d'infos, lire README.md
    """)


if __name__ == "__main__":
    setup()
