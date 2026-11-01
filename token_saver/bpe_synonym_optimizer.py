"""
BPE Synonym Optimizer:
Vocabulary Hacking for Closed-Weights Tokenizers.
Substitutes multi-token phrasing with single-token semantic primitives natively
indexed in modern LLM vocabularies (e.g. Gemini SentencePiece, OpenAI cl100k_base).
"""

import re
from typing import Dict


class BPESynonymOptimizer:
    # Mappings from multi-token phrases to high-entropy single-token equivalents
    DEFAULT_SYNONYM_MAP: Dict[str, str] = {
        # Developer & Technical concepts
        r"\bnot implemented\b": "unimplemented",
        r"\bcalculate (the )?difference between\b": "diff",
        r"\bauthentication and authorization\b": "auth",
        r"\bdatabase connection\b": "db_conn",
        r"\benvironment variable(s)?\b": "env",
        r"\bregular expression(s)?\b": "regex",
        r"\bstandard deviation\b": "std_dev",
        r"\babstract syntax tree\b": "AST",
        r"\bapplication programming interface\b": "API",
        r"\bkey[- ]value pair(s)?\b": "mapping",
        r"\bcommand line interface\b": "CLI",
        r"\bhypertext transfer protocol\b": "HTTP",
        r"\bdomain specific language\b": "DSL",
        
        # Conversational / Linguistic multi-token reduction
        r"\bas soon as possible\b": "immediately",
        r"\bin order to\b": "to",
        r"\bwith respect to\b": "regarding",
        r"\bat the present time\b": "currently",
        r"\bdue to the fact that\b": "because",
        r"\bin the event that\b": "if",
        r"\ba large number of\b": "many",
        r"\bmake a decision\b": "decide",
        r"\btake into consideration\b": "consider",
        r"\bgive an explanation\b": "explain",
    }

    def __init__(self, custom_mappings: Dict[str, str] = None):
        self.mappings = dict(self.DEFAULT_SYNONYM_MAP)
        if custom_mappings:
            self.mappings.update(custom_mappings)

    def optimize_text(self, text: str) -> str:
        """
        Replaces multi-token idioms with single-token semantic equivalents.
        """
        optimized = text
        for pattern, replacement in self.mappings.items():
            optimized = re.sub(pattern, replacement, optimized, flags=re.IGNORECASE)
        return re.sub(r"[ \t]+", " ", optimized).strip()

