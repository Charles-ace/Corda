# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *
import json

class Corda(gl.Contract):
    """
    Corda Intelligent Contract:
    Checks whether an open-source AI framework's public privacy/marketing claims match what its public code appears to do.
    Uses GenLayer web access + multi-validator comparative consensus.
    """
    reports: TreeMap[u256, str]
    report_count: u256

    def __init__(self):
        self.report_count = u256(0)

    @gl.public.write
    def analyze(self, repo_url: str, privacy_url: str) -> str:
        def evaluate_claim():
            def extract_text(resp) -> str:
                if hasattr(resp, "body"):
                    b = resp.body
                    if isinstance(b, bytes):
                        return b.decode("utf-8", errors="ignore")
                    return str(b)
                if hasattr(resp, "text"):
                    return str(resp.text)
                return str(resp)

            # 1. Fetch privacy claim page
            raw_privacy = gl.nondet.web.get(privacy_url)
            privacy_text = extract_text(raw_privacy)

            # 2. Fetch code/manifest evidence from repository
            code_evidence = ""
            if "raw.githubusercontent.com" in repo_url or "gist.githubusercontent.com" in repo_url or repo_url.endswith(('.py', '.json', '.toml', '.txt', '.md')):
                raw_code = gl.nondet.web.get(repo_url)
                code_evidence = extract_text(raw_code)
            else:
                base_raw = repo_url.replace("github.com", "raw.githubusercontent.com").rstrip("/")
                probes = [
                    "/main/package.json",
                    "/main/pyproject.toml",
                    "/main/telemetry.py",
                    "/master/package.json",
                    "/master/telemetry.py"
                ]
                for probe in probes:
                    try:
                        raw_probe = gl.nondet.web.get(base_raw + probe)
                        probe_text = extract_text(raw_probe)
                        if probe_text and len(probe_text.strip()) > 0 and "404" not in probe_text[:50]:
                            code_evidence += f"\n--- File: {probe} ---\n" + probe_text[:2000]
                    except Exception:
                        pass
                if not code_evidence:
                    code_evidence = "No high-value telemetry or manifest files found in standard repository paths."

            # 3. Prompt LLM to evaluate claim against evidence
            prompt = f"""
You are an impartial auditor analyzing an open-source AI project's public privacy claims versus its public code.

PRIVACY DOCUMENTATION:
\"\"\"
{privacy_text[:3000]}
\"\"\"

PUBLIC CODE EVIDENCE:
\"\"\"
{code_evidence[:4000]}
\"\"\"

TASK:
1. Extract the specific privacy/telemetry claim made in the documentation.
2. Identify any relevant telemetry, tracking, analytics, or network logging dependencies/code in the code evidence (e.g. posthog, segment, mixpanel, telemetry initialization, Sentry, phone-home network calls).
3. Determine the verdict strictly from these three options:
   - DISCLOSURE_MATCH: The code evidence is consistent with the privacy claim (e.g. claim says no telemetry and no telemetry is found, or claim discloses telemetry accurately).
   - DISCLOSURE_MISMATCH: The code evidence contradicts the privacy claim (e.g. claim says 'no telemetry' or 'self-hosted with zero tracking', but code imports or initializes telemetry like PostHog).
   - INSUFFICIENT_EVIDENCE: The evidence is too sparse, missing, or ambiguous to evaluate the claim.

Return your response strictly as valid JSON with no markdown backticks and no additional commentary:
{{
  "verdict": "DISCLOSURE_MATCH" | "DISCLOSURE_MISMATCH" | "INSUFFICIENT_EVIDENCE",
  "claim": "<concise extracted privacy claim>",
  "evidence": "<concise summary of public code evidence with file/library names>",
  "explanation": "<one short explanation of why the evidence conflicts with or matches the claim>"
}}
"""
            raw_response = gl.nondet.exec_prompt(prompt)
            clean_text = raw_response.strip()
            if clean_text.startswith("```"):
                lines = clean_text.splitlines()
                clean_text = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])

            try:
                parsed = json.loads(clean_text)
            except Exception:
                verdict = "INSUFFICIENT_EVIDENCE"
                if "DISCLOSURE_MISMATCH" in clean_text:
                    verdict = "DISCLOSURE_MISMATCH"
                elif "DISCLOSURE_MATCH" in clean_text:
                    verdict = "DISCLOSURE_MATCH"
                parsed = {
                    "verdict": verdict,
                    "claim": "Extracted from provided privacy documentation",
                    "evidence": "Extracted from public code files",
                    "explanation": clean_text[:300]
                }

            if parsed.get("verdict") not in ["DISCLOSURE_MATCH", "DISCLOSURE_MISMATCH", "INSUFFICIENT_EVIDENCE"]:
                parsed["verdict"] = "INSUFFICIENT_EVIDENCE"

            return json.dumps(parsed)

        # 4. Multi-validator comparative consensus
        consensus_result = gl.eq_principle.prompt_comparative(
            evaluate_claim,
            principle="""
            The final verdict must be exactly one of:
            DISCLOSURE_MATCH
            DISCLOSURE_MISMATCH
            INSUFFICIENT_EVIDENCE

            The verdict must be based on the supplied privacy claim
            and the supplied public-code evidence.
            Validators must independently verify that if the documentation claims 'no telemetry'
            and code contains telemetry imports/initializations (such as PostHog), the verdict must be DISCLOSURE_MISMATCH.
            If the documentation claims telemetry is disabled by default / offline-first and no telemetry is in code, the verdict must be DISCLOSURE_MATCH.
            """
        )

        current_id = self.report_count
        self.reports[current_id] = consensus_result
        self.report_count = current_id + u256(1)
        return consensus_result

    @gl.public.view
    def get_report(self, report_id: u256) -> str:
        return self.reports.get(report_id, "{}")

    @gl.public.view
    def get_latest_report(self) -> str:
        if self.report_count == u256(0):
            return "{}"
        return self.reports.get(self.report_count - u256(1), "{}")

    @gl.public.view
    def get_report_count(self) -> u256:
        return self.report_count
