"""
Comprehensive Demonstration of Advanced TokenSaver Capabilities:
  1. AST Skeletonization (stripping function bodies, preserving contracts)
  2. BPE Vocabulary Hacking (single-token synonym substitution)
  3. Receding Horizon Memory Decay (tiered multi-step trajectory compaction)
"""

from token_saver import ASTSkeletonizer, BPESynonymOptimizer, RecedingHorizonMemory


def run_demo():
    print("=" * 80)
    print("1. AST SKELETONIZATION DEMO (Code Interface Preservation)")
    print("=" * 80)

    sample_service_code = """class PaymentService:
    def __init__(self, api_key: str, timeout: int = 30):
        self.api_key = api_key
        self.timeout = timeout
        self._client = StripeClient(api_key, timeout)

    def process_charge(self, user_id: str, amount_cents: int, currency: str = "usd") -> dict:
        \"\"\"Process payment through stripe with automatic retry.\"\"\"
        if amount_cents <= 0:
            raise ValueError("Amount must be positive")
        for attempt in range(3):
            try:
                res = self._client.charge(user_id=user_id, amount=amount_cents)
                return {"status": "success", "id": res.id}
            except Exception as e:
                logger.error(f"Attempt {attempt} failed: {e}")
        return {"status": "failed"}

    def refund_charge(self, charge_id: str, reason: str = "requested_by_customer") -> bool:
        return self._client.refund(charge_id=charge_id, reason=reason)
"""

    skeleton = ASTSkeletonizer.skeletonize_python(sample_service_code, keep_docstrings=True)
    raw_chars = len(sample_service_code)
    skel_chars = len(skeleton)

    print(f"Original Code:   {raw_chars} chars (~{raw_chars // 4} tokens)")
    print(f"Skeletonized:    {skel_chars} chars (~{skel_chars // 4} tokens) -> Saved {round((1 - skel_chars/raw_chars)*100)}%")
    print("\n--- Output Skeleton ---")
    print(skeleton)

    print("\n" + "=" * 80)
    print("2. BPE VOCABULARY HACKING DEMO (Single-Token Synonym Mapping)")
    print("=" * 80)

    optimizer = BPESynonymOptimizer()
    sample_phrase = (
        "In order to calculate the difference between the two datasets, "
        "we must inspect the database connection as soon as possible and take into consideration "
        "the authentication and authorization pipeline due to the fact that it is not implemented."
    )
    optimized_phrase = optimizer.optimize_text(sample_phrase)

    print("Original Phrase:")
    print(f"  \"{sample_phrase}\"")
    print("\nOptimized Phrase (aligned to single-token BPE primitives):")
    print(f"  \"{optimized_phrase}\"")

    print("\n" + "=" * 80)
    print("3. RECEDING HORIZON MEMORY DEMO (Multi-Turn Trajectory Compaction)")
    print("=" * 80)

    memory = RecedingHorizonMemory()
    
    # Simulate an 8-turn conversation
    turns = [
        ("user", "Can we set up a FastAPI backend with PostgreSQL?"),
        ("assistant", "Sure, I will initialize FastAPI with SQLAlchemy and asyncpg."),
        ("user", "Please add the user authentication endpoints with JWT tokens."),
        ("assistant", "Added JWT auth endpoints in src/auth.py with bcrypt hashing."),
        ("user", "We ran pytest and got an expired token signature error in tests."),
        ("assistant", "I diagnosed the issue in tests/test_auth.py: mock expiration timestamp was in past."),
        ("user", "Now let's implement the payment service for premium subscriptions."),
        ("assistant", "I'm working on the payment service now using Stripe integration.")
    ]

    for role, content in turns:
        memory.add_turn(role, content)

    compacted_history = memory.compile_decayed_context()
    print("--- Tiered Context Ready for Next Turn ---")
    print(compacted_history)
    print("=" * 80)


if __name__ == "__main__":
    run_demo()

