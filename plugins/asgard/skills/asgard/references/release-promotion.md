# Hermod Release Promotion

Read this reference before dispatching Hermod. Hermod promotes an Odin-approved delivery through Git hosting and observes deployment performed by repository Actions. Hermod does not accept the delivery, change product code to repair failures, or deploy directly.

## Required authority and input

Odin must provide the repository, approved delivery branch and revision, authoritative version artifacts, branch policy, required checks and reviews, release-note source, and explicit authority for each applicable operation: commit, push, pull-request creation, merge, tag creation, GitHub Release creation, and CI monitoring. Missing authority stops before the affected mutation.

The repository must be clean. Confirm remote state immediately before every mutation and bind CI evidence to the current pull-request or merge revision. Never rely on a successful check for an older revision.

## GitHub command policy

Use the GitHub CLI for every GitHub integration. Start by requiring `gh auth status` to succeed for the intended host and account. Prefer `gh api` with explicit REST or GraphQL endpoints for pull requests, reviews, required checks, workflow runs, merge operations, tags, and releases. Use focused commands such as `gh run view`, `gh pr`, or `gh release` only when they provide a clearer supported operation than the API endpoint.

Use `git` for repository operations such as status, fetch, branch creation, commits, tags, and push; do not use a browser, connector, or a different API client as a silent fallback for failed `gh` authentication or authorization. Stop and report the failed `gh` command, sanitized response, host, account, and required scope. Paginate collection endpoints when the complete result affects a decision, and re-read the pull-request head SHA and required-check state immediately before merging.

## State machine

```text
DELIVERY_APPROVED
  -> DELIVERY_PR_OPEN
  -> DELIVERY_CI_PASSED
  -> DELIVERY_MERGED_TO_DEVELOP
  -> VERSION_SUGGESTED
  -> AWAITING_VERSION_DECISION
  -> RELEASE_BRANCH_CREATED
  -> APPLICATION_VERSION_UPDATED
  -> RELEASE_PR_OPEN
  -> RELEASE_CI_PASSED
  -> RELEASE_MERGED_TO_MASTER
  -> VERSION_TAGGED
  -> PRODUCTION_ACTIONS_RUNNING
  -> PRODUCTION_DEPLOYED
  -> GITHUB_RELEASE_PUBLISHED
  -> BACKPORT_DISCOVERED
  -> BACKPORT_CI_PASSED
  -> BACKPORT_MERGED_TO_DEVELOP
  -> RELEASE_COMPLETE

Any failure -> BLOCKED -> REPORT_TO_ODIN
```

Resume idempotently from observed repository state. Do not duplicate branches, pull requests, tags, or releases. Treat an ambiguous match as a blocker.

## Delivery integration

Delivery branches originate from `develop` and target `develop`. Prefer squash merge. Before merging, inspect whether the branch is an active base for dependent branches. When squash would destroy ancestry required by those branches, use a merge commit. If protections do not allow the safe method, stop and report; do not rebase or force-push dependent branches automatically.

Merge only when the pull request is not a draft, has no conflicts, satisfies required reviews, is current when required, passes every required check for its current revision, and the provider reports it mergeable. Pending, failed, cancelled, or timed-out required checks block the merge.

## Version decision

After merging the delivery, synchronize local `develop` and analyze only the approved delivery. Recommend:

- `major` for incompatible public behavior, contract, or data changes;
- `minor` for backward-compatible functionality;
- `patch` for backward-compatible fixes or internal improvements.

Show the current version, recommended increment and result, confidence, evidence, and the resulting major, minor, and patch alternatives. Stop at `AWAITING_VERSION_DECISION`; the user always chooses the increment.

After the choice, create `release/<major.minor.patch>` from synchronized `develop`. Update only authoritative version artifacts and required generated counterparts, validate that the application reports the chosen version, and use a Conventional Commit such as `chore(release): bump version to 1.2.3`.

## Master promotion, tag, and release

Release branches originate from `develop` and target `master`. Always merge release pull requests with a merge commit after their current-revision gates pass.

Create `v<major.minor.patch>` for the exact master merge revision and never move or reuse a published version tag. Respect the repository trigger: publish the tag before monitoring when the tag starts packaging or deployment. Publish the GitHub Release as stable only after required production Actions succeed, with notes derived from the approved delivery. If deployment fails after tagging, report and leave the immutable tag in place; a correction receives a new version.

Repository Actions own package generation, publication, and environment deployment. Hermod only monitors them. A master merge is not deployment success.

## CI-created backport

After production publication, discover the pull request created by CI directly from `master` to `develop` using reliable workflow output, version, revision, and repository metadata. Confirm both branches belong to the same repository, the head is the published `master` revision, and the changes return production state without unrelated divergence. Multiple plausible matches or a missing backport after the configured monitoring window block promotion.

Apply the ordinary `develop` merge rule, normally squash, after all backport gates pass. Synchronize local `develop` and verify its application version equals production before declaring `RELEASE_COMPLETE`.

## Failure report

On a definitive failure, stop and return:

```yaml
agent: Hermod
status: BLOCKED
phase: DELIVERY_PR | RELEASE_PR | TAG | PRODUCTION_DEPLOY | GITHUB_RELEASE | BACKPORT
repository: owner/repository
version: value | not selected
pull_request: url | not applicable
revision: sha
workflow: name | not applicable
job: name | not applicable
failed_step: value | unknown
workflow_run: url | not applicable
classification: application | test | build | deployment | infrastructure | permission | timeout | cancelled | ambiguous | unknown
summary: concise observed cause
evidence: short sanitized evidence
retry_possible: true | false | unknown
recommended_owner: Brokkr | Sindri | Ymir | Odin | repository-maintainer
```

Never reproduce credentials, tokens, personal data, or unnecessary exploit details. A transient-looking failure may justify recommending a rerun, but Hermod does not rerun automatically unless that exact retry authority and a bounded retry policy were supplied.

## Completion record

Return the selected version; delivery, release, and backport pull-request URLs and merge revisions; master release revision; tag and GitHub Release URLs; production workflow and deployed revision; synchronized develop revision and version; merge methods; residual risks; and excluded operations not performed.
