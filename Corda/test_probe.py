"""
Corda Empirical Probe Script (Commit 1 Rule / Validation Test)
Tests the semantic adjudication logic on Case A (MATCH) and Case B (MISMATCH).
"""

import os
import json
import re

def evaluate_claim_simulation(privacy_text: str, code_evidence: str) -> dict:
    """
    Simulates the core semantic evaluation logic of gl.nondet.exec_prompt.
    Checks whether the code evidence contains telemetry/tracking imports/initializations
    and compares them to the privacy claim.
    """
    privacy_lower = privacy_text.lower()
    
    # Inspect code lines for active telemetry SDK imports or initialization calls
    telemetry_patterns = [
        r"\bimport\s+posthog\b",
        r"\bfrom\s+posthog\b",
        r"\bposthog\.capture\b",
        r"\bposthog\.init\b",
        r"\bimport\s+segment\b",
        r"\bimport\s+mixpanel\b",
        r"\bimport\s+sentry_sdk\b",
        r"\bsentry_sdk\.init\b",
        r"\btelemetry\.init\b",
        r"\bimport\s+datadog\b",
    ]
    detected_telemetry = []
    for line in code_evidence.splitlines():
        line_clean = line.strip()
        if line_clean.startswith("#") or line_clean.startswith('"""') or line_clean.startswith("'''"):
            continue
        for pattern in telemetry_patterns:
            match = re.search(pattern, line_clean, re.IGNORECASE)
            if match:
                detected_telemetry.append(match.group(0))

    # Detect privacy claim tone
    claims_no_telemetry = any(phrase in privacy_lower for phrase in [
        "no telemetry", "telemetry is disabled", "zero analytics", "100% private", "offline-first"
    ])

    if detected_telemetry and claims_no_telemetry:
        verdict = "DISCLOSURE_MISMATCH"
        explanation = f"Documentation promises 'No telemetry / 100% private', but code evidence contains active telemetry imports and calls: {', '.join(set(detected_telemetry))}."
        evidence_summary = f"Detected {', '.join(set(detected_telemetry))} in code execution paths."
    elif not detected_telemetry and claims_no_telemetry:
        verdict = "DISCLOSURE_MATCH"
        explanation = "Documentation states telemetry is disabled by default / offline-first, and no telemetry imports or tracking initializations were found in inspected code."
        evidence_summary = "Inspected code files show clean local execution with zero tracking dependencies."
    else:
        verdict = "INSUFFICIENT_EVIDENCE"
        explanation = "The public evidence provided does not contain sufficient telemetry configuration or documentation statements to decisively evaluate disclosure alignment."
        evidence_summary = "Inconclusive evidence in target paths."

    claim_extracted = ""
    for line in privacy_text.splitlines():
        if any(w in line.lower() for w in ["telemetry", "private", "data policy", "promise", "guarantee"]):
            claim_extracted += line.strip() + " "
    if not claim_extracted:
        claim_extracted = privacy_text[:150]

    return {
        "verdict": verdict,
        "claim": claim_extracted.strip(),
        "evidence": evidence_summary,
        "explanation": explanation
    }

def run_tests():
    fixtures_dir = os.path.join(os.path.dirname(__file__), "fixtures")
    
    # --- Case A: MATCH ---
    with open(os.path.join(fixtures_dir, "case_a_privacy.md"), "r", encoding="utf-8") as f:
        case_a_priv = f.read()
    with open(os.path.join(fixtures_dir, "case_a_code.py"), "r", encoding="utf-8") as f:
        case_a_code = f.read()

    result_a = evaluate_claim_simulation(case_a_priv, case_a_code)
    print("\n==========================================")
    print("PROBE TEST — CASE A (EXPECTED: DISCLOSURE_MATCH)")
    print("==========================================")
    print(json.dumps(result_a, indent=2))
    assert result_a["verdict"] == "DISCLOSURE_MATCH", f"Expected DISCLOSURE_MATCH, got {result_a['verdict']}"
    print(">>> CASE A: PASS (DISCLOSURE_MATCH confirmed)")

    # --- Case B: MISMATCH ---
    with open(os.path.join(fixtures_dir, "case_b_privacy.md"), "r", encoding="utf-8") as f:
        case_b_priv = f.read()
    with open(os.path.join(fixtures_dir, "case_b_code.py"), "r", encoding="utf-8") as f:
        case_b_code = f.read()

    result_b = evaluate_claim_simulation(case_b_priv, case_b_code)
    print("\n==========================================")
    print("PROBE TEST — CASE B (EXPECTED: DISCLOSURE_MISMATCH)")
    print("==========================================")
    print(json.dumps(result_b, indent=2))
    assert result_b["verdict"] == "DISCLOSURE_MISMATCH", f"Expected DISCLOSURE_MISMATCH, got {result_b['verdict']}"
    print(">>> CASE B: PASS (DISCLOSURE_MISMATCH confirmed)")
    print("\nALL EMPIRICAL PROBES PASSED SUCCESSFULLY.")

if __name__ == "__main__":
    run_tests()
