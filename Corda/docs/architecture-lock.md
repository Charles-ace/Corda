# Architecture Lock — Corda

> **Governing System Specification**  
> Formatted in accordance with the Enoch Model / Morrow Standard (`hackathon-unified-master`).

---

## 1. Scope Boundaries

### Explicitly IN Scope
* **Intelligent Contract Protocol**: Authoring, linting, deploying, and executing a GenLayer Intelligent Contract in Python (`Corda.py`) utilizing `gl.nondet.web.get()` and `gl.eq_principle.prompt_comparative()`.
* **On-Chain Studionet Verification**: Deploying to live GenLayer Studionet (Chain ID `61999`), validating multi-validator consensus across decentralized nodes, and achieving `GenVM Result: SUCCESS` (`kind: "return"`).
* **Defensible Verdict Classification**: Strictly resolving three outcomes: `DISCLOSURE_MATCH`, `DISCLOSURE_MISMATCH`, and `INSUFFICIENT_EVIDENCE`.
* **Zero-Wallet Proof Room**: A read-only verification interface allowing judges and auditors to reproduce full on-chain proofs in <60 seconds without connecting a Web3 wallet.
* **Tamper-Evident Receipts**: Real transaction hashes and block explorer verification for both Match and Mismatch scenarios.
* **Automated Audio-Visual Pipeline**: ElevenLabs text-to-speech synthesis, `ffprobe` duration measurement, Remotion React composition rendering (Full HD 1080p, 30fps), and automated QA verification.

### Explicitly OUT of Scope
* **Private / Closed-Source Repositories**: Scraping behind logins, SSH keys, or private enterprise repositories.
* **CAPTCHA / Bot-Gated Endpoints**: Bypassing Cloudflare Turnstile, hCaptcha, or anti-bot defenses.
* **Dynamic JavaScript Scraping**: Running client-side SPAs requiring browser rendering within GenVM nodes (analysis targets raw manifests, raw source files, or static documentation).
* **Escrow / Freelance Marketplace Pools**: No token speculation, staking pools, or synthetic financial instruments.
* **Subjective Marketing Advice**: Corda does not provide prose critique; it asserts factual consistency between stated policy and codebase evidence.

---

## 2. Complete Data Flow & State Mutations

```text
               ┌────────────────────────────────────────────────────────┐
               │              Judge / Security Auditor                  │
               └──────────────────────────┬─────────────────────────────┘
                                          │
                   1. Input Target Gist URLs (or 1-click Preset)
                                          │
                                          ▼
               ┌────────────────────────────────────────────────────────┐
               │       Corda Proof Room UI (Vercel / Local)             │
               │   - Pixel-perfect Nesa dark glassmorphism              │
               │   - 4-Phase Consensus Stepper                          │
               │   - Zero-wallet execution trigger                      │
               └──────────────────────────┬─────────────────────────────┘
                                          │
                  2. POST /api/analyze { repo_url, privacy_url }
                                          │
                                          ▼
 ┌─────────────────────────────────────────────────────────────────────────────────────┐
 │                GenLayer Studionet Intelligent Contract (0x70c2...3e92)               │
 │                                                                                     │
 │  Step A: Non-Deterministic Web Crawl                                                │
 │          raw_privacy = gl.nondet.web.get(privacy_url)                               │
 │          raw_code    = gl.nondet.web.get(repo_url)                                  │
 │                                                                                     │
 │  Step B: Multi-Validator Comparative Consensus                                      │
 │          verdict_raw = gl.eq_principle.prompt_comparative(                          │
 │              prompt=EVALUATION_TASK,                                                │
 │              principle=STRICT_GROUNDING_CRITERIA                                    │
 │          )                                                                          │
 │                                                                                     │
 │  Step C: Tamper-Evident Storage Mutation                                            │
 │          audit_id = self.audit_count                                                │
 │          self.audit_records[audit_id] = serialized_receipt                          │
 │          self.audit_count = audit_id + u256(1)                                      │
 │                                                                                     │
 │  Step D: Return Structured JSON Payload                                             │
 └────────────────────────────────────────┬────────────────────────────────────────────┘
                                          │
               3. Transaction Finalization (5/5 Validators Accepted)
                                          │
                                          ▼
               ┌────────────────────────────────────────────────────────┐
               │                 Finalized Proof Card                   │
               │   - DISCLOSURE_MISMATCH / DISCLOSURE_MATCH             │
               │   - Cited Telemetry Calls (e.g. PostHog)               │
               │   - GenLayer Block Explorer Deep-Link                  │
               └────────────────────────────────────────────────────────┘
```

---

## 3. Component Classification (REAL vs. MOCKED)

| Module / Component | Classification | Ground Truth Justification |
| :--- | :--- | :--- |
| `Corda/contracts/Corda.py` | **REAL** | Syntactically validated against GenVM AST; linter passed; deployed on-chain. |
| Studionet Deployment | **REAL** | Immutably stored at `0x70c2F7491A2CC7f81AC05ca964a059c05feD3e92`. |
| Consensus Execution | **REAL** | Validated with live transactions `0x5452...a099` (Case B) and `0xeb63...018c` (Case A). |
| GenVM Result Status | **REAL** | `GenVM Result: SUCCESS` (`kind: "return"`), verified via block explorer. |
| ElevenLabs Voice Synthesis | **REAL** | Generated using ElevenLabs API (`Adam - Tech Narrator`, 82.85s). |
| Remotion Video Render | **REAL** | 2,486 frames rendered to `Corda/Corda-demo-final.mp4` with audio multiplexing. |
| Vercel Production Serverless | **REAL** | Live serverless endpoint at `https://corda-vert.vercel.app/api/analyze`. |
| Ground-Truth Test Cases | **REAL** | Publicly accessible raw GitHub Gists for Case A and Case B. |
| User Wallet Connection | **OMITTED** | Omitted intentionally to guarantee <60s Zero-Wallet judging path. |

---

## 4. The Morrow Honesty Bar Disclosures

1. **The Atomic Verb**: `invalidate` — Corda invalidates ungrounded privacy claims by contrasting marketing declarations against repository AST reality.
2. **"Delete the Sponsor's Tech" Failure**: If GenLayer is removed:
   - Traditional EVM contracts cannot fetch off-chain URLs or parse natural language.
   - Traditional Web2 servers rely on a single centralized LLM API key, introducing censorship, hallucinations, and single points of failure.
   - Web2 oracles (e.g. Chainlink) only deliver deterministic numbers/feeds, not comparative semantic consensus.
   - Without GenLayer, decentralized consensus on natural language discrepancy is technically impossible.
3. **The Single Sponsor Load-Bearing Primitive**: `gl.eq_principle.prompt_comparative` coupled with `gl.nondet.web.get` running across Byzantine-fault-tolerant validators.
4. **Honest Limitations**:
   - Analyzes publicly visible code repositories and static documents; does not decompile obfuscated binaries or monitor live production network traffic.
   - Round finalization is bounded by Studionet consensus time (~20-40 seconds per transaction).
   - Serves as an objective discrepancy oracle, not as a substitute for formal human legal counsel.
5. **Zero-Wallet Judging Path**: Immediate verification accessible at `https://corda-vert.vercel.app` using pre-loaded Case A and Case B presets.
