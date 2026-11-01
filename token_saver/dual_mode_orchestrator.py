"""
Dual-Mode Orchestrator:
Separates AI processing into two distinct channels:
  1. Internal Thinking & Background Channel: Hyper-compressed, telegraphic, macro-dense (saves tokens)
  2. User-Facing Output Channel: 100% Natural, polite, well-formatted English (zero jargon or macros leaked)
"""

from typing import Dict, Any, Tuple
from .telegraphic import TelegraphicOptimizer
from .semantic_pruner import SemanticCompressor
from .prompt_caching import PromptCachingEngine
from .coding_agent_minifier import CodingAgentMinifier


class DualModeOrchestrator:
    SYSTEM_CACHE_PREFIX = """You are an advanced autonomous AI coding assistant.
You operate on a strict DUAL-CHANNEL communication protocol:

1. [CHANNEL 1: INTERNAL REASONING / THINKING SCRATCHPAD]
   - When generating your internal `<thought>` block, you MUST use dense telegraphic notation.
   - Use these standardized macro anchors to save tokens:
     @E[loc:err]    -> Encountered error or test failure
     @F[path:lines] -> File targeted or inspected
     @T[action]     -> Tool action to take
     @S[goal_state] -> Current milestone achieved
   - DO NOT write polite conversational essays in your thought block. Be ultra-dense and concise.

2. [CHANNEL 2: USER-FACING RESPONSE]
   - When generating your final `<response>` block for the user, you MUST use clear, natural, high-fidelity human English.
   - DO NOT use the internal macros (@E, @T) or telegraphic slang in your user response.
   - Be helpful, well-structured, professional, and friendly to the user.

OUTPUT FORMAT:
<thought>
[Dense telegraphic reasoning using macros]
</thought>
<response>
[Natural, polished human response]
</response>
"""

    def __init__(self, provider: str = "gemini"):
        self.telegraphic = TelegraphicOptimizer(aggressive=False)
        self.semantic = SemanticCompressor(target_retention_ratio=0.70)
        self.caching = PromptCachingEngine(provider=provider)
        self.minifier = CodingAgentMinifier()

    def prepare_agent_turn(self, user_query: str, background_tool_output: str = "") -> Dict[str, Any]:
        """
        Compresses background tool outputs and user context into token-efficient payloads,
        enforcing the dual-mode prompt contract.
        """
        # Compress background tool data (git diffs, pytest logs, etc.)
        compressed_tool_output = ""
        if background_tool_output:
            minified_raw = self.minifier.minify_test_or_build_log(background_tool_output)
            compressed_tool_output = f"\nTOOL_RESULT_COMPRESSED:\n{minified_raw}"

        # Light telegraphic optimization on query
        processed_query = self.telegraphic.strip_fillers(user_query)

        dynamic_payload = f"USER_INPUT: {processed_query}{compressed_tool_output}"

        return self.caching.partition_prompt(
            static_system_instructions=self.SYSTEM_CACHE_PREFIX,
            dynamic_payload=dynamic_payload
        )

    @staticmethod
    def parse_dual_output(raw_model_response: str) -> Tuple[str, str]:
        """
        Splits the model's output into:
          - internal_thought (kept in agent history / logs in compressed format)
          - user_facing_response (displayed cleanly to the user)
        """
        thought = ""
        response = raw_model_response

        if "<thought>" in raw_model_response and "</thought>" in raw_model_response:
            parts = raw_model_response.split("</thought>")
            thought = parts[0].replace("<thought>", "").strip()
            rest = parts[1]
            if "<response>" in rest and "</response>" in rest:
                response = rest.replace("<response>", "").replace("</response>", "").strip()
            else:
                response = rest.strip()
        elif "<response>" in raw_model_response:
            response = raw_model_response.replace("<response>", "").replace("</response>", "").strip()

        return thought, response

