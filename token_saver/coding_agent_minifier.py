"""
Coding Agent Background Minifier:
Compresses massive development outputs (git diffs, pytest logs, compiler errors,
file dumps, and AST trees) before passing them to the LLM's context window.
"""

import re
from typing import List


class CodingAgentMinifier:
    @staticmethod
    def minify_git_diff(raw_diff: str) -> str:
        """
        Compresses git diffs by stripping index metadata, hashes, and unchanged
        context lines, keeping only added (+) and removed (-) lines and hunk headers.
        """
        minified_lines: List[str] = []
        for line in raw_diff.splitlines():
            # Skip git index metadata hashes (e.g. 'index 8a3b1..4c2d 100644')
            if line.startswith("index ") or line.startswith("diff --git"):
                continue
            # Keep file targets
            if line.startswith("--- ") or line.startswith("+++ "):
                minified_lines.append(line)
            # Keep hunk headers
            elif line.startswith("@@"):
                minified_lines.append(line)
            # Keep additions and deletions
            elif line.startswith("+") or line.startswith("-"):
                minified_lines.append(line)
            # Prune unchanged context lines to save tokens

        return "\n".join(minified_lines)

    @staticmethod
    def minify_test_or_build_log(raw_log: str, max_lines: int = 40) -> str:
        """
        Extracts only failures, tracebacks, and summary lines from verbose test/compiler logs.
        """
        lines = raw_log.splitlines()
        critical_lines = []
        capture = False

        for line in lines:
            lower = line.lower()
            if any(k in lower for k in ["fail", "error", "traceback", "exception", "assert"]):
                capture = True
                critical_lines.append(line)
            elif capture and (line.startswith(" ") or line.startswith("\t")):
                critical_lines.append(line)
            elif any(k in lower for k in ["passed", "failed", "summary", "error(s)"]):
                critical_lines.append(line)
                capture = False
            else:
                capture = False

        if not critical_lines:
            # Fallback if no specific failure patterns matched
            return "\n".join(lines[:10] + ["\n[...SNIPPED...]\n"] + lines[-10:])

        if len(critical_lines) > max_lines:
            critical_lines = critical_lines[:max_lines // 2] + ["\n[...SNIPPED...]\n"] + critical_lines[-max_lines // 2:]

        return "\n".join(critical_lines)

    @staticmethod
    def minify_code_for_reading(code: str) -> str:
        """
        Strips non-essential comments and consecutive blank lines from files read into context.
        """
        # Collapse multiple blank lines
        code = re.sub(r"\n\s*\n\s*\n+", "\n\n", code)
        return code.strip()

