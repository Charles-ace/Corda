# REAL_VS_MOCKED.md — Pacta

**Date:** September 17, 2026
**Governing Standard:** Hackathon Serial Winner Playbook (Section 5.3 & 5.4)

| Component | Classification | Verification / Evidence Mechanism |
| :--- | :---: | :--- |
| **GenLayer Contract Logic** | **REAL** | Python contract running on GenVM with `gl.Contract`, state persistence, and public write methods. |
| **Rule Document Retrieval** | **REAL** | `gl.nondet.web.get()` fetching live, unauthenticated public documents over HTTP GET. |
| **Sepolia Transaction Retrieval** | **REAL** | `gl.nondet.web.get()` fetching live transaction JSON from Blockscout Sepolia v2 API (`https://eth-sepolia.blockscout.com/api/v2/transactions/{tx_hash}`). |
| **Validator Consensus** | **REAL** | `gl.nondet.exec_prompt()` + `gl.eq_principle.strict_eq()` enforcing multi-validator consensus across GenLayer nodes. |
| **On-Chain Persistence** | **REAL** | Adjudication cases stored in contract instance state (`self.cases[case_id]`). |
| **Proof Room Frontend** | **REAL** | Read-only React web application displaying fetched rule, transaction evidence, on-chain case ID, and verdict. |
| **Simulated Fallbacks** | **NONE** | Zero simulated or fake fallback data. If an external URL is unreachable or transaction missing, verdict deterministically evaluates to `UNCLEAR`. |
