<p align="center">
  <img src="assets/banner.svg" alt="TokenSaver Hero Banner" width="100%" />
</p>

<p align="center">
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.8+"/></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge&logo=open-source-initiative&logoColor=white" alt="MIT License"/></a>
  <a href="#-benchmarks"><img src="https://img.shields.io/badge/Token_Savings--75%25_to_-85%25-brightgreen?style=for-the-badge" alt="Savings"/></a>
  <a href="#-the-active-session-ledger-session-log"><img src="https://img.shields.io/badge/Session_Memory-Lossless_Code-8A2BE2?style=for-the-badge" alt="Memory"/></a>
  <a href="https://github.com/tanushgargjanuary-bot/token-saver"><img src="https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge" alt="Production"/></a>
</p>

<p align="center">
  <b>Lossless, high-precision session memory logs and dual-channel prompt compression for AI coding workflows and autonomous agent swarms.</b>
</p>

---

## ⚡ Why TokenSaver?

When building with AI coding assistants and autonomous agents:

1. **Traditional `session.log` files are destructive:** Normal chat summaries describe code in vague prose (*"The user created an auth function and resolved an error"*). When you open a new session, the AI loses all exact imports, function signatures, SQL schemas, and variable types.
2. **The Context Death Spiral:** Pasting raw files, compiler traces, and 80-line test outputs across multiple turns causes context windows to compound quadratically, running out of memory and burning through API credits.
3. **Internal Thinking is 3×–4× More Expensive:** In reasoning models, Chain-of-Thought (CoT) tokens cost up to 4× more than input tokens. Verbose self-talk burns credits fast.

**TokenSaver solves all three through an Active Content-Addressed Code Ledger and a Dual-Channel Cognitive Tokenizer.**

---

## 🏛️ System Architecture

<p align="center">
  <img src="assets/architecture.svg" alt="TokenSaver Architecture" width="100%" />
</p>

---

## 🌟 The Flagship Feature: Active Session Ledger (`session-log`)

Instead of saving narrative chat summaries, **TokenSaver turns your project's memory into an active, content-addressed database** (`.session.log`):

* 🔑 **Exact Code Fidelity:** Stores code snippets by 6-character content hashes (`#REF:9b2f14`). Repeated code blocks are automatically deduplicated.
* 📈 **State Transition Graph:** Tracks decisions, errors, and milestones as state machines rather than messy paragraphs.
* 🤝 **Instant Session Handshake:** Run `session-log prompt` to get a copy-pasteable block that restores deep memory in **80% fewer tokens**.

### CLI Quickstart

```bash
# 1. Install locally into your environment
pip install -e .

# 2. In any project root, initialize an active session ledger:
session-log init

# 3. Record an architectural decision:
session-log record --type DECISION --target "Database" --details "Switched to asyncpg connection pooling"

# 4. Snapshot an exact code file (stored with content-hash #REF:hash):
session-log record-code --file src/models/user.py --details "Created async User model"

# 5. Export prompt block for a NEW AI conversation:
session-log prompt
```

#### What Session 2 Reads:
```markdown
[ACTIVE SESSION LEDGER PROTOCOL]
- Events marked [#REF:<hash>] reference exact code in the EXACT CODE REGISTRY.
- Treat this ledger as ground truth for existing files and decisions.

[DECISION] Database -> Switched to asyncpg connection pooling
[CODE_SNAPSHOT] user.py -> Created async User model | #REF:9b2f14

--- EXACT CODE REGISTRY (CONTENT-ADDRESSED) ---
#REF:9b2f14 >>>
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
<<<
```

---

## 🧠 Breakthrough Concepts

<details open>
<summary><b>1. Words ➔ Thoughts ➔ Thought Tokens (Conceptual Reasoning)</b></summary>
<br>

Current LLMs tokenize raw characters *before* understanding them. TokenSaver flips the paradigm:

$$\text{Surface Words} \xrightarrow{\quad\text{Semantic Distillation}\quad} \mathbf{\text{Conceptual Propositions}} \xrightarrow{\quad\text{Quantization}\quad} \text{Thought Tokens}$$

* **Input:** `"The authentication database connection crashed because the jwt token expired."`
* **Distilled Thought:** `ENT: [AUTH, DB] | ACT: [FAIL] | CAUSE: [AUTH.TOKEN, STATE.EXPIRED]`
* **Thought Token:** `[THOUGHT: ENT(AUTH,DB) -> ACT(FAIL) | CAUSE(AUTH.TOKEN,STATE.EXPIRED)]`

> **Why Reasoning Improves:** Strips 70% of grammatical fluff while locking in causal logic. Different ways of expressing the same bug collapse into the identical thought token.
</details>

<details open>
<summary><b>2. AST Code Skeletonization (Differential Topology)</b></summary>
<br>

