# DESIGN.md — Pacta Design Specification

## System Architecture

```
                      User / Observer / Auditor
                                 │
                                 ▼
                    [ Pacta Proof Room (Frontend) ]
                    - Submit Case (Rule URL + Tx Hash)
                    - Inspect Proof by Case ID
                                 │
                                 ▼
                     [ GenLayer JSON-RPC Node ]
                                 │
                                 ▼
                 [ Pacta Intelligent Contract (GenVM) ]
                                 │
          ┌──────────────────────┴──────────────────────┐
          │                                             │
          ▼                                             ▼
  [ gl.nondet.web.get ]                         [ gl.nondet.web.get ]
  Rule Document (Public Web)            Blockscout Sepolia REST API (Tx JSON)
          │                                             │
          └──────────────────────┬──────────────────────┘
                                 │
                                 ▼
                    [ gl.nondet.exec_prompt ]
                 Semantic Adjudication Prompt:
                 - Natural language rule text
                 - Raw tx parameters (from, to, value, decoded call)
                 - Output: COMPLIANT | VIOLATION | UNCLEAR + reason
                                 │
                                 ▼
                    [ gl.eq_principle.strict_eq ]
                  Multi-Validator Consensus Check
                                 │
                                 ▼
                    [ Contract Storage Commit ]
                     self.cases[case_id] = record
```

## Security & Consensus Invariants

1. **Strict JSON Normalization:** Non-deterministic prompt outputs must be constrained to a normalized JSON schema with exact verdict keys to prevent validator divergence.
2. **Missing Evidence Invariant:** If the transaction data does not contain enough information to decisively prove or disprove the rule, the validator must output `UNCLEAR`. Never extrapolate.
3. **Passive Adjudication Invariant:** The contract only adjudicates and records findings; it never calls external contracts or pauses systems.
