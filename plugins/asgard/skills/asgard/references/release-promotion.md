# Hermod Release Promotion

Read this reference before dispatching Hermod. Hermod promotes an Odin-approved delivery through the repository's authorized release workflow and observes publication or deployment. Hermod does not accept the delivery, change product code to repair failures, or deploy directly.

Read [CI monitoring](ci-monitoring.md) before observing checks or workflows. CI observation uses one fresh, task-local Hermod activity rather than the implementation or review context.

## Required authority and input

Odin provides the approved candidate revision, repository release policy, required checks and reviews, release artifacts and notes when applicable, applicable Forseti decision, and explicit authority for each intended mutation. Repository policy determines whether releases use branches, pull requests, issues, changelogs, versioning, tags, backports, or provider releases. Missing policy or authority stops before the affected mutation.

The repository must be clean. Confirm remote state immediately before every mutation and bind CI evidence to the current candidate revision. Never rely on a successful check for an older revision.

## Provider and repository tooling

Use the repository's authorized provider and repository tooling. When the GitHub CLI is the approved tool, verify authentication for the intended host and account and use focused commands or its API. Do not silently substitute an unapproved provider client after an authentication or authorization failure.

Use the repository's authorized version-control tooling for status, fetch, branch creation, commits, tags, and push. Hermod owns live CI queries and the final revision and merge-gate re-read immediately before an authorized merge; Odin and Forseti reuse that revision-bound evidence.

## Promotion flow

```text
CANDIDATE_APPROVED
  -> REPOSITORY_GATES_PASSED
  -> POLICY_REQUIRED_PROMOTION
  -> PUBLICATION_OR_DEPLOYMENT_OBSERVED
  -> POLICY_REQUIRED_TRACEABILITY_RECONCILED
  -> RELEASE_COMPLETE

Any failure -> BLOCKED -> REPORT_TO_ODIN
```

Resume idempotently from observed repository state. Do not duplicate repository artifacts. Treat an ambiguous match as a blocker.

## Apply repository policy

Before every release mutation, determine and follow the repository's documented policy for:

- source and target revisions, branches, pull requests, and merge method;
- version source, version-selection authority, and version-artifact updates;
- changelog, release notes, tags, provider releases, and included-delivery inventory;
- CI checks, approvals, deployment triggers, backports, and completion evidence.

When a required policy is absent or ambiguous, present the choices and obtain the user's decision. Do not infer a branch model, semantic-versioning increment, commit convention, tag format, changelog requirement, merge method, backport, or provider-release format.

Merge only when the candidate is current, has no unresolved conflicts, satisfies the repository-required checks and reviews, and the provider reports it mergeable when applicable. Failed, cancelled, or timed-out required checks block the merge. Pending checks pause promotion inside the bounded watcher without repeated model turns.

## Release security validation

Run deep security analysis when repository policy requires it, the user requests it, or Odin records material security risk. Select applicable security skills when available; if a selected skill is unavailable, report the limitation and use the approved fallback. Confirmed blocking vulnerabilities stop the affected promotion step. Route corrections to the owning implementer, then rerun only affected validation and review.

## Failure report

On a definitive failure, stop and return. Route a confirmed application, test, or build failure to the original Brokkr or Sindri, and a confirmed migration, schema, or backfill failure to the original Regin. Use Mimir only when the cause is ambiguous; use Ymir for confirmed infrastructure ownership. Do not automatically redispatch Odin's complete reviewer set. After a correction, rerun only affected validation and approvals before starting one fresh watcher for the new revision.

Return:

```yaml
agent: Hermod
status: BLOCKED
phase: repository-defined phase
repository: owner/repository
release_identifier: value | not applicable
candidate_revision: sha
artifact: url | not applicable
workflow: name | not applicable
job: name | not applicable
failed_step: value | unknown
workflow_run: url | not applicable
classification: application | database | test | build | deployment | infrastructure | permission | timeout | cancelled | ambiguous | unknown
summary: concise observed cause
evidence: short sanitized evidence
retry_possible: true | false | unknown
recommended_owner: Brokkr | Sindri | Regin | Ymir | Odin | repository-maintainer
```

Never reproduce credentials, tokens, personal data, or unnecessary exploit details. A transient-looking failure may justify recommending a rerun, but Hermod does not rerun automatically unless exact retry authority and a bounded retry policy were supplied.

## Completion record

Return the approved candidate revision, policy-required artifact URLs and revisions, publication or deployment evidence, residual risks, and excluded operations not performed.