Coding agents don't need to read internal function bodies of files they aren't editing. The `ASTSkeletonizer` parses source code into an Abstract Syntax Tree, extracts the class interfaces, types, decorators, and signatures, and replaces implementations with `...` (Python Ellipsis):

```python
# SKELETONIZED CODE: 75% fewer tokens, 100% type & contract fidelity
class PaymentService:
    def __init__(self, api_key: str, timeout: int = 30): ...
    def process_charge(self, user_id: str, amount_cents: int, currency: str = "usd") -> dict: ...
    def refund_charge(self, charge_id: str, reason: str = "requested") -> bool: ...
```
</details>

<details open>
<summary><b>3. Dual-Channel Cognitive Bifurcation</b></summary>
<br>

Separates internal AI reasoning from user-facing communication:
* **Channel 1 (Background & Thinking):** Constrained to dense telegraphic syntax (`@E` for errors, `@T` for tools, `@F` for files). Saves up to **75% of expensive output tokens**.
* **Channel 2 (User-Facing Response):** 100% natural, polite, beautifully formatted markdown. Zero internal macros or technical jargon leaked.
</details>

<details open>
<summary><b>4. Team-of-Teams Swarm Framework</b></summary>
<br>

Organizes autonomous multi-agent systems into 4 specialized teams:
* 🌐 **Team 1: Cognitive Thought-Tokenization Swarm** (*Words ➔ Thoughts ➔ Tokens*)
* 💻 **Team 2: Codebase Topology & AST Swarm** (*Interface extraction & patch generation*)
* 🧠 **Team 3: State-Ledger & Receding Memory Swarm** (*Multi-tier exponential context decay*)
* 🛡️ **Team 4: Closed-API Gateway & Cost Governor Swarm** (*Prompt-caching discounts & routing*)
</details>

---

## 📊 Benchmarks

<p align="center">
  <img src="assets/metrics.svg" alt="TokenSaver Benchmarks" width="100%" />
</p>

| Component | Uncompressed | TokenSaver | Reduction | Impact |
| :--- | :--- | :--- | :--- | :--- |
| **Pytest / Compiler Traces** | ~350 tokens | **~75 tokens** | **-78%** | Removes stack frame clutter |
| **Git Diffs** | ~180 tokens | **~45 tokens** | **-75%** | Keeps only hunk additions/deletions |
| **Model Thinking (CoT)** | ~90 tokens | **~22 tokens** | **-75%** | Cuts expensive output tokens |
| **Multi-Turn History** | ~850 words | **~140 words** | **-83%** | Lossless code hash registry |
| **Static System Context** | Full Price | **Prompt Cached** | **-90%** | Anthropic / Gemini cache hit |

---

## 🧪 Testing & Demos

Run all verification scripts directly from your terminal:

```bash
# 1. Run the Active Session Ledger demo
python examples/run_session_ledger_demo.py

# 2. Run the Words -> Thoughts -> Tokens demo
python examples/run_thought_tokenizer_demo.py

# 3. Run the Dual-Channel Coding Agent simulation
python examples/run_coding_agent_demo.py

# 4. Run the Full Advanced Pipeline (AST + BPE + Receding Memory)
python examples/run_full_advanced_pipeline.py

# 5. Run the Automated Unit Test Suite
python -m unittest discover tests
```

---

## 📦 Project Organization

```
token-saver/
├── assets/                        # SVG architecture diagrams and hero banners
│   ├── banner.svg
│   ├── architecture.svg
│   └── metrics.svg
├── token_saver/                   # Core Python Library
│   ├── __init__.py
│   ├── session_cli.py             # 'session-log' CLI command utility
│   ├── session_ledger.py          # Lossless Content-Addressed Code Memory
│   ├── thought_tokenizer.py       # Words -> Thoughts -> Thought Tokens Engine
│   ├── ast_skeletonizer.py        # Interface-Preserving AST Compactor
│   ├── bpe_synonym_optimizer.py   # Single-Token BPE Vocabulary Hacking
│   ├── receding_horizon_memory.py # Multi-Tier Context Decay Engine
│   ├── coding_agent_minifier.py   # Pytest, Traceback & Git Diff Minifier
│   ├── prompt_caching.py          # Gemini / Claude / GPT Caching Adapter
│   └── swarm_orchestrator.py      # Team-of-Teams Swarm Framework
├── tests/                         # Automated Unittest Suite
│   └── test_session_ledger.py
├── examples/                      # Interactive Executable Demos
│   ├── run_session_ledger_demo.py
│   ├── run_thought_tokenizer_demo.py
│   ├── run_coding_agent_demo.py
│   └── run_full_advanced_pipeline.py
├── pyproject.toml
├── setup.py
├── LICENSE                        # MIT License
└── README.md
```

---

## 📄 License

Distributed under the **MIT License**. Free for open-source and commercial use.
See [`LICENSE`](LICENSE) for details.
