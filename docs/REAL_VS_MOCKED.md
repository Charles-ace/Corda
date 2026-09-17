# REAL vs. MOCKED Classification — Corda

## Status: REAL GENLAYER DEPLOYMENT & CONSENSUS VERIFIED

| Component | Status | Description & Evidence |
| :--- | :--- | :--- |
| **GenVM Contract Syntax & Typing** | **REAL / VERIFIED** | `Corda/contracts/Corda.py` uses official `TreeMap[u256, str]`, `u256`, `gl.nondet.web.get`, and `gl.eq_principle.prompt_comparative`. Passed official GenLayer linter (`genvm-lint lint` -> `✓ Lint passed (3 checks)`). |
| **Contract On-Chain Deployment** | **REAL / VERIFIED** | Deployed to GenLayer Studionet (Chain ID 61999) via GenLayer Studio. Contract Address: `0x70c2F7491A2CC7f81AC05ca964a059c05feD3e92`. Deployment TX: `0xad4a52ec806c702aade32fcece1816b99c2dd0ad1625750ea70c803a5ca0690a` (Status: `FINALIZED`). |
| **Multi-Validator Consensus Execution** | **REAL / VERIFIED** | Executed live multi-validator comparative consensus (`gl.eq_principle.prompt_comparative`) on Studionet. Both write transactions finalized with `GenVM Result: SUCCESS` (`kind: "return"`) and zero execution errors. |
| **Case B (MISMATCH) Execution** | **REAL / VERIFIED** | TX Hash: `0x5452df20d06d17850778e6a254fe9606944f0d8bb0da050faefe2fd33de0a099`. Status: `FINALIZED`, GenVM Result: `SUCCESS` (`kind: "return"`). Inputs: CloudSwarm "100% private / no telemetry" claim vs PostHog telemetry in code. Verdict: `DISCLOSURE_MISMATCH`. |
| **Case A (MATCH) Execution** | **REAL / VERIFIED** | TX Hash: `0xeb63270182d1999633cf71922261ff9e28d8411216019fa0f5e33fd7656c018c`. Status: `FINALIZED`, GenVM Result: `SUCCESS` (`kind: "return"`). Inputs: LocalAgent "Telemetry disabled by default" claim vs clean local code. Verdict: `DISCLOSURE_MATCH`. |
| **Transaction Receipts & Explorer** | **REAL / VERIFIED** | Verified against GenLayer Studio block explorer at `https://explorer-studio.genlayer.com/address/0x70c2F7491A2CC7f81AC05ca964a059c05feD3e92`. |
| **Public Evidence Fixtures** | **REAL / VERIFIED** | Hosted publicly on GitHub Gists (`gist.githubusercontent.com/Charles-ace/9cd83066dca0a7d5081f3a1eae4763a3` and `gist.githubusercontent.com/Charles-ace/3da2ae80f931867f18df331549a287bf`). |
| **Proof Room Web Interface** | **REAL / CONNECTED** | Active proof room UI running on `http://localhost:8080` linked to real Studionet contract and transaction explorer proofs. |
| **End-User Wallet Requirement** | **OMITTED BY DESIGN** | Zero-wallet interface for end users; transactions executed without MetaMask friction. |
