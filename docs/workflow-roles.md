# Antigravity Studio — Workflow & Role Assignment (v1.0)

**Companion to `# Antigravity Studio — Master Hackathon Prompt (v1.0 Unified)`. That doc defines WHAT gets produced at each stage.
This doc defines WHO produces it and who checks it. If the two ever conflict, the master prompt
wins on content; this doc wins on sequencing/ownership.**

**One rule underneath everything below: no tool audits its own output.** A tool that generates
an idea, a spec, or code does not get to be the sole check on that same artifact — not because
it's incapable, but because it shares whatever blind spot produced the miss in the first place.
Every stage below routes to a *different* tool for its check than the one that produced it.

---

## Stage-by-stage assignment

### Stage 0-3 (Recon → Kill-Pattern Check → Broad Problem Recon → Candidate Generation)
**Owner: ChatGPT.**
Runs Sections 2-5 of the master prompt. Produces the recon report and 2-4 candidates per track.
Does not self-score, does not rank, does not say "I recommend candidate 2."

### Stage 4 — Mechanical Gate Check (first pass)
**Owner: Antigravity.**
Not a full audit — a fact-check pass on the parts of Gate 2-5 that are sourced/checkable rather
than judgment calls:
- Same-ecosystem collision search (sponsor's GitHub org, Discord, submission list — directly,
  not general web search)
- Required-tech capability verification against current primary docs (does the claimed
  mechanism actually map to a real, documented capability)
- Gate 3 scope-pruning check (does the specific data source actually require login/private
  access, is the external dependency actually bot-detection-prone)

Antigravity reports this as a table — CONFIRMED / COLLISION FOUND / CAPABILITY UNVERIFIED — per
candidate. **This is not a pass/fail verdict on the idea. It's evidence Claude uses at the next
stage.** Antigravity does not decide which candidates advance.

*Trial period note:* this is an untested split — Ace has not previously used Antigravity for
same-ecosystem collision search specifically. Run this in parallel with Claude's own collision
check for the first 1-2 cycles and compare hit rates before trusting Antigravity's table alone
to filter what reaches Claude.

### Stage 4 (cont.) — Judgment Gates + Stage 5 (Adversarial Grill, Honesty Bar)
**Owner: Claude.**
Takes Antigravity's mechanical check + ChatGPT's candidates. Runs the judgment parts of Gate 2
(does the concrete failure actually hold up), the boring-twin test, the adversarial grill, and
the honesty bar. Produces the rejected-idea log. **Does not pick a winner.** Presents survivors,
scars, and open questions to Ace.

### Checkpoint — Ace locks a candidate
**Owner: Ace. Only Ace.** No AI tool's confidence substitutes for this signal, regardless of how
strong a survivor looks after Claude's pass.

### Stage 6 — Architecture Lock
**Owner: Claude drafts, in dialogue with Ace.**
This is Claude's highest-value use of limited free-tier budget — protect this checkpoint over
earlier ones. Antigravity does not draft the spec (it will be building from it — the same
self-audit problem applies to writing the spec you'll later build to your own convenience).
Iterates per Section 8.3 of the master prompt until Ace gives the explicit lock signal.

### Stage 9.1 — Constraint & Capability Confirmation
**Owner: Antigravity drafts the dependency table (it's closest to the actual tooling/SDKs);
Claude reviews it before Ace sees the go/no-go ask.**
This is the second highest-value use of Claude's budget. A wrong CONFIRMED FEASIBLE here is
exactly the failure mode that's already cost build-days — worth a Claude pass even if it means
skipping a Claude re-check somewhere earlier in the pipeline.

### Stage 9 — Build
**Owner: Antigravity.**
Produces code, raw terminal output, REAL/MOCKED classification, evidence per Section 9.4 of the
master prompt. Does not grade its own work — no self-reported PASS.

### Build audit (code/evidence review)
**Owner: Claude, at minimum for:**
- Anything Antigravity marks as a completed milestone before it's treated as demo-ready
- Any REAL/MOCKED reclassification
- The final pre-submission pass (Section 10 of the master prompt: does the reported evidence
  actually support the claims)

**Untested and not yet assigned: ChatGPT as a code/build auditor.** Ace has never used ChatGPT
this way. Do not route build-audit work to ChatGPT as a default just because it's available and
Claude is rationed — that's optimizing for availability over correctness on the exact checkpoint
category where memory shows the cost of being wrong is highest. If ChatGPT is tried here, treat
its first pass as a trial to be compared against a Claude pass on the same evidence, not as a
substitute for one.

---

## The actual reason for this split, stated once so it doesn't need re-litigating per hackathon

Claude is the strongest auditor and the scarcest resource. The split above is not "give Claude
the important-sounding stuff" — it's routing Claude specifically to the two checkpoints where
your own history (pre-merge memory) shows a miss is expensive to recover from: Architecture Lock
and Constraint Confirmation. Everything upstream of those (ideation, mechanical gate-checking) is
routed to tools that are cheap to be wrong with, because Stage 4's gates and Stage 5's adversarial
grill exist precisely to catch an early miss before it costs anything. Protect the scarce resource
for the stage where scarcity would otherwise cause the exact repeat mistake this whole merge was
meant to end.

---

## Quick-reference table

| Stage | Produces | Owner | Checked by |
|---|---|---|---|
| Recon | Recon report | ChatGPT | Antigravity (mechanical) |
| Ideation | 2-4 candidates/track | ChatGPT | — |
| Gate check (mechanical) | Collision/capability table | Antigravity | Claude (trial period only) |
| Gate check (judgment) + adversarial grill | Survivors + rejected log | Claude | Ace (lock decision) |
| Architecture spec | Locked spec | Claude + Ace | Ace (lock signal) |
| Constraint table | Feasibility table | Antigravity | Claude, then Ace (go/no-go) |
| Build | Code + evidence | Antigravity | Claude (milestone/pre-submission) |

**No row has the same tool in both the "Owner" and "Checked by" columns. If you ever find
yourself about to skip a check because "the tool that built it seems confident," that's the
signal to stop, not proceed.**
