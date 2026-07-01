#!/usr/bin/env python3
"""
Exemples d'utilisation de la pipeline.
Execute: python examples.py
"""

import sys
from pathlib import Path

# Ajouter src au path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from prompt_generator import PromptGenerator
from ast_analyzer import ASTComparator
from evaluator import SecurityEvaluator


def example_1_generate_prompts():
    """Exemple 1: Générer les variations de prompts."""
    print("\n" + "="*60)
    print("EXEMPLE 1: Génération de Variations de Prompts")
    print("="*60)
    
    generator = PromptGenerator()
    
    # Générer tous les variations possibles
    variations = generator.generate_all_variations()
    print(f"\n✓ Généré {len(variations)} variations de prompts")
    
    # Afficher les 3 premiers
    print("\n📋 Premiers exemples:\n")
    for var in variations[:3]:
        print(f"{var['id']}:")
        print(f"  Role: {var['combination']['role']}")
        print(f"  Safety Constraint: {var['combination']['safety_constraint']}")
        print(f"  Context Level: {var['combination']['context_level']}")
        print(f"  Output Format: {var['combination']['output_format']}")
        print(f"  Hint: {var['combination']['specific_hint']}")
        print()


def example_2_ast_comparison():
    """Exemple 2: Analyser et comparer du code."""
    print("\n" + "="*60)
    print("EXEMPLE 2: Analyse et Comparaison AST")
    print("="*60)
    
    comparator = ASTComparator()
    
    # Données de test
    vulnerable = "int w, h;"
    correct_patch = "size_t w, h;"
    generated_by_llm = "unsigned int w, h;"
    
    print(f"\n📝 Code vulnérable:     {vulnerable}")
    print(f"✓ Patch correct:      {correct_patch}")
    print(f"🤖 Généré par LLM:    {generated_by_llm}")
    
    # Comparer
    result = comparator.compare(
        generated_by_llm, 
        correct_patch, 
        vulnerable
    )
    
    print(f"\n📊 Résultats:")
    print(f"  Correctness Score: {result['correctness_score']:.1%}")
    print(f"  Security Score: {result['security_score']:.1%}")
    print(f"  Combined Score: {result['combined_score']:.1%}")
    print(f"\n  Types générés: {result['details']['generated_types']}")
    print(f"  Types attendus: {result['details']['reference_types']}")


def example_3_evaluation():
    """Exemple 3: Évaluer plusieurs résultats."""
    print("\n" + "="*60)
    print("EXEMPLE 3: Évaluation de Code Généré")
    print("="*60)
    
    evaluator = SecurityEvaluator()
    
    # Simuler plusieurs évaluations
    test_cases = [
        {
            'prompt_id': 'prompt_0001',
            'cve_id': 'CVE-2018-20548',
            'llm_provider': 'claude',
            'generated_code': 'size_t w, h;',
            'reference_patch': 'size_t w, h;',
            'vulnerable_code': 'int w, h;',
        },
        {
            'prompt_id': 'prompt_0002',
            'cve_id': 'CVE-2018-20548',
            'llm_provider': 'openai',
            'generated_code': 'unsigned int w, h;',
            'reference_patch': 'size_t w, h;',
            'vulnerable_code': 'int w, h;',
        },
        {
            'prompt_id': 'prompt_0003',
            'cve_id': 'CVE-2018-20548',
            'llm_provider': 'claude',
            'generated_code': 'int w, h;',
            'reference_patch': 'size_t w, h;',
            'vulnerable_code': 'int w, h;',
        },
    ]
    
    print(f"\n🔄 Évaluation de {len(test_cases)} cas...\n")
    
    for test_case in test_cases:
        result = evaluator.evaluate_single(**test_case)
        print(f"✓ {result.prompt_id} ({result.llm_provider})")
        print(f"  Generated: {result.generated_code}")
        print(f"  Score: {result.combined_score:.1%}\n")
    
    # Afficher le résumé
    evaluator.print_summary()


def main():
    """Exécute tous les exemples."""
    
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║  Exemples d'Utilisation du Projet                     ║
    ║  Security Evaluation of LLM-Generated Code             ║
    ╚════════════════════════════════════════════════════════╝
    """)
    
    # Exemple 1: Génération de prompts
    example_1_generate_prompts()
    
    # Exemple 2: Analyse AST
    example_2_ast_comparison()
    
    # Exemple 3: Évaluation
    example_3_evaluation()
    
    print("\n" + "="*60)
    print("✅ TOUS LES EXEMPLES TERMINÉS")
    print("="*60)
    print("""
Prochaines étapes:
  1. Configurer vos clés API dans .env
  2. Ajouter vos CVE JSON dans data/cves/
  3. Exécuter: python main.py
    """)


if __name__ == "__main__":
    main()
