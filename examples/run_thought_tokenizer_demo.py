"""
Demo: Words -> Thoughts -> Thought Tokens & Multi-Team Swarm Architecture
Demonstrates:
  1. Distilling complex natural sentences into atomic conceptual Thought Tokens
  2. The Team-of-Teams Swarm Roster with distinct goals and specialist subagents
"""

from token_saver.thought_tokenizer import ThoughtTokenizer
from token_saver.swarm_orchestrator import SwarmHierarchy


def run_demo():
    print("=" * 80)
    print("DEMO 1: WORDS -> THOUGHTS -> THOUGHT TOKENS (CONCEPTUAL REASONING)")
    print("=" * 80)

    tokenizer = ThoughtTokenizer()

    test_sentences = [
        "The authentication database crashed because the jwt token expired.",
        "Could you please add the new user registration endpoint to the api server?",
        "We need to audit and verify the postgres database connection due to a timeout error."
    ]

    for sentence in test_sentences:
        thought_proposition = tokenizer.distill_sentence_to_thought(sentence)
        thought_token = tokenizer.encode_thought_tokens(sentence)

        words_in_raw = len(sentence.split())
        words_in_thought = len(thought_token.split())

        print(f"\n[SURFACE WORDS] ({words_in_raw} words):")
        print(f"  \"{sentence}\"")
        print(f"[EXTRACTED CONCEPTUAL THOUGHT]:")
        print(f"  Entities: {thought_proposition['entities']}")
        print(f"  Actions:  {thought_proposition['actions']}")
        print(f"  Causes:   {thought_proposition['causes']}")
        print(f"[CONVERTED THOUGHT TOKEN] (~{words_in_thought} token units, saved {round((1 - words_in_thought/words_in_raw)*100)}%):")
        print(f"  {thought_token}")

    print("\n" + "=" * 80)
    print("DEMO 2: TEAM-OF-TEAMS MULTI-AGENT SWARM STRUCTURE")
    print("=" * 80)

    hierarchy = SwarmHierarchy()
    print(hierarchy.display_full_swarm_hierarchy())


if __name__ == "__main__":
    run_demo()

