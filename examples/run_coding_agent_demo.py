"""
Example: Running a Coding Agent with Compressed Background/Thinking & Natural User Output
Demonstrates how the Dual-Mode Orchestrator saves tokens without degrading user experience.
"""

from token_saver import DualModeOrchestrator, CodingAgentMinifier


def run_demo():
    orchestrator = DualModeOrchestrator(provider="gemini")

    # 1. Realistic User Request
    user_request = (
        "Hey! Could you please take a look at the failing authentication test in our repo "
        "and tell me what went wrong and how we can resolve it?"
    )

    # 2. Realistic Bloated Pytest Tool Output (normally 80+ lines of clutter)
    raw_pytest_output = """
============================= test session starts ==============================
platform linux -- Python 3.11.4, pytest-7.4.0, pluggy-1.2.0
rootdir: /home/runner/work/auth-service
plugins: asyncio-0.21.1, cov-4.1.0
collected 14 items

tests/test_health.py ............                                        [ 85%]
tests/test_auth.py F                                                     [100%]

=================================== FAILURES ===================================
___________________________ test_token_expiration ____________________________

    def test_token_expiration():
        token = generate_expired_token(user_id=42)
>       result = auth_service.verify(token)

src/auth/service.py:112: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'

    def verify(token: str):
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
>       if payload["exp"] < time.time():
E       jwt.exceptions.ExpiredSignatureError: Signature has expired

/usr/local/lib/python3.11/site-packages/jwt/api_jwt.py:198: ExpiredSignatureError
=========================== short test summary info ============================
FAILED tests/test_auth.py::test_token_expiration - jwt.exceptions.ExpiredSignatureError: Signature has expired
========================= 1 failed, 13 passed in 2.14s =========================
"""

    print("=" * 80)
    print("STEP 1: BACKGROUND PREPARATION (Compressing Raw Logs & Prompt Framing)")
    print("=" * 80)
    
    # Check raw log token count approximation
    raw_words = len(raw_pytest_output.split())
    minified_log = CodingAgentMinifier.minify_test_or_build_log(raw_pytest_output)
    minified_words = len(minified_log.split())

    print(f"Raw Pytest Log Words:      ~{raw_words} words")
    print(f"Minified Log Words:         ~{minified_words} words (Saved {round((1 - minified_words/raw_words)*100)}%)")
    print("\n--- Compressed Background Tool Output Passed to Model Context ---")
    print(minified_log)

    # 2. Prepare payload
    payload = orchestrator.prepare_agent_turn(user_request, background_tool_output=raw_pytest_output)

    # 3. Simulated Model Response following the Dual-Mode Contract
    simulated_model_raw_output = """
<thought>
@E[test_auth.py:test_token_expiration: ExpiredSignatureError]
@F[src/auth/service.py:112 verify()]
Root cause: test fixture token exp timestamp < time.time()
@T[fix]: Mock time.time() or refresh fixture exp delta +3600s
@S[diagnosis_complete]
</thought>
<response>
I found the issue causing the failure in `tests/test_auth.py`.

### What Happened
The test `test_token_expiration` failed with an `ExpiredSignatureError` in `src/auth/service.py` at line 112 because the JWT payload has an expiration timestamp in the past.

### How to Fix It
In your test setup (`tests/test_auth.py`), you can either:
1. Increase the token expiration delta in `generate_expired_token` to be dynamic.
2. Use `freezegun` or mock `time.time()` during the test execution.

Let me know if you would like me to apply this fix to the test file!
</response>
"""

    print("\n" + "=" * 80)
    print("STEP 2: MODEL EXECUTION & DUAL-CHANNEL BIFURCATION")
    print("=" * 80)

    thought, user_response = orchestrator.parse_dual_output(simulated_model_raw_output)

    print("\n[CHANNEL 1: COMPRESSED INTERNAL THOUGHT - SAVES REASONING TOKENS]")
    print(thought)

    print("\n[CHANNEL 2: USER-FACING RESPONSE - POLISHED & 100% NATURAL]")
    print(user_response)
    print("=" * 80)


if __name__ == "__main__":
    run_demo()

