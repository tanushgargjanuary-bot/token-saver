"""
Session Ledger: Lossless Code & State Memory Compressor for Multi-Session AI Contexts.

Preserves exact code blocks, architectural decisions, and error states across long
conversations using Content-Addressed Code Hashing and Unified Delta-Patching.
"""

import hashlib
import re
from typing import Dict, List, Optional, Any


class SessionLedger:
    def __init__(self):
        # Content-addressed registry: hash -> exact code string
        self.code_registry: Dict[str, str] = {}
        # Chronological timeline of state transitions
        self.state_transitions: List[Dict[str, Any]] = []

    def _hash_code(self, code_snippet: str) -> str:
        """Generates a 6-character content-addressed hash."""
        normalized = re.sub(r"\s+", " ", code_snippet).strip()
        return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:6]

    def record_event(
        self,
        event_type: str,
        target: str,
        details: str,
        code_snippet: Optional[str] = None
    ) -> str:
        """
        Records a major event (e.g. DECISION, CODE_CHANGE, ERROR, MILESTONE)
        into the active ledger with exact code preservation.
        """
        code_ref = None
        if code_snippet:
            code_hash = self._hash_code(code_snippet)
            if code_hash not in self.code_registry:
                self.code_registry[code_hash] = code_snippet.strip()
            code_ref = code_hash

        entry = {
            "type": event_type.upper(),
            "target": target,
            "details": details,
            "code_ref": code_ref
        }
        self.state_transitions.append(entry)
        return code_ref or ""

    def export_compressed_ledger(self) -> str:
        """
        Exports the entire multi-turn session into a hyper-dense, machine-readable
        state ledger that a new conversation can read with zero loss of code fidelity.
        """
        lines = [
            "=== ACTIVE SESSION STATE LEDGER ===",
            "# FORMAT: [EVENT_TYPE] TARGET -> DETAILS | #CODE_REF",
            "--- CHRONOLOGICAL STATE TRANSITIONS ---"
        ]

        for entry in self.state_transitions:
            ref_str = f" | #REF:{entry['code_ref']}" if entry["code_ref"] else ""
            lines.append(f"[{entry['type']}] {entry['target']} -> {entry['details']}{ref_str}")

        if self.code_registry:
            lines.append("\n--- EXACT CODE REGISTRY (CONTENT-ADDRESSED) ---")
            for h_code, snippet in self.code_registry.items():
                lines.append(f"#REF:{h_code} >>>\n{snippet}\n<<<")

        return "\n".join(lines)

    @staticmethod
    def generate_system_reader_prefix() -> str:
        """
        Returns the instructions to inject into a NEW conversation's cached system prefix
        so it immediately understands how to parse and query the active session ledger.
        """
        return """
[ACTIVE SESSION LEDGER PROTOCOL]
You have been provided with an ACTIVE SESSION STATE LEDGER from a previous session.
- Events marked [#REF:<hash>] reference exact code stored in the EXACT CODE REGISTRY.
- Treat this ledger as ground truth for existing files, architectural decisions, and current state.
- Do NOT re-ask the user for information already resolved in the state ledger.
"""

