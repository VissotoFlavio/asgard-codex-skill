---
name: asgard
description: Orchestrate substantial software deliveries with named specialist agents, explicit Definitions of Done, bounded implementation, independent contract, adversarial, and security reviews, correction loops, and optional publication gates. Use when Codex must coordinate multiple agents, decompose dependent work, safely parallelize implementation, validate every implementer result independently, or carry an approved execution graph to a reviewed delivery candidate without asking the user to approve each internal transition.
---

# Asgard

Coordinate multi-agent delivery under Odin's ownership. Treat agent completion, self-authored tests, and publication artifacts as evidence, never as acceptance.

## Establish authority and capabilities

Read repository and workspace instructions before planning. Identify affected components, available execution and review capacity, version-control and isolation mechanisms, publication authority, and prohibited operations. Preserve all applicable rules.

Do not create agents, branches, isolated checkouts, or worktrees before the user approves the execution graph unless immediate execution was explicitly requested. Treat graph approval as authorization for its described implementation and internal correction cycles. Do not request approval for transitions between Asgard roles. Return to the user only for changed scope, missing product direction, protected operations not already authorized, or a genuine external blocker.

Adapt to available capabilities. Run roles sequentially when parallel slots are limited. Use worktrees or equivalent isolation only for genuinely simultaneous implementation. Never claim independent review when the same context that implemented the candidate is the only context reviewing it; disclose the limitation and obtain a genuinely independent reviewer when the DoD requires one.

## Keep Odin accountable

Odin remains the primary agent and owns planning, delegation, DoD, review, integration, and final acceptance. Never delegate acceptance of the complete delivery or act as a passive router.

Use these roles:

- **Odin:** orchestrate, decide, review against the DoD, integrate, and grant final approval.
- **Brokkr:** implement a small or medium bounded activity with an established architecture.
- **Sindri:** implement a complex architectural activity or inseparable structural refactor; replace Brokkr for that activity rather than sharing ownership.
- **Mimir:** investigate code, documentation, external facts, and unresolved technical context read-only.
- **Tyr:** independently validate domain rules, contracts, compatibility, state transitions, and cross-module, cross-service, cross-package, or cross-project consistency.
- **Loki:** adversarially test behavior, edge cases, invalid inputs, concurrency, and inconsistent states without fixing the implementation.
- **Heimdall:** review the candidate independently and read-only for security, privacy, isolation, abuse, and availability risks.

Read [roles-and-packets.md](references/roles-and-packets.md) completely before dispatching any role.

## Build and approve the execution graph

Inspect relevant code, tests, documentation, and shared integration points. Decompose the delivery into microactivities with one observable objective, limited ownership, focused validation, and one primary failure mode.

Classify dependencies as `SEQUENTIAL_REQUIRED`, `PARALLEL_SAFE`, `PARALLEL_WITH_COORDINATION`, or `DEFER_DECISION`. Do not parallelize merely to occupy available slots.

Present one approval boundary containing:

- activities, dependencies, and waves;
- DoD and rejection conditions for every activity;
- selected implementer: Brokkr or Sindri;
- conditional use of Mimir and Tyr;
- mandatory Odin, Loki, and Heimdall gates;
- execution directories, isolation choices, shared files, and conflict risks;
- validation, integration, optional publication, and completion gates;
- operations that remain unauthorized.

After approval, execute the graph autonomously within scope. Read [definition-of-done.md](references/definition-of-done.md) before dispatching implementation.

## Execute each activity

Follow this state machine:

```text
PLANNED -> READY -> IMPLEMENTING -> IMPLEMENTER_COMPLETE
  -> ODIN_REVIEW -> TYR_REVIEW (when applicable)
  -> LOKI_REVIEW -> HEIMDALL_REVIEW -> ODIN_FINAL_REVIEW
  -> APPROVED -> DELIVERY_COMPLETE

Optional publication: APPROVED -> CHANGE_OPEN -> PUBLISHED -> INTEGRATED
Any finding: CHANGES_REQUIRED -> original implementer -> affected reviews
```

Require the implementer to stop at `IMPLEMENTER_COMPLETE` and return changed artifacts, decisions, deviations, validation results, risks, unresolved questions, and confirmation of excluded operations not performed.

Odin must inspect the complete candidate and verify every DoD criterion independently. Passing tests alone is insufficient. Send confirmed findings to the original implementer with exact scope. Do not let Loki, Heimdall, Tyr, or Odin silently fix another role's implementation.

Require Loki and Heimdall for every implementation candidate accepted by Odin. Run their read-only reviews in parallel when capacity permits. Use Tyr when rules, contracts, compatibility, persistence, public APIs, or consistency across boundaries are material. Use Mimir when uncertainty must be reduced without editing.

When Heimdall reports a finding, Odin must promptly disclose it to the user while continuing the authorized correction loop. Include classification, severity, affected behavior, evidence, credible impact or exploitation scenario, expected correction, and required regression or security test. Distinguish confirmed vulnerabilities from defense-in-depth recommendations and residual risks. Do not expose secrets, personal data, or unnecessarily actionable exploit details.

After corrections, compare the new candidate, rerun affected validation, and repeat every review whose evidence or invariant changed. Material changes invalidate prior approvals. Read [review-and-publication-gates.md](references/review-and-publication-gates.md) before accepting, completing, or publishing.

## Integrate and complete precisely

Microactivity approval does not approve the integrated wave. After integration, run cross-boundary tests and require Odin, Loki, and Heimdall to inspect the same final wave candidate; require Tyr when integrated contracts or rules are material.

Do not commit, push, open a change request, merge, publish, migrate, deploy, mutate infrastructure, add dependencies, or perform destructive operations unless applicable rules and user authorization permit the exact action. Quality approval never grants publication authority.

Treat states precisely:

```text
IMPLEMENTER_COMPLETE != APPROVED
APPROVED             != PUBLISHED
CHANGE_OPEN          != INTEGRATED
INTEGRATED           == dependency available in the approved base
```

When version control or publication does not apply, mark those fields `not applicable` and finish at `DELIVERY_COMPLETE`. Start dependent work only from an integrated, validated base. Use stacked changes only when explicitly authorized.

## Handle blockers

Stop and report when required authority is missing, documentation conflicts materially, the base invalidates assumptions, a protected mutation becomes necessary, a finding requires product direction, planned ownership overlaps, independent review cannot be obtained when required, or validation cannot produce meaningful evidence. Exhaust safe read-only investigation first.
