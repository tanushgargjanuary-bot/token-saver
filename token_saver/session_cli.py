"""
Session Ledger CLI:
A developer command-line utility to record, update, inspect, and export
compressed, lossless session logs for any coding project.

Usage:
  session-log init
  session-log record --type DECISION --target "Database" --details "Using PostgreSQL with asyncpg"
  session-log record-code --file src/models.py --details "Created User model"
  session-log dump
  session-log prompt
"""

import sys
import argparse
import os
from pathlib import Path
from .session_ledger import SessionLedger

LEDGER_FILENAME = ".session.log"


def load_or_create_ledger(base_dir: Path) -> Tuple[SessionLedger, Path]:
    ledger_path = base_dir / LEDGER_FILENAME
    ledger = SessionLedger()

    # If an existing ledger exists, we can append or restore
    # For now, it initializes in memory and syncs to disk
    return ledger, ledger_path


def cmd_init(args):
    target_dir = Path(args.dir or ".").resolve()
    ledger_path = target_dir / LEDGER_FILENAME
    if ledger_path.exists():
        print(f"[*] Session ledger already exists at: {ledger_path}")
        return

    ledger = SessionLedger()
    ledger.record_event(
        event_type="SESSION_INIT",
        target="Project",
        details=f"Initialized active session ledger in {target_dir.name}"
    )
    with open(ledger_path, "w", encoding="utf-8") as f:
        f.write(ledger.export_compressed_ledger())

    print(f"[+] Initialized active session ledger: {ledger_path}")


def cmd_record(args):
    target_dir = Path(args.dir or ".").resolve()
    ledger_path = target_dir / LEDGER_FILENAME

    ledger = SessionLedger()
    # Read existing if available
    existing_content = ""
    if ledger_path.exists():
        with open(ledger_path, "r", encoding="utf-8") as f:
            existing_content = f.read()

    ref = ledger.record_event(
        event_type=args.type,
        target=args.target,
        details=args.details
    )

    # Append to ledger file
    with open(ledger_path, "a", encoding="utf-8") as f:
        f.write(f"\n[{args.type.upper()}] {args.target} -> {args.details}")

    print(f"[+] Recorded {args.type} for '{args.target}' into {LEDGER_FILENAME}")


def cmd_record_code(args):
    target_dir = Path(args.dir or ".").resolve()
    ledger_path = target_dir / LEDGER_FILENAME
    file_path = Path(args.file).resolve()

    if not file_path.exists():
        print(f"[!] Error: File '{args.file}' does not exist.")
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        code_content = f.read()

    ledger = SessionLedger()
    ref = ledger.record_event(
        event_type="CODE_SNAPSHOT",
        target=str(file_path.relative_to(target_dir) if file_path.is_relative_to(target_dir) else file_path.name),
        details=args.details or f"Snapshot of {file_path.name}",
        code_snippet=code_content
    )

    with open(ledger_path, "a", encoding="utf-8") as f:
        f.write(f"\n[CODE_SNAPSHOT] {file_path.name} -> {args.details} | #REF:{ref}")
        f.write(f"\n#REF:{ref} >>>\n{code_content.strip()}\n<<<")

    print(f"[+] Stored exact code snapshot of '{file_path.name}' (#REF:{ref}) into {LEDGER_FILENAME}")


def cmd_dump(args):
    target_dir = Path(args.dir or ".").resolve()
    ledger_path = target_dir / LEDGER_FILENAME
    if not ledger_path.exists():
        print(f"[!] No {LEDGER_FILENAME} found in {target_dir}. Run 'session-log init' first.")
        return

    with open(ledger_path, "r", encoding="utf-8") as f:
        print(f.read())


def cmd_prompt(args):
    target_dir = Path(args.dir or ".").resolve()
    ledger_path = target_dir / LEDGER_FILENAME
    if not ledger_path.exists():
        print(f"[!] No {LEDGER_FILENAME} found in {target_dir}. Run 'session-log init' first.")
        return

    with open(ledger_path, "r", encoding="utf-8") as f:
        ledger_body = f.read()

    prefix = SessionLedger.generate_system_reader_prefix()
    
    print("=" * 80)
    print("COPY & PASTE THIS ENTIRE BLOCK INTO YOUR NEW AI SESSION / SYSTEM PROMPT:")
    print("=" * 80)
    print(prefix.strip())
    print("\n" + ledger_body.strip())
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(
        prog="session-log",
        description="Active Session Ledger: High-precision, compressed memory logs for AI coding workflows."
    )
    parser.add_argument("--dir", default=".", help="Project root directory (default: current directory)")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # init
    p_init = subparsers.add_parser("init", help="Initialize a .session.log in the project root")
    p_init.set_defaults(func=cmd_init)

    # record
    p_record = subparsers.add_parser("record", help="Record a decision, milestone, or architectural event")
    p_record.add_argument("--type", default="DECISION", help="Event type: DECISION, MILESTONE, ERROR_RESOLVED")
    p_record.add_argument("--target", required=True, help="Target system, module, or component")
    p_record.add_argument("--details", required=True, help="Brief description of the event")
    p_record.set_defaults(func=cmd_record)

    # record-code
    p_code = subparsers.add_parser("record-code", help="Record exact code snapshot from a file with content hash")
    p_code.add_argument("--file", required=True, help="Path to code file")
    p_code.add_argument("--details", default="Code snapshot", help="Description of changes")
    p_code.set_defaults(func=cmd_record_code)

    # dump
    p_dump = subparsers.add_parser("dump", help="Print the current compressed session ledger")
    p_dump.set_defaults(func=cmd_dump)

    # prompt
    p_prompt = subparsers.add_parser("prompt", help="Export the ready-to-paste prompt block for new AI chats")
    p_prompt.set_defaults(func=cmd_prompt)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

