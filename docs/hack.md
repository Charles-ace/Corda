# HACK.md — Pacta

**Project:** Pacta
**Tagline:** Pacta turns protocol rules written in plain English into verifiable on-chain adjudications.
**Event:** GenLayer Agent Tank Hackathon (Sept 2026)
**Track:** Autonomous Protocols
**Repository Root:** `c:\Builds\Genlayer`

---

## 1. The Core Wedge & Problem

Protocols publish high-minded operational promises in English:
- *"Emergency maintenance calls will never exceed 1.0 ETH without a 48h timelock."*
- *"Treasury reserves are strictly allocated to audited yield adapters, never to unverified contracts or EOAs."*
- *"Protocol fees remain capped at 0.3%."*

When protocols violate these rules, the only recourse today is an angry tweet, a forum post, or a medium article. Centralized monitors can be censored, and traditional smart contracts cannot read English documents or evaluate qualitative commitments.

Pacta gives the ecosystem an **on-demand, autonomous, decentralized adjudication engine**. Anyone provides:
1. The Protocol Name
2. The Link to the Published Rule Document
3. The Target Sepolia Transaction Hash

GenLayer independent validators reach consensus on whether the transaction breached the rule, producing a permanent, un-censorable on-chain verdict: **COMPLIANT**, **VIOLATION**, or **UNCLEAR**.

---

## 2. Technical Stack & Architecture

- **Intelligent Contract:** Python contract on GenVM (`Pacta.py`).
- **Web Evidence Fetching:** `gl.nondet.web.get()` fetching live markdown/HTML rules.
- **On-Chain Evidence Fetching:** `gl.nondet.web.get()` querying the public Blockscout v2 REST API for Ethereum Sepolia (`https://eth-sepolia.blockscout.com/api/v2/transactions/{tx_hash}`).
- **Equivalence Principle:** `gl.eq_principle.strict_eq()` enforcing byte-for-byte agreement across independent validator nodes.
- **Frontend / Proof Room:** React + Vite + Tailwind CSS zero-wallet verification interface.

---

## 3. Demo Cases (Adversarial Validation)

- **Case A (COMPLIANT):**
  - Rule: Treasury emergency transfer threshold <= 1.0 ETH.
  - Transaction: Real Sepolia transfer of 0.2 ETH.
  - Expected Verdict: `COMPLIANT`.
- **Case B (VIOLATION):**
  - Rule: Treasury emergency transfer threshold <= 1.0 ETH.
  - Transaction: Real Sepolia transfer of 2.5 ETH.
  - Expected Verdict: `VIOLATION`.
- **Case C (UNCLEAR):**
  - Rule: Ambiguous / unevidenced condition.
  - Transaction: Unrelated contract interaction.
  - Expected Verdict: `UNCLEAR` (strict adherence to Section 5: never guess missing facts).
