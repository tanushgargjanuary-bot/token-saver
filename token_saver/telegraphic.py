"""
Agent 1: Telegraphic and Structural Optimizer
Converts conversational padding into token-efficient telegraphic syntax
and structured key-value representations.
"""

import re
from typing import List, Optional


class TelegraphicOptimizer:
    CONVERSATIONAL_FILLERS = [
        r"\b(could you please|can you please|please kindly|would you mind)\b",
        r"\b(i was wondering if you could|i would like you to|i need you to)\b",
        r"\b(hello|hey|hi there|good morning|good evening|greetings)\b",
        r"\b(thank you so much|thanks in advance|i would really appreciate it)\b",
        r"\b(as an ai language model|as you know|in order to)\b",
        r"\b(feel free to|make sure to|be sure to)\b",
        r"\b(can you tell me|let me know)\b",
    ]

    ARTICLES_AND_WEAK_WORDS = [
        r"\b(a|an|the)\b",
    ]

    def __init__(self, aggressive: bool = False):
        self.aggressive = aggressive

    def strip_fillers(self, text: str) -> str:
        cleaned = text
        for pattern in self.CONVERSATIONAL_FILLERS:
            cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)
        return re.sub(r"[ \t]+", " ", cleaned).strip()

    def to_telegraphic(self, text: str) -> str:
        """
        Converts text into compact telegraphic English, safely preserving code.
        """
        code_blocks = []

        def save_code(match):
            code_blocks.append(match.group(0))
            return f"__CODE_SNIP_{len(code_blocks)-1}__"

        # Protect code snippets
        text_protected = re.sub(r"```[\s\S]*?```|`[^`]+`", save_code, text)

        cleaned = self.strip_fillers(text_protected)

        if self.aggressive:
            for pattern in self.ARTICLES_AND_WEAK_WORDS:
                cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)

        # Restore code blocks
        for i, block in enumerate(code_blocks):
            cleaned = cleaned.replace(f"__CODE_SNIP_{i}__", block)

        return re.sub(r"[ \t]+", " ", cleaned).strip()

    def to_structured_yaml(self, task: str, context: Optional[str] = None, constraints: Optional[List[str]] = None) -> str:
        """
        Converts requirements into a compact YAML structure that BPE tokenizers
        encode significantly more efficiently than verbose paragraphs.
        """
        lines = [f"TASK: {self.to_telegraphic(task)}"]
        if context:
            lines.append(f"CONTEXT: {self.to_telegraphic(context)}")
        if constraints:
            lines.append("CONSTRAINTS:")
            for c in constraints:
                lines.append(f"  - {self.to_telegraphic(c)}")
        return "\n".join(lines)

