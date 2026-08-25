# Review, Completion, and Publication Gates

## Review order

1. Require the implementer to finish editing and provide evidence.
2. Require Odin to inspect the whole candidate and verify the DoD.
3. Require Tyr when the activity materially affects rules, contracts, compatibility, persistence, public APIs, or consistency across boundaries.
4. Require Loki and Heimdall to review the same candidate independently and read-only; run them concurrently when capacity permits.
5. Require Odin to disclose every Heimdall finding to the user with classification, severity, evidence, impact, expected correction, and required test without pausing the authorized correction loop.
6. Route findings through Odin to the original implementer.
7. Compare the corrected candidate, rerun affected validation, and repeat invalidated reviews.
8. Require Odin to make final acceptance only after all required approvals refer to the same candidate.

## Approval integrity

Do not treat an agent report, passing self-authored tests, or the absence of findings in one review as complete acceptance. Record evidence separately from assumptions. Invalidate approval when a material change affects reviewed behavior or invariants. Disclose when independent review cannot be obtained; never simulate it by relabeling the implementer's context.

## Integrated wave gate

After combining approved microactivities, rerun cross-boundary and regression validation. Require Odin, Loki, and Heimdall to inspect the integrated candidate. Require Tyr when integration changes or exercises shared contracts or rules.

## Completion and optional publication record

```text
Activity or wave:
Base revision: value | not applicable
Candidate revision or diff:
DoD satisfied:
Odin approved:
Tyr approved/not applicable:
Loki approved:
Heimdall approved:
Required validation passed:
Documentation synchronized:
Out-of-scope changes:
Residual risks:
Delivery complete:
Commit authorized: yes | no | not applicable
Push authorized: yes | no | not applicable
Change request authorized and target: value | not applicable
Integration authorized: yes | no | not applicable
```

Applicable workspace rules and explicit user authority control commit, push, change requests, integration, migration, deployment, dependency addition, infrastructure mutation, and destructive operations. Internal Asgard approval never grants those permissions.

## Dependency availability

Treat a result as available only after it exists in the validated base used by dependent work. When using Git-style review, this normally means the change is merged and the base is updated. In other environments, use the equivalent approved integration checkpoint. Avoid stacked changes unless explicitly authorized.

## Hermod promotion gate

Use Hermod only after Odin approves the exact candidate and records the permitted repository mutations. Follow [release-promotion.md](release-promotion.md) for the state machine, branch and merge policy, SemVer decision boundary, CI failure packet, tag and GitHub release rules, and CI-created backport verification.

Passing CI does not authorize the next transition by itself. Hermod must also verify the current revision, required reviews, branch protection, source and target policy, mergeability, and its recorded authority. A production deployment is complete only when its required Actions succeed; a release is complete only when the verified backport returns the production version to develop.
