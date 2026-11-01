"""
Example: Active Session Ledger for Multi-Session AI Memory
Demonstrates how to preserve exact code, architectural state, and decisions
across long conversation sessions with minimal token overhead.
"""

from token_saver import SessionLedger


def run_session_ledger_demo():
    print("=" * 80)
    print("SIMULATING SESSION 1: MULTI-STEP CODING & ARCHITECTURE WORKFLOW")
    print("=" * 80)

    ledger = SessionLedger()

    # Turn 1: Decision on database & framework
    ledger.record_event(
        event_type="DECISION",
        target="Stack",
        details="PostgreSQL + SQLAlchemy 2.0 with asyncpg driver"
    )

    # Turn 2: Exact User Model Code written
    user_model_code = """class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(default=True)"""

    ref1 = ledger.record_event(
        event_type="CODE_CREATED",
        target="src/models/user.py",
        details="Added async SQLAlchemy User model with email index",
        code_snippet=user_model_code
    )
    print(f"Recorded Code Event -> Created code hash #REF:{ref1}")

    # Turn 3: Error occurred and fixed
    ledger.record_event(
        event_type="ERROR_RESOLVED",
        target="src/models/user.py",
        details="Fixed missing Mapped type import from sqlalchemy.orm"
    )

    # Turn 4: Migration generated
    ledger.record_event(
        event_type="MILESTONE",
        target="Alembic",
        details="Generated migration 001_create_users_table and ran upgrade head"
    )

    print("\n" + "=" * 80)
    print("EXPORTING ACTIVE SESSION STATE LEDGER (Lossless, Compressed Memory)")
    print("=" * 80)

    compressed_ledger_text = ledger.export_compressed_ledger()
    print(compressed_ledger_text)

    # Check words vs raw conversation estimate
    ledger_words = len(compressed_ledger_text.split())
    # A standard 4-turn chat with code would easily be 800+ words of conversational back-and-forth
    raw_estimate_words = 850
    savings = round((1 - ledger_words / raw_estimate_words) * 100)

    print("\n" + "=" * 80)
    print("SESSION TRANSITION EFFICIENCY")
    print("=" * 80)
    print(f"Standard Multi-Turn History: ~{raw_estimate_words} words")
    print(f"Active Session Ledger:       ~{ledger_words} words (Saved {savings}%)")
    print("\nHow Session 2 reads this:")
    print("1. Inject `SessionLedger.generate_system_reader_prefix()` into the cached system prompt.")
    print("2. Pass the compressed ledger above. The new conversation immediately inherits")
    print("   the EXACT code for `src/models/user.py` without needing to re-read raw chat logs!")
    print("=" * 80)


if __name__ == "__main__":
    run_session_ledger_demo()

