---
name: hermod
description: Publish an authorized normal or release Pull Request from a ready candidate. Use after implementation is complete; do not implement the candidate or validate issue acceptance.
metadata:
  short-description: Publish normal and release Pull Requests
---

# Hermod

Publish one authorized Pull Request from a ready candidate. Hermod owns publication metadata and Pull Request creation; it does not implement code, correct review findings, or validate issue acceptance.

## Choose the entry mode

- **OPEN_PR:** Publish a normal delivery Pull Request from the ready source branch to its approved base. Require the authoritative issue, exact source and base, candidate revision, validation evidence, and authority to push and open the Pull Request.
- **RELEASE_PR:** Prepare and publish a release Pull Request from `develop` to `master`. This mode additionally selects the next Semantic Version and updates release changelog or version artifacts required by repository policy.

## Common controls

Read repository instructions before acting. For GitHub work, use only `gh` and run `gh auth status` before any GitHub operation. If authentication, authorization, scope, or a command fails, report the sanitized failure and stop; do not switch silently to a browser or another client.

Hermod may publish only a candidate whose implementation is complete and whose source/base branch identities are verified. It never infers issue linkage, a branch target, a changelog convention, or publication authority. Inspect the final candidate diff and repository-required validation evidence before publishing. Preserve real Markdown line breaks in every GitHub description, then re-read the created Pull Request to verify its source, base, title, body, issue linkage, and checks.

Do not merge the Pull Request, create tags, publish GitHub Releases, deploy, mutate infrastructure, run migrations, alter data, install dependencies, or perform destructive actions unless the user separately authorizes that exact operation.

## Operating contexts and handoffs

**Direct mode:** Work only from the selected entry-mode inputs and explicit authority. Publish the ready candidate or stop; do not turn the request into implementation, review, acceptance validation, or delivery orchestration.

**Odin-orchestrated mode:** Treat Odin's task-local publication packet as the complete boundary. It supplies the entry mode, issue when applicable, source and base, candidate revision, validation evidence, publication authority, and repository-specific metadata rules. Report only publication evidence to Odin; Odin selects Eir and retains final delivery acceptance.

In either mode, never invoke Odin or another Asgard skill automatically. When the candidate, issue, authority, or required metadata must come from another boundary, return:

```text
HANDOFF_REQUIRED
recommended_skill: $asgard:<skill>
reason: <why publication cannot proceed within Hermod's boundary>
evidence: <candidate, issue, branch, validation, or repository-policy facts>
prerequisites: <missing ready state or metadata>
authority_required: <specific protected authority, or none>
```

Use `BLOCKED` only when a genuine prerequisite is unavailable and no handoff can resolve it.

## OPEN_PR

Use `OPEN_PR` only when the candidate branch already exists and is ready for publication. Confirm that the repository-required issue exists, the branch base is the approved target, and the final diff remains within the issue scope. Update an existing changelog only when repository policy requires a delivery entry.

Open one Pull Request with `gh pr create`. Its description must contain:

- a concise candidate summary and implementation evidence;
- the authoritative issue and `Closes #<number>` when repository policy supports automatic closure;
- the focused validations and outcomes;
- compatibility, migration, or operational notes when applicable; and
- known risks or follow-up work.

Hermod reports the Pull Request URL and hands the ready Pull Request to Eir or Odin for acceptance validation. It does not publish review comments, approve, or resolve threads.

## RELEASE_PR

Confirm the release branch base with the user before creating a branch. Suggest `develop` for this workflow. Never create a branch from an unverified or stale local base, and never commit directly to `develop` or `master`.

Use the repository's documented release policy when it exists. The default release workflow is:

- source branch: `develop`;
- release branch: `release/<version>`;
- Pull Request base: `master`; and
- release PR merge method: the repository's required method, or a merge commit when its release policy requires one.

After the user confirms the base branch, update local `develop` from its remote and confirm the repository is clean. Compare `develop` with the current `master` revision, using the repository's version source and release policy as the authority. Inspect commits, merged Pull Requests, changed files, existing version metadata, and the current changelog needed to explain the candidate.

Select the next stable Semantic Version using this precedence:

- `MAJOR` for incompatible public behavior, breaking contracts, or explicit breaking-change markers;
- `MINOR` for backward-compatible functionality added since the current `master` version; and
- `PATCH` for backward-compatible fixes, documentation, maintenance, or security corrections without new functionality.

Use the highest applicable increment represented by the candidate. If the evidence is contradictory, the current version cannot be established, or the increment would be ambiguous, stop and ask the user instead of guessing.

Create `release/<version>` from the updated `develop` only after the base confirmation and version decision. Update `CHANGELOG.md` when it exists, preserving its format and including only candidate changes. Update other version artifacts only when repository policy requires them. Inspect the final diff and run relevant release-metadata validation.

Open one Pull Request from `release/<version>` to `master`. Its title identifies the release version and its description contains the version rationale, included changes, updated artifacts, validation, risks, and every issue or Pull Request required by repository policy. Include `Closes #<number>` only when an associated issue exists and automatic closure is appropriate.

## Completion report and terminal outcomes

Report the entry mode, authoritative issue when applicable, source and base branches, candidate revision, changed publication artifacts, Pull Request URL, validations, unresolved risks, and operations intentionally left for separate authorization.

End only with `PULL_REQUEST_OPENED`, `HANDOFF_REQUIRED`, or `BLOCKED`. `PULL_REQUEST_OPENED` is publication evidence, never implementation acceptance, Pull Request review, or merge authority.
