"""
Agent 2: Semantic Information-Entropy Pruner
Prunes low-information grammatical words while preserving critical semantic anchors
(code, numbers, identifiers, logic, error traces).
"""

import re
from typing import List, Tuple


class SemanticCompressor:
    # High-frequency grammatical function words carrying near-zero task entropy
    LOW_INFORMATION_WORDS = {
        "that", "which", "there", "their", "these", "those", "been", "being",
        "have", "having", "with", "from", "into", "during", "including", "until",
        "against", "among", "throughout", "despite", "towards", "upon", "such",
        "about", "also", "very", "really", "basically", "actually", "just"
    }

    # Protected syntactic anchors that must NEVER be stripped
    PROTECTED_PATTERNS = [
        r"```[\s\S]*?```",           # Multi-line code
        r"`[^`]+`",                   # Inline code
        r"\b\d+(\.\d+)?\b",           # Numbers & floats
        r"[=<>!+\-*/\\{}()\[\]@#$]",  # Syntax / Logic / Macro operators
        r"\b(not|never|no|if|else|return|def|class|error|fail|pass|true|false)\b", # Logic
        r"\b[A-Za-z0-9_]+\.[A-Za-z0-9_]+\b", # File paths or object dot access
    ]

    def __init__(self, target_retention_ratio: float = 0.65):
        """
        target_retention_ratio: 0.65 retains ~65% of the most informative words.
        """
        self.retention_ratio = target_retention_ratio

    def _calculate_token_importance(self, token: str, is_protected: bool) -> float:
        if is_protected:
            return 10.0

        clean = token.lower().strip(",.?!:;\"'")
        if not clean:
            return 0.0

        if clean in self.LOW_INFORMATION_WORDS:
            return 0.2

        score = 1.0
        # Longer words usually carry more domain information
        score += min(len(clean) * 0.15, 1.5)

        # Capitalized words (proper nouns, technical classes) carry high entropy
        if token and token[0].isupper():
            score += 1.2

        # Identifier structures (camelCase, snake_case)
        if "_" in token or any(c.isupper() for c in token[1:]):
            score += 2.0

        return score

    def compress(self, text: str) -> str:
        tokens = text.split(" ")
        if len(tokens) <= 6:
            return text

        scored_tokens: List[Tuple[str, float, bool]] = []
        for token in tokens:
            is_protected = any(re.search(pat, token) for pat in self.PROTECTED_PATTERNS)
            score = self._calculate_token_importance(token, is_protected)
            scored_tokens.append((token, score, is_protected))

        non_protected_scores = [item[1] for item in scored_tokens if not item[2]]
        if not non_protected_scores:
            return text

        non_protected_scores.sort(reverse=True)
        keep_count = int(len(non_protected_scores) * self.retention_ratio)
        cutoff = non_protected_scores[min(keep_count, len(non_protected_scores) - 1)]

        compressed = []
        for token, score, is_protected in scored_tokens:
            if is_protected or score >= cutoff:
                compressed.append(token)

        return " ".join(compressed)

