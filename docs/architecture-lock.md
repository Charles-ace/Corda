# ARCHITECTURE SPEC (LOCKED) — Pacta

**Status: LOCKED. BUILD AUTHORIZED.**
**Locked Date:** September 17, 2026
**Target Event:** GenLayer Agent Tank Hackathon (Deadline: 15:30 UTC)
**Track:** Autonomous Protocols
**Wedge Type:** Real-Gap / Self-Referential Hybrid

---

## 1. WHAT IT IS

Pacta is an on-demand protocol rule adjudication engine powered by GenLayer. It enables anyone to verify whether a specific on-chain blockchain transaction adhered to a protocol's published natural-language governance rule, policy, or operational charter. Using GenLayer's Equivalence Principle, independent validators fetch the public rule document and the real on-chain transaction data, perform semantic consensus on compliance, and record an immutable, verifiable verdict (COMPLIANT, VIOLATION, or UNCLEAR) on-chain with zero human intervention.

---

## 2. USE CASES / USER FLOWS

1. **Case Submission:** A user (protocol observer, DAO member, or auditor) submits a case:
   `[Protocol Name] + [Public Rule URL] + [Ethereum Sepolia Transaction Hash]`.
2. **On-Chain Adjudication (GenVM):**
   - The Intelligent Contract fetches the published rule document via `gl.nondet.web.get(rule_url)`.
   - The Intelligent Contract fetches the real transaction data via `gl.nondet.web.get(blockscout_api_url)`.
   - Validators execute non-deterministic semantic reasoning via `gl.nondet.exec_prompt(...)` comparing transaction behavior to natural-language invariants.
   - Validators reach strict consensus via `gl.eq_principle.strict_eq`.
   - The verdict (`COMPLIANT` / `VIOLATION` / `UNCLEAR`) and justification are committed to the contract's persistent storage.
3. **Zero-Wallet Proof Room Verification:** Anyone opens the Proof Room for a case ID via URL or search, viewing the exact fetched rule text, the raw transaction parameters, and the on-chain consensus verdict without connecting a Web3 wallet.

---

## 3. COMPONENTS (REAL VS. MOCKED)

- **Frontend (Proof Room):** React + Tailwind application with Case Submission Form and Read-Only Proof Room display. — **REAL**
- **Intelligent Contract (`Pacta.py`):** GenLayer Python contract running on GenVM executing `gl.nondet.web.get`, `gl.nondet.exec_prompt`, and `gl.eq_principle.strict_eq`. — **REAL**
- **Blockchain Data Source:** Ethereum Sepolia Blockscout v2 REST API (`https://eth-sepolia.blockscout.com/api/v2/transactions/{tx_hash}`) queried via HTTP GET. — **REAL**
- **Public Rule Source:** Real live public markdown/HTML documents hosted on GitHub / public web. — **REAL**
- **Testnet Adjudication Cases:** Real Sepolia transactions representing Case A (COMPLIANT) and Case B (VIOLATION). — **REAL**

---

## 4. DATA FLOW

1. **Rule Retrieval:** `gl.nondet.web.get(rule_url)` fetches the verbatim published text.
2. **Transaction Retrieval:** `gl.nondet.web.get("https://eth-sepolia.blockscout.com/api/v2/transactions/" + tx_hash)` fetches raw transaction JSON (from, to, value, decoded call data, status).
3. **Semantic Consensus:** Prompt strictly asks:
   *"Does the transaction comply with the published rule? Do not assume facts not present in evidence. Return COMPLIANT, VIOLATION, or UNCLEAR."*
4. **State Commit:** `self.cases[case_id] = CaseRecord(...)` stores the record permanently.

---

## 5. EXPLICITLY IN SCOPE

- Single-case submission and adjudication flow.
- Direct Blockscout REST API integration via HTTP GET.
- Strict equality validator consensus on normalized JSON verdict.
- Persistent on-chain case registry.
- Read-only Proof Room UI (zero-wallet requirement).
- Two real Sepolia demo cases (Case A: Compliant, Case B: Violation).

---

## 6. EXPLICITLY OUT OF SCOPE

- Continuous / cron / keeper protocol monitoring.
- Native appeal bonds / staking mechanisms.
- Automated protocol pausing or fund-freezing actions (maintains clean anti-collision against AgentMandate).
- Multi-chain support (Sepolia only).
- Wallet connection requirements for proof inspection.
