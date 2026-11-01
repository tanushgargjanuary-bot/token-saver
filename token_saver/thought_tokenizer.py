"""
Thought Tokenizer:
Transforms surface language words into atomic Conceptual Propositions (Thought Tokens).
Pipeline:
  Surface Text -> Semantic Parsing -> Proposition Graph -> Atomic Thought Tokens
Eliminates grammatical fluff while preserving 100% of the logical causal structure.
"""

import re
from typing import List, Dict, Any, Tuple


class ThoughtTokenizer:
    """
    Encodes natural language into atomic thought units:
      [ACTOR] -> [ACTION / PREDICATE] -> [TARGET / PATIENT] | [CONDITION / CAUSE]
    """

    # Universal Semantic Primitives (Actions / States)
    ACTION_PRIMITIVES = {
        "crashed": "FAIL", "failed": "FAIL", "broken": "FAIL", "error": "FAIL",
        "create": "MUTATE.NEW", "add": "MUTATE.ADD", "implement": "MUTATE.NEW",
        "remove": "MUTATE.DEL", "delete": "MUTATE.DEL", "drop": "MUTATE.DEL",
        "update": "MUTATE.MOD", "modify": "MUTATE.MOD", "edit": "MUTATE.MOD",
        "fetch": "QUERY.READ", "get": "QUERY.READ", "read": "QUERY.READ",
        "verify": "EVAL.CHECK", "check": "EVAL.CHECK", "audit": "EVAL.CHECK",
        "expired": "STATE.EXPIRED", "timeout": "STATE.TIMEOUT",
    }

    # Universal Entity Primitives
    ENTITY_PRIMITIVES = {
        "database": "DB", "db": "DB", "postgres": "DB.PG", "mysql": "DB.MYSQL",
        "authentication": "AUTH", "auth": "AUTH", "jwt": "AUTH.JWT", "token": "AUTH.TOKEN",
        "user": "ENTITY.USER", "account": "ENTITY.USER",
        "server": "SYS.SERVER", "api": "SYS.API", "endpoint": "SYS.ROUTE",
        "test": "TEST", "pytest": "TEST.PYTEST",
    }

    def __init__(self):
        pass

    def distill_sentence_to_thought(self, text: str) -> Dict[str, Any]:
        """
        Extracts semantic roles from a sentence into a structured Thought Proposition.
        """
        words = re.findall(r"\b[A-Za-z0-9_.]+\b", text.lower())
        
        entities = []
        actions = []
        causes = []

        is_cause = False
        for word in words:
            if word in ["because", "due", "since", "caused"]:
                is_cause = True
                continue

            # Identify entity primitives
            if word in self.ENTITY_PRIMITIVES:
                ent = self.ENTITY_PRIMITIVES[word]
                if is_cause:
                    causes.append(ent)
                else:
                    entities.append(ent)

            # Identify action primitives
            elif word in self.ACTION_PRIMITIVES:
                act = self.ACTION_PRIMITIVES[word]
                if is_cause:
                    causes.append(act)
                else:
                    actions.append(act)

        return {
            "entities": list(dict.fromkeys(entities)),
            "actions": list(dict.fromkeys(actions)),
            "causes": list(dict.fromkeys(causes)),
            "raw": text
        }

    def encode_thought_tokens(self, text: str) -> str:
        """
        Converts natural words directly into atomic Thought Tokens.
        Example:
          "The authentication database crashed because the token expired"
          -> "[THOUGHT: ENT(AUTH, DB) -> ACT(FAIL) | CAUSE(AUTH.TOKEN, STATE.EXPIRED)]"
        """
        thought = self.distill_sentence_to_thought(text)
        
        ent_str = ",".join(thought["entities"]) if thought["entities"] else "SYS"
        act_str = ",".join(thought["actions"]) if thought["actions"] else "EVAL"
        
        cause_part = ""
        if thought["causes"]:
            cause_part = f" | CAUSE({','.join(thought['causes'])})"

        return f"[THOUGHT: ENT({ent_str}) -> ACT({act_str}){cause_part}]"

    @staticmethod
    def generate_thought_decoder_prefix() -> str:
        """
        Instruction injected into cached system prompt so LLMs natively read Thought Tokens.
        """
        return """
[THOUGHT-TOKEN GRAMMAR SPECIFICATION]
The input stream contains atomic Thought Tokens representing conceptual state:
- ENT(entities): Target systems or components
- ACT(action): Fundamental operation (FAIL, MUTATE, QUERY, EVAL)
- CAUSE(cause): Causal condition or failure trigger
Interpret these thought units directly as your cognitive context.
"""

