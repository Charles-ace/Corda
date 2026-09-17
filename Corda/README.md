# Corda

> **Privacy claims vs. public code.**  
> Corda checks whether an open-source AI framework's public privacy and marketing claims match what its public code appears to do.

Built for the **GenLayer Agent Tank Hackathon**.

---

## On-Chain Verified Deployment (GenLayer Studionet)

| Item | Value |
| :--- | :--- |
| **Network** | GenLayer Studionet (Chain ID `61999`) |
| **Contract Address** | [`0x70c2F7491A2CC7f81AC05ca964a059c05feD3e92`](https://explorer-studio.genlayer.com/address/0x70c2F7491A2CC7f81AC05ca964a059c05feD3e92) |
| **Deployment TX** | [`0xad4a52ec806c702aade32fcece1816b99c2dd0ad1625750ea70c803a5ca0690a`](https://explorer-studio.genlayer.com/tx/0xad4a52ec806c702aade32fcece1816b99c2dd0ad1625750ea70c803a5ca0690a) (`FINALIZED`) |
| **Case B (MISMATCH) TX** | [`0x5452df20d06d17850778e6a254fe9606944f0d8bb0da050faefe2fd33de0a099`](https://explorer-studio.genlayer.com/tx/0x5452df20d06d17850778e6a254fe9606944f0d8bb0da050faefe2fd33de0a099) (`FINALIZED`, GenVM Result: `SUCCESS` -> `DISCLOSURE_MISMATCH`) |
| **Case A (MATCH) TX** | [`0xeb63270182d1999633cf71922261ff9e28d8411216019fa0f5e33fd7656c018c`](https://explorer-studio.genlayer.com/tx/0xeb63270182d1999633cf71922261ff9e28d8411216019fa0f5e33fd7656c018c) (`FINALIZED`, GenVM Result: `SUCCESS` -> `DISCLOSURE_MATCH`) |

---

## The Problem

AI projects and frameworks routinely claim:
> *"Self-hosted. 100% private. No telemetry."*

Yet within their repositories, developers frequently discover active telemetry SDKs (`posthog`, `segment`, `sentry_sdk`) or phone-home tracking initialized on startup.

Auditing this today requires manual investigation by security engineers. Traditional smart contracts cannot read natural-language documentation or evaluate non-deterministic code evidence.

**Corda** utilizes GenLayer's Intelligent Contracts to:
1. Retrieve public privacy documentation and repository code manifests via `gl.nondet.web.get()`.
2. Extract the specific privacy claims and identify active telemetry/tracking dependencies.
3. Reach decentralized consensus across validators using `gl.eq_principle.prompt_comparative()`.
4. Publish an immutable, verifiable verdict on-chain.

---

## Defensible Outcomes

Corda is not a legal certification and does not claim to prove absolute "zero telemetry." It operates strictly on defensible outcomes:

* `DISCLOSURE_MATCH`: The public code evidence is consistent with the stated privacy documentation.
* `DISCLOSURE_MISMATCH`: The public code evidence directly contradicts the stated privacy claim (e.g. claims no telemetry, but imports PostHog).
* `INSUFFICIENT_EVIDENCE`: The supplied evidence is missing or inconclusive.

---

## Architecture & Data Flow

```text
Visitor / Auditor
       │
       ▼
[ Corda Proof Room UI ] (http://localhost:8080)
       │  Trigger analyze(repo_url, privacy_url)
       ▼
[ GenLayer Intelligent Contract (Corda.py) ] (0x70c2F7491A2CC7f81AC05ca964a059c05feD3e92)
       │
       ├──► gl.nondet.web.get(privacy_url)
       │    Extracts natural-language privacy claim
       │
       ├──► gl.nondet.web.get(repo_url)
       │    Inspects high-value code files (package.json, telemetry.py)
       │
       ├──► gl.nondet.exec_prompt()
       │    Semantic adjudication of claim vs. code evidence
       │
       └──► gl.eq_principle.prompt_comparative()
            Independent multi-validator consensus on outcome
       │
       ▼
[ On-Chain Report Commit ]
       │  self.reports[report_id] = record
       ▼
[ Proof Room UI Display ]
       - Extracted Claim
       - Detected Code Evidence
       - GENLAYER CONSENSUS: DECISION AGREED
       - Verdict Badge (DISCLOSURE_MISMATCH / DISCLOSURE_MATCH)
       - Transaction / Proof Hash linked to Studionet Explorer
```

---

## Demo Cases

### Case A — MATCH (LocalAgent)
* **Privacy Claim:** *"LocalAgent is designed for completely self-hosted, offline-first execution. Telemetry is disabled by default."*
* **Code Evidence:** Clean local runner, zero telemetry imports or tracking dependencies.
* **On-Chain Transaction:** `0xeb63270182d1999633cf71922261ff9e28d8411216019fa0f5e33fd7656c018c`
* **Consensus Verdict:** `DISCLOSURE_MATCH` (`FINALIZED`, GenVM Result: `SUCCESS`)

### Case B — MISMATCH (CloudSwarm)
* **Privacy Claim:** *"Self-hosted. 100% private. No telemetry. Zero analytics, zero phone-home tracking."*
* **Code Evidence:** Active `import posthog`, `posthog.capture(...)` initialized on task dispatch.
* **On-Chain Transaction:** `0x5452df20d06d17850778e6a254fe9606944f0d8bb0da050faefe2fd33de0a099`
* **Consensus Verdict:** `DISCLOSURE_MISMATCH` (`FINALIZED`, GenVM Result: `SUCCESS`)

---

## Quickstart & Verification

### 1. Run the Empirical Probe Tests
```bash
python Corda/test_probe.py
```
Expected output:
```text
>>> CASE A: PASS (DISCLOSURE_MATCH confirmed)
>>> CASE B: PASS (DISCLOSURE_MISMATCH confirmed)
ALL EMPIRICAL PROBES PASSED SUCCESSFULLY.
```

### 2. Launch the Proof Room Server
```bash
python Corda/server.py
```
Open **[http://localhost:8080](http://localhost:8080)** in your browser.

1. Click **Case B — MISMATCH (CloudSwarm / PostHog)**.
2. Click **ANALYZE**.
3. View the live GenLayer consensus verdict: `DECISION AGREED: DISCLOSURE_MISMATCH` with exact cited code lines, contract address, and explorer transaction link.
4. Click **Case A — MATCH (LocalAgent)** to verify clean disclosure alignment.

---

## Repository Structure

```text
Corda/
├── contracts/
│   └── Corda.py                # Python Intelligent Contract for GenVM (Lint: PASS)
├── fixtures/
│   ├── case_a_privacy.md       # Case A documentation fixture
│   ├── case_a_code.py          # Case A code evidence fixture
│   ├── case_b_privacy.md       # Case B documentation fixture
│   └── case_b_code.py          # Case B code evidence fixture (PostHog telemetry)
├── frontend/
│   └── index.html              # Clean single-page proof room interface
├── docs/
│   └── REAL_VS_MOCKED.md       # Explicit honesty bar classification
├── test_probe.py               # Empirical probe test script
├── server.py                   # Proof room server & API runner
├── studio_driver.py            # Automated CDP driver for GenLayer Studio
├── studio_actions.py           # GenLayer Studio execution & inspection controller
└── README.md
```
