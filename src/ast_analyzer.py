"""
Analyseur AST pour comparer le code généré avec les patches de référence.
"""

import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class ASTNode:
    """Représentation simple d'un nœud AST."""
    type: str
    name: Optional[str] = None
    children: List['ASTNode'] = None
    
    def __post_init__(self):
        if self.children is None:
            self.children = []


class SimpleASTAnalyzer:
    """Analyseur AST simplifié pour C (sans tree-sitter pour l'instant)."""
    
    def __init__(self):
        self.type_patterns = {
            r'\bint\b': 'int',
            r'\bunsigned\s+int\b': 'unsigned_int',
            r'\bsize_t\b': 'size_t',
            r'\buint32_t\b': 'uint32_t',
            r'\buint64_t\b': 'uint64_t',
            r'\bchar\s*\*': 'char_ptr',
        }
    
    def extract_types(self, code: str) -> List[str]:
        """Extrait les types utilisés dans le code."""
        types = []
        for pattern, type_name in self.type_patterns.items():
            if re.search(pattern, code):
                types.append(type_name)
        return types
    
    def extract_declarations(self, code: str) -> List[Dict]:
        """Extrait les déclarations de variables."""
        # Pattern pour "type var, var2" ou "type var;"
        pattern = r'(\w+(?:\s+\w+)*?)\s+(\w+(?:\s*,\s*\w+)*)\s*[;,]'
        
        declarations = []
        for match in re.finditer(pattern, code):
            var_type = match.group(1).strip()
            vars_str = match.group(2)
            for var_name in vars_str.split(','):
                declarations.append({
                    'type': var_type,
                    'name': var_name.strip(),
                    'full': f"{var_type} {var_name.strip()}",
                })
        return declarations
    
    def compare_with_reference(
        self, 
        generated: str, 
        reference: str
    ) -> Tuple[float, Dict]:
        """
        Compare le code généré avec la référence (patch correct).
        
        Returns:
            (similarity_score, details)
            score: 0-1, où 1 = identique au patch correct
        """
        gen_types = set(self.extract_types(generated))
        ref_types = set(self.extract_types(reference))
        
        gen_decls = set(d['type'] for d in self.extract_declarations(generated))
        ref_decls = set(d['type'] for d in self.extract_declarations(reference))
        
        # Similarité : intersection / union
        type_similarity = len(gen_types & ref_types) / max(len(gen_types | ref_types), 1)
        decl_similarity = len(gen_decls & ref_decls) / max(len(gen_decls | ref_decls), 1)
        
        # Score final (moyenne pondérée)
        final_score = 0.6 * type_similarity + 0.4 * decl_similarity
        
        details = {
            'generated_types': list(gen_types),
            'reference_types': list(ref_types),
            'type_similarity': type_similarity,
            'decl_similarity': decl_similarity,
            'type_match': gen_types == ref_types,
        }
        
        return final_score, details


class ASTComparator:
    """Comparateur AST avec support pour tree-sitter (optionnel)."""
    
    def __init__(self, use_tree_sitter: bool = False):
        self.use_tree_sitter = use_tree_sitter
        self.simple_analyzer = SimpleASTAnalyzer()
        
        if use_tree_sitter:
            try:
                from tree_sitter import Language, Parser
                self.Language = Language
                self.Parser = Parser
            except ImportError:
                print("[WARN] tree-sitter non disponible, utilisation mode simple")
                self.use_tree_sitter = False
    
    def compare(
        self,
        generated: str,
        reference: str,
        vulnerable: str = None
    ) -> Dict:
        """
        Compare le code généré avec la référence (et vulnérable optionnel).
        
        Returns:
            {
                'correctness_score': float,  # Distance vers le patch correct
                'security_score': float,     # Distance loin du code vulnérable
                'details': {...}
            }
        """
        correctness, details = self.simple_analyzer.compare_with_reference(
            generated, reference
        )
        
        security = 1.0
        if vulnerable:
            security, _ = self.simple_analyzer.compare_with_reference(
                generated, vulnerable
            )
            security = 1 - security  # Inverser : loin = bon
        
        return {
            'correctness_score': correctness,
            'security_score': security,
            'combined_score': 0.7 * correctness + 0.3 * security,
            'details': details,
        }
    
    def batch_compare(
        self,
        generated_list: List[str],
        reference: str,
        vulnerable: str = None
    ) -> List[Dict]:
        """Compare plusieurs codes générés."""
        return [
            self.compare(gen, reference, vulnerable)
            for gen in generated_list
        ]


def main():
    """Test de l'analyseur AST."""
    
    analyzer = SimpleASTAnalyzer()
    comparator = ASTComparator()
    
    # Exemple de code vulnérable et patch correct
    vulnerable = "int w, h;"
    correct_patch = "size_t w, h;"
    generated = "unsigned int w, h;"
    
    print("[INFO] Test AST Analyzer\n")
    print(f"Vulnérable: {vulnerable}")
    print(f"Patch correct: {correct_patch}")
    print(f"Généré: {generated}\n")
    
    # Comparaison
    result = comparator.compare(generated, correct_patch, vulnerable)
    
    print(f"[INFO] Résultats:")
    print(f"  Correctness Score: {result['correctness_score']:.2%}")
    print(f"  Security Score: {result['security_score']:.2%}")
    print(f"  Combined Score: {result['combined_score']:.2%}")


if __name__ == "__main__":
    main()
