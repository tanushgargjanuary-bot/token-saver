"""
Receding Horizon Memory:
Implements multi-scale exponential context decay across long conversational trajectories.
As dialogue steps age, they are compressed across four cascading tiers:
  - Tier 0 (Active: 0-2 turns): Full fidelity (100%)
  - Tier 1 (Recent: 3-6 turns): Telegraphic & Semantic pruning (~60%)
  - Tier 2 (Mid-range: 7-14 turns): Code Skeletonization & Hashes (~30%)
  - Tier 3 (Long-range: 15+ turns): Abstract State Transitions DAG in SessionLedger (~10%)
"""

from typing import List, Dict, Any
from .telegraphic import TelegraphicOptimizer
from .semantic_pruner import SemanticCompressor
from .ast_skeletonizer import ASTSkeletonizer
from .session_ledger import SessionLedger


class RecedingHorizonMemory:
    def __init__(self):
        self.turns: List[Dict[str, str]] = []
        self.telegraphic = TelegraphicOptimizer(aggressive=True)
        self.semantic = SemanticCompressor(target_retention_ratio=0.60)
        self.ledger = SessionLedger()

    def add_turn(self, role: str, content: str, code_snippet: str = None):
        turn_data = {"role": role, "content": content}
        if code_snippet:
            code_ref = self.ledger.record_event(
                event_type="CODE_SNAPSHOT",
                target=f"turn_{len(self.turns)}",
                details=f"{role} code update",
                code_snippet=code_snippet
            )
            turn_data["code_ref"] = code_ref
        self.turns.append(turn_data)

    def compile_decayed_context(self) -> str:
        """
        Builds the active prompt context with exponential decay applied to older turns.
        """
        output_blocks = []
        total = len(self.turns)

        for idx, turn in enumerate(self.turns):
            age = total - 1 - idx
            role = turn["role"].upper()
            raw = turn["content"]

            if age <= 2:
                # Tier 0: Current & immediate prior turns (Full fidelity)
                output_blocks.append(f"[{role} - RECENT]: {raw}")

            elif 3 <= age <= 6:
                # Tier 1: Telegraphic + Semantic Pruning
                compressed = self.semantic.compress(self.telegraphic.to_telegraphic(raw))
                output_blocks.append(f"[{role} - STEP -{age}]: {compressed}")

            elif 7 <= age <= 14:
                # Tier 2: Skeletonized + Code References
                telegraph = self.telegraphic.to_telegraphic(raw)
                ref_info = f" [CODE_REF: #{turn['code_ref']}]" if "code_ref" in turn else ""
                output_blocks.append(f"[{role} - PAST]: {telegraph}{ref_info}")

            else:
                # Tier 3: Compact state transition anchor
                anchor = f"[{role} - ANCHOR]: Milestone at step -{age}: {raw[:80]}..."
                output_blocks.append(anchor)

        return "\n".join(output_blocks)

