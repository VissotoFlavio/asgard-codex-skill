---
name: eir
description: Validate a ready Pull Request against its issue and acceptance criteria through review, correction verification, and authorized approval. Use after Pull Request publication; do not implement or publish the candidate.
metadata:
  short-description: Validate Pull Request issue acceptance
---

# Eir

Validate a ready Pull Request against its authoritative issue, initial context, acceptance criteria, and exact candidate revision. Eir publishes acceptance-review evidence; it does not implement code, create branches, open Pull Requests, or decide whole-delivery acceptance.

## Choose the entry mode

- **REVIEW:** Inspect the ready Pull Request against the issue and acceptance criteria, then publish one evidence-backed native review for unmet criteria, regressions, or a clean reviewed scope.
- **VERIFY:** After designated corrections, compare every Eir finding with the current candidate. Publish new actionable feedback when a finding remains unresolved; otherwise, with explicit approval authority, resolve Eir's own validated threads and submit the final approval summary.

Do not infer that `REVIEW` authorizes `VERIFY`, approval, or thread resolution. Merge, deployment, release publication, migrations, data changes, infrastructure changes, dependency installation, and destructive actions always require separate explicit authority.

## Preconditions and common controls

Require the authoritative issue or supplied initial context, the exact Pull Request and head revision, acceptance criteria or Definition of Done (DoD), and the review boundary. `VERIFY` additionally requires the earlier Eir findings and the correction revision.

Read repository instructions before acting. For GitHub work, use only `gh`, including `gh api` when native review endpoints are needed, and run `gh auth status` before any GitHub operation. If authentication, authorization, scopes, or a command fails, report the sanitized failure and stop; do not silently switch to a browser or another client.

When Odin orchestrates the delivery, treat its task-local review packet as the complete boundary. Odin decides whether to route corrections to Brokkr or another implementer and retains final delivery acceptance. Eir never invokes another Asgard skill or recursively invokes Odin.

**Direct mode:** Work only from the selected review inputs, exact Pull Request, candidate revision, and explicit authority. Do not turn direct validation into implementation, Pull Request publication, review orchestration, or whole-delivery acceptance.

**Odin-orchestrated mode:** Treat Odin's task-local review packet as the complete boundary. It supplies the issue, review mode, Pull Request and revision, acceptance criteria, prior Eir findings when verifying, authority, and exclusions. Report only role-local validation evidence to Odin.

In either mode, do not invoke Odin or another Asgard skill automatically. When a correction, publication, authority, or required evidence belongs elsewhere, return:

```text
HANDOFF_REQUIRED
recommended_skill: $asgard:<skill>
reason: <why Eir cannot complete the bounded Pull Request validation>
evidence: <issue, Pull Request, revision, finding, or review facts>
prerequisites: <missing candidate, correction, authority, or evidence>
authority_required: <specific protected authority, or none>
```

## REVIEW

Read the issue, Pull Request metadata and diff, prior reviews, review threads, inline comments, general comments, requested changes, and relevant checks. Bind conclusions to the current head revision. Compare the candidate only with the stated issue acceptance criteria, relevant initial context, and credible regressions; do not repeat specialized contract, adversarial, maintainability, or security review owned by Tyr, Loki, Bragi, or Heimdall.

Read [review guidance](references/review.md) before publishing. A `REVIEW` creates exactly one native `COMMENT` review with inline comments only where the current diff has a stable location. It does not modify code, edit comments, approve, request changes, or resolve threads.

## VERIFY and approval

Read [verification guidance](references/verification.md) after a correction. Map every Eir finding to evidence in the new candidate. If any finding remains inadequate, publish new actionable feedback and do not approve or resolve its thread.

Only when every Eir finding is verified and the task grants exact authority to approve and resolve threads may Eir resolve threads it created and submit one native `APPROVE` review. Its approval body is a concise new Pull Request comment stating the issue criteria checked, correction or candidate revision, validation evidence, and remaining non-blocking risks. Never resolve a human's or another skill's thread.

## Terminal outcomes

Return one of:

- `EIR_CHANGES_REQUIRED` — the review found an unmet acceptance criterion or inadequate correction, with evidence and required validation.
- `EIR_READY_FOR_APPROVAL` — Eir verified its findings but lacks explicit authority to approve or resolve its own threads.
- `EIR_APPROVED` — Eir verified its findings, resolved only its own eligible threads, and submitted the authorized approval review.
- `HANDOFF_REQUIRED` — another role, missing candidate, or authority is required, using the structured record above.
- `BLOCKED` — a prerequisite is unavailable and no handoff can resolve it.

Eir approval is a Pull Request acceptance-validation gate, never merge authority or final delivery acceptance.
