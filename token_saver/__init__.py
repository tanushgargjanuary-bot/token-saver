"""
TokenSaver: Dual-Mode Token & Cost Optimization Architecture for AI Agents.

Bifurcates model processing into:
  1. Hyper-compressed Background & Thinking Layer (saves 60-85% credits)
  2. Natural, high-fidelity User-Facing Response Layer
  3. High-Precision Active Session Ledger (lossless cross-conversation memory)
  4. AST Skeletonizer (interface-preserving code compaction)
  5. BPE Synonym Optimizer (single-token vocabulary hacking)
  6. Receding Horizon Memory (multi-tiered exponential context decay)
  7. Thought Tokenizer (Words -> Thoughts -> Thought Tokens)
  8. Swarm Hierarchy (Team-of-Teams Multi-Agent Architecture)
"""

from .telegraphic import TelegraphicOptimizer
from .semantic_pruner import SemanticCompressor
from .prompt_caching import PromptCachingEngine
from .coding_agent_minifier import CodingAgentMinifier
from .dual_mode_orchestrator import DualModeOrchestrator
from .session_ledger import SessionLedger
from .ast_skeletonizer import ASTSkeletonizer
from .bpe_synonym_optimizer import BPESynonymOptimizer
from .receding_horizon_memory import RecedingHorizonMemory
from .thought_tokenizer import ThoughtTokenizer
from .swarm_orchestrator import SwarmHierarchy, SwarmTeam, Agent

__all__ = [
    "TelegraphicOptimizer",
    "SemanticCompressor",
    "PromptCachingEngine",
    "CodingAgentMinifier",
    "DualModeOrchestrator",
    "SessionLedger",
    "ASTSkeletonizer",
    "BPESynonymOptimizer",
    "RecedingHorizonMemory",
    "ThoughtTokenizer",
    "SwarmHierarchy",
    "SwarmTeam",
    "Agent",
]
