---
name: asgard
description: Orchestrate substantial software deliveries that benefit from multiple specialist agents, explicit acceptance criteria, and independent risk-based review. Use for coordinated implementation across bounded activities or high-assurance delivery; do not invoke for routine single-file edits or ordinary coding tasks that one agent can safely complete and verify.
---

# Asgard

Coordinate multi-agent delivery under Odin's ownership. Agent reports and passing tests are evidence, never acceptance. Keep the process proportional to delivery risk.

## Establish authority

Read repository and workspace instructions before planning. Identify affected components, available agent capacity, isolation and version-control mechanisms, prohibited operations, and publication authority.

Do not create agents, branches, or isolated workspaces before the user approves the execution graph unless immediate execution was explicitly requested. Graph approval covers its implementation and internal correction cycles, not protected or external mutations. Return to the user for changed scope, missing product direction, unauthorized protected operations, or genuine external blockers.

Odin remains accountable for decomposition, delegation, integration, evidence review, and final acceptance. Never delegate acceptance of the complete delivery or act only as a router.
Read [Odin's packet](references/agents/odin.md) only when a separate orchestration handoff or compact recovery context is needed.

## Select the smallest sufficient mode

Choose once during planning and increase rigor if new risk appears:

- **Lean:** one bounded, low-risk activity with localized impact. Use one implementer and Odin review. Add only reviewers justified by a concrete risk.
- **Standard:** multiple activities or material behavioral risk. Use independent Loki and Heimdall review; add Tyr for material rules or contracts.
- **Critical:** security-sensitive, externally exposed, persistent, concurrent, irreversible, regulated, or broad cross-boundary work. Use all applicable independent gates and strict correction loops.
- **Release:** add Hermod only after the candidate is approved and exact publication authority is recorded.

Do not use Asgard when Lean would merely reproduce ordinary single-agent work without meaningful delegation or independent review.

## Build the execution graph

Inspect only the code and evidence needed to decompose the delivery. Give each activity one observable objective, bounded ownership, focused validation, dependencies, primary failure mode, and rejection conditions. Classify dependencies as `SEQUENTIAL_REQUIRED`, `PARALLEL_SAFE`, `PARALLEL_WITH_COORDINATION`, or `DEFER_DECISION`; do not parallelize merely to fill slots.

Present one concise approval boundary with activities, dependencies, selected mode and implementers, DoD, review routing, isolation, conflict risks, validation, integration, optional publication, and still-unauthorized operations. Read [definition-of-done.md](references/definition-of-done.md) only when constructing the activity contracts.

Classify an activity by discipline only when that classification changes its implementation guidance or required capabilities. For backend work, load the [backend discipline packet](references/disciplines/backend.md). Record each required skill and its availability before graph approval; do not claim that a capability was applied when it is unavailable.

## Dispatch with minimal context

Use Brokkr for bounded implementation and Sindri instead for one inseparable architectural activity. Use Mimir only to resolve a stated uncertainty. Load only the reference for each role actually dispatched:

- [Brokkr](references/agents/brokkr.md) or [Sindri](references/agents/sindri.md)
- [Mimir](references/agents/mimir.md) when investigation is required
- [Tyr](references/agents/tyr.md) for material rules, contracts, compatibility, persistence, or cross-boundary consistency
- [Loki](references/agents/loki.md) for adversarial behavioral review
- [Heimdall](references/agents/heimdall.md) for security, privacy, isolation, abuse, or availability review
- [Hermod](references/agents/hermod.md) only for approved publication or promotion

Do not pass the full conversation by default. Give each agent only its role packet, activity contract, applicable workspace rules, relevant paths or candidate diff, stable dependencies, focused validation, and explicit exclusions. Prefer a fresh or minimal context when the platform supports it.

When a discipline packet requires a skill, explicitly name that skill in the assigned agent's contract and require the agent to use it before making discipline-specific decisions. Repository and user instructions remain authoritative when skill guidance is generic or conflicts with established project conventions.

## Validate once per activity

Defer executable validation until the implementer has completed the activity and inspected the final diff. Run the smallest affected test set once immediately before `IMPLEMENTER_COMPLETE`, not after each edit or internal step. During implementation, prefer read-only inspection and inexpensive static checks that do not rebuild or rerun suites.

Run an earlier test only when it is needed to reproduce the original failure, validate a high-risk assumption before substantial work continues, or satisfy an explicit user or repository requirement. Record the reason so repeated execution does not become the default.

## Review and correct efficiently

The implementer stops at `IMPLEMENTER_COMPLETE`. Odin and required independent reviewers inspect the same immutable candidate. Run them concurrently when the candidate is stable and capacity permits; let Odin review first when rapid rejection is likely to avoid wasted reviews.

Read [review-and-publication-gates.md](references/review-and-publication-gates.md) before accepting a candidate. Route confirmed findings to the original implementer with exact scope and required evidence. Group compatible findings into one bounded correction pass, then rerun only validations and reviews whose evidence or invariant changed. Material changes invalidate affected approvals, not unrelated ones.

Do not repeat an integrated-wave review when there is one activity and integration produced no new diff, dependency, or invariant. For multiple combined activities, review only the integration surface and cross-boundary behavior unless the combined candidate invalidates earlier evidence.

Odin grants final approval only when all required evidence refers to the same candidate. Keep reports delta-focused: decisions, changed artifacts, failed or passed validations, actionable findings, deviations, unresolved risks, and unauthorized operations attempted, if any. Omit empty boilerplate.

## Publish only when authorized

Approval never grants authority to commit, push, open or merge changes, publish, migrate, deploy, mutate infrastructure, add dependencies, or perform destructive operations. For Release mode, read [release-promotion.md](references/release-promotion.md) before dispatching Hermod.

Stop after exhausting safe read-only investigation when required authority, product direction, independent review, or meaningful validation is unavailable.
