# Review, Completion, and Publication Gates

## Review the same candidate

After the implementer stops editing, bind every review to the same immutable diff or revision. Odin and required specialists may review concurrently when the candidate is stable and capacity permits. Let Odin reject first when obvious incompleteness would make specialist work wasteful.

Mode determines the minimum gate:

- **Lean:** Odin; add Tyr, Loki, or Heimdall only for an identified material risk.
- **Standard:** Odin, Loki, and Heimdall; add Tyr for material rules, contracts, compatibility, persistence, or cross-boundary consistency.
- **Critical:** Odin plus every applicable independent specialist, with explicit negative and security evidence.
- **Release:** the selected delivery gate, followed by Hermod only after final approval and mutation authority.

Independent reviewers remain read-only and must not share the implementer's context as their only evidence. Disclose limitations when genuine independence is unavailable.

## Correct proportionally

Odin confirms actionable findings, groups compatible corrections into one bounded pass, and returns exact scope, affected DoD criterion, expected correction, and required evidence to the original implementer. Reviewers do not silently fix findings.

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

```text
IMPLEMENTER_COMPLETE != APPROVED
APPROVED             != PUBLISHED
CHANGE_OPEN          != INTEGRATED
```

## Publication gate

Applicable repository rules and explicit user authority control commits, pushes, change requests, merges, migrations, deployments, dependencies, infrastructure, tags, releases, and destructive operations. Internal Asgard approval grants none of them.

Use Hermod only for an Odin-approved exact revision with authority recorded for each intended mutation. Read [release-promotion.md](release-promotion.md) for branch policy, current-revision checks, version decision, failure handling, publication, and backport verification.
