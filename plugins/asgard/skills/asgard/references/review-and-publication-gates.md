# Review, Completion, and Publication Gates

## Review the same candidate

After the implementer stops editing, bind every review to the same immutable diff or revision. Odin and required specialists may review concurrently when the candidate is stable and capacity permits. Let Odin reject first when obvious incompleteness would make specialist work wasteful.

Mode determines the minimum gate:

- **Lean:** Odin; add Tyr, Loki, or Heimdall only for an identified material risk, and consider Brokkr's Bragi recommendation when maintainability is relevant.
- **Standard:** Odin, Loki, and Heimdall; add Tyr for material rules, contracts, compatibility, persistence, or cross-boundary consistency, and record Odin's decision on Brokkr's Bragi recommendation when production code is added or structurally changed.
- **Critical:** Odin plus every applicable independent specialist, with explicit negative and security evidence; consider Brokkr's recorded Bragi recommendation against the candidate's maintenance risk.

Independent reviewers remain read-only and must not share the implementer's context as their only evidence. Forseti's only exception is the authorized, idempotent insertion of an unambiguous closing reference into an eligible delivery pull-request body. Disclose limitations when genuine independence is unavailable.

Every Brokkr completion records `BRAGI_RECOMMENDED` with the candidate, scope, and rationale. It is not a gate and does not invoke Bragi automatically: Odin or the direct requester decides whether the recommendation warrants an independent Bragi review. When selected, dispatch Bragi only after `IMPLEMENTER_COMPLETE` against the stable candidate, never after each edited file. Bragi may consume existing static-analysis evidence but does not start services or rerun broad validations. Its blocking findings require concrete comprehension or maintenance impact; preferences remain non-blocking recommendations.

## Correct proportionally

Odin confirms actionable findings, groups compatible corrections into one bounded pass, and returns exact scope, affected DoD criterion, expected correction, and required evidence to the original implementer. Reviewers do not silently fix findings.

The default budget permits one grouped correction cycle. If material findings remain afterward, Odin stops, records the delta and cause, and proposes a revised graph or explicit budget increase instead of automatically repeating implementer and reviewer loops.

For a designated Pull Request correction, Odin routes each designated review-thread reply to Brokkr as part of the correction contract, with explicit authority to comment on that exact Pull Request and those exact threads. Brokkr corrects the candidate, runs focused validation, and replies to every designated thread before Eir verifies. Eir retains ownership only of verifying, approving, and resolving Eir's own threads; Brokkr does not approve, resolve, or change thread state.

After a correction:

1. compare the candidate with the previously reviewed revision;
2. complete the bounded correction pass, then rerun affected validation once;
3. invalidate only approvals whose evidence or invariant changed;
4. rerun those reviews against the new candidate;
5. let Odin make final acceptance when all required evidence aligns.

Report confirmed vulnerabilities promptly. Consolidate defense-in-depth recommendations and residual risks unless immediate user action is required.

## Avoid duplicate integration gates

Skip a separate integrated-wave review when one activity is the entire delivery and integration creates no new diff, dependency, configuration, generated artifact, or invariant.

When multiple activities are combined, validate and review their integration surface and cross-boundary behavior. Reopen complete activity reviews only when integration changes their prior evidence. Dependent work starts only from the integrated, validated base required by its contract.

## Complete concisely

Record the candidate, DoD result, required approvals, focused validation, deviations, out-of-scope changes, and residual risks. Omit empty fields and repeated leaf-skill guidance. Distinguish precisely:

Reference the candidate revision and bounded paths instead of reproducing its full diff. For passing validation, record the command, conclusion, and artifact or run URL; include output only for a concise failure excerpt. A reviewer approval needs one decision line plus material findings, not a restatement of its leaf-skill guidance or the complete DoD.

```text
IMPLEMENTER_COMPLETE != PUBLISHED
PUBLISHED            != EIR_APPROVED
EIR_APPROVED         != ODIN_ACCEPTED
CHANGE_OPEN          != INTEGRATED
```

## Publication gate

Applicable repository rules and explicit user authority control commits, pushes, change requests, merges, migrations, deployments, dependencies, infrastructure, tags, releases, and destructive operations. Internal Asgard approval grants none of them.

When Pull Request publication is authorized, Hermod opens the ready candidate as a normal or release Pull Request. Eir then validates the ready Pull Request against the authoritative issue and acceptance criteria: `REVIEW` publishes one COMMENT review; `VERIFY` rechecks Eir's own findings after a Brokkr correction and its designated thread replies. Eir may approve only with exact approval authority and may resolve only its own threads with exact resolution authority. Eir approval is never merge authority or Odin's final delivery acceptance.

When traceability policy applies, require Forseti to verify the policy-required artifacts available at that phase before merge or publication.
