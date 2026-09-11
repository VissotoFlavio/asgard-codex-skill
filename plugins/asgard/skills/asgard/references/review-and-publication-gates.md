# Review, Completion, and Publication Gates

## Review the same candidate

After the implementer stops editing, bind every review to the same immutable diff or revision. Odin and required specialists may review concurrently when the candidate is stable and capacity permits. Let Odin reject first when obvious incompleteness would make specialist work wasteful.

Mode determines the minimum gate:

- **Lean:** Odin; add Tyr, Loki, Bragi, or Heimdall only for an identified material risk.
- **Standard:** Odin, Loki, and Heimdall; add Tyr for material rules, contracts, compatibility, persistence, or cross-boundary consistency, and Bragi when production code is added or structurally changed.
- **Critical:** Odin plus every applicable independent specialist, with explicit negative and security evidence; Bragi is required for production-code candidates.
- **Release:** the selected delivery gate, applicable Forseti traceability approval, then Hermod only after final approval and mutation authority.

Independent reviewers remain read-only and must not share the implementer's context as their only evidence. Forseti's only exception is the authorized, idempotent insertion of an unambiguous closing reference into an eligible delivery pull-request body. Disclose limitations when genuine independence is unavailable.

Dispatch Bragi only after `IMPLEMENTER_COMPLETE` against the stable candidate, never after each edited file. Bragi may consume existing static-analysis evidence but does not start services or rerun broad validations. Its blocking findings require concrete comprehension or maintenance impact; preferences remain non-blocking recommendations.

## Correct proportionally

Odin confirms actionable findings, groups compatible corrections into one bounded pass, and returns exact scope, affected DoD criterion, expected correction, and required evidence to the original implementer. Reviewers do not silently fix findings.

The default budget permits one grouped correction cycle. If material findings remain afterward, Odin stops, records the delta and cause, and proposes a revised graph or explicit budget increase instead of automatically repeating implementer and reviewer loops.

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

Record the candidate, DoD result, required approvals, focused validation, deviations, out-of-scope changes, and residual risks. Omit empty fields and repeated role instructions. Distinguish precisely:

Reference the candidate revision and bounded paths instead of reproducing its full diff. For passing validation, record the command, conclusion, and artifact or run URL; include output only for a concise failure excerpt. A reviewer approval needs one decision line plus material findings, not a restatement of its packet or the complete DoD.

```text
IMPLEMENTER_COMPLETE != APPROVED
APPROVED             != PUBLISHED
CHANGE_OPEN          != INTEGRATED
```

## Publication gate

Applicable repository rules and explicit user authority control commits, pushes, change requests, merges, migrations, deployments, dependencies, infrastructure, tags, releases, and destructive operations. Internal Asgard approval grants none of them.

Use Hermod only for an Odin-approved exact revision with authority recorded for each intended mutation. When traceability policy applies, require Forseti to verify the issue, provider-recognized closing relationship, pull request, changelog, and release inventory available at that phase before merge or publication. Read [release-promotion.md](release-promotion.md) for branch policy, current-revision checks, version decision, failure handling, publication, and backport verification.
