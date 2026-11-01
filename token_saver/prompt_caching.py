"""
Agent 3: Prompt Caching & Cache Boundary Manager
Structures prompts to maximize hit rates on cloud provider context caches
(Anthropic Ephemeral Caching, Gemini Context Caching, OpenAI Automatic Caching),
yielding up to 90% credit discounts on static prefix blocks.
"""

from typing import Dict, Any


class PromptCachingEngine:
    def __init__(self, provider: str = "gemini"):
        self.provider = provider.lower()

    def partition_prompt(self, static_system_instructions: str, dynamic_payload: str) -> Dict[str, Any]:
        """
        Guarantees that static system instructions and macro specifications
        are strictly isolated from dynamic timestamps, session IDs, and user input.
        """
        if self.provider == "anthropic":
            # Anthropic prompt caching requires >= 1024 tokens for cache breakpoint
            return {
                "system": [
                    {
                        "type": "text",
                        "text": static_system_instructions,
                        "cache_control": {"type": "ephemeral"}
                    }
                ],
                "messages": [
                    {"role": "user", "content": dynamic_payload}
                ]
            }

        elif self.provider in ("gemini", "openai"):
            # Gemini & OpenAI cache based on matching leading prefix tokens
            return {
                "cached_prefix": static_system_instructions,
                "dynamic_suffix": dynamic_payload,
                "cache_eligible": True
            }

        return {
            "system": static_system_instructions,
            "user": dynamic_payload
        }

