#!/usr/bin/env python3
"""
Point d'entrée principal du projet.
Lance la pipeline d'évaluation de sécurité des LLMs.
"""

import sys
from pathlib import Path

# Ajouter src au path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from orchestrator import SecurityEvaluationPipeline
from config import LLM_MODELS


def main():
    """Fonction principale."""
    
    print(r"""
    ============================================================
      LLM Security Evaluation - Adversarial Examples Project
      Evaluation de la securite du code genere par les LLMs
      face a des variations de prompts
    ============================================================
    """)
    
    try:
        # Initialiser la pipeline
        pipeline = SecurityEvaluationPipeline()

        print(f"[INFO] Providers configurés : {list(LLM_MODELS.keys())}")
        
        # Exécuter avec les paramètres de test
        # Pour production: augmenter max_cves et max_prompts_per_cve
        pipeline.run_all(
            max_cves=1,           # Commencer par 1 CVE
            max_prompts_per_cve=1 # Puis 3 prompts
        )
        
    except FileNotFoundError as e:
        print(f"[X] Erreur: {e}")
        print("\n[TIP] Pour commencer:")
        print("  1. Créer le fichier data/cves/cves.json avec vos données CVE")
        print("  2. Ou copier votre fichier JSON dans data/cves/")
        return 1
    except Exception as e:
        print(f"[X] Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
