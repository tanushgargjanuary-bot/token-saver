"""
Automated Test Suite for TokenSaver & Active Session Ledger
Runs with Python's built-in unittest framework.
"""

import unittest
from token_saver import (
    SessionLedger,
    ASTSkeletonizer,
    BPESynonymOptimizer,
    TelegraphicOptimizer,
    ThoughtTokenizer
)


class TestSessionLedger(unittest.TestCase):
    def setUp(self):
        self.ledger = SessionLedger()

    def test_record_event(self):
        ref = self.ledger.record_event(
            event_type="DECISION",
            target="Database",
            details="Switched to PostgreSQL"
        )
        self.assertEqual(len(self.ledger.state_transitions), 1)
        self.assertEqual(self.ledger.state_transitions[0]["type"], "DECISION")

    def test_code_hashing_and_deduplication(self):
        sample_code = "def authenticate(user): return True"
        ref1 = self.ledger.record_event(
            event_type="CODE_CREATED",
            target="auth.py",
            details="Auth helper",
            code_snippet=sample_code
        )
        self.assertTrue(len(ref1) > 0)
        self.assertIn(ref1, self.ledger.code_registry)

        # Same code with whitespace variation should produce identical hash
        sample_code_spaced = "   def authenticate(user): return True   \n"
        ref2 = self.ledger.record_event(
            event_type="CODE_SNAPSHOT",
            target="auth2.py",
            details="Duplicate auth helper",
            code_snippet=sample_code_spaced
        )
        self.assertEqual(ref1, ref2, "Identical code should resolve to the same content hash")

    def test_export_ledger(self):
        self.ledger.record_event("MILESTONE", "Core", "Setup completed")
        exported = self.ledger.export_compressed_ledger()
        self.assertIn("=== ACTIVE SESSION STATE LEDGER ===", exported)
        self.assertIn("[MILESTONE] Core -> Setup completed", exported)


class TestOptimizationModules(unittest.TestCase):
    def test_ast_skeletonizer(self):
        code = """class Foo:
    def bar(self, x: int) -> int:
        y = x * 2
        return y"""
        skeleton = ASTSkeletonizer.skeletonize_python(code)
        self.assertIn("class Foo:", skeleton)
        self.assertIn("def bar(self, x: int) -> int:", skeleton)
        self.assertNotIn("y = x * 2", skeleton, "Implementation body should be replaced with ellipsis")

    def test_bpe_optimizer(self):
        opt = BPESynonymOptimizer()
        res = opt.optimize_text("in order to calculate the difference between items")
        self.assertEqual(res, "to diff items")

    def test_thought_tokenizer(self):
        tokenizer = ThoughtTokenizer()
        res = tokenizer.encode_thought_tokens("The database crashed because the jwt token expired")
        self.assertIn("ENT(", res)
        self.assertIn("ACT(FAIL)", res)
        self.assertIn("CAUSE(", res)


if __name__ == "__main__":
    unittest.main()

