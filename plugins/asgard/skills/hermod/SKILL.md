---
name: hermod
description: Prepare and open release Pull Requests from develop to master by analyzing the candidate changes, selecting the next Semantic Version, updating the changelog, and validating traceability. Use directly for release PR preparation without invoking Asgard or Odin.
metadata:
  short-description: Prepare and open release Pull Requests
---

# Hermod

Prepare and open a release Pull Request directly. This skill is independent from Asgard and Odin. It owns the bounded preparation of the release candidate and the opening of the Pull Request; merge, tag, publication, deploy, and infrastructure changes remain separate operations.

## Preconditions and authority

Read repository instructions before acting. For GitHub work, use only `gh` and run `gh auth status` before any GitHub operation. If authentication, authorization, scope, or a command fails, report the sanitized failure and stop; do not switch silently to a browser or another client.

Confirm the branch base with the user before creating a branch. Suggest `develop` for this workflow. Never create a branch from an unverified or stale local base, and never commit directly to `develop` or `master`.

Use the repository's documented release policy when it exists. This skill's default workflow is:

- source branch: `develop`;
- release branch: `release/<version>`;
- Pull Request base: `master`;
- release PR merge method: the repository's required method, or a merge commit when its release policy requires one.

Do not merge the Pull Request, create tags, publish GitHub Releases, deploy, mutate infrastructure, run migrations, alter data, install dependencies, or perform destructive actions unless the user separately authorizes that exact operation.

## Analyze the candidate

After the user confirms the base branch, update the local `develop` from its remote and confirm the repository is clean. Compare `develop` with the current `master` revision, using the repository's version source and release policy as the authority.

Inspect the commits, merged Pull Requests, changed files, existing version metadata, and the current changelog needed to explain the candidate. Prefer explicit breaking-change markers and the repository's established commit or PR conventions. Summarize the evidence before choosing the version.

Select the next stable Semantic Version using this precedence:

- `MAJOR` for incompatible public behavior, breaking contracts, or explicit breaking-change markers;
- `MINOR` for backward-compatible functionality added since the current `master` version;
- `PATCH` for backward-compatible fixes, documentation, maintenance, or security corrections without new functionality.

Use the highest applicable increment represented by the candidate. Confirm that the result is valid SemVer and greater than the current stable version. If the evidence is contradictory, the current version cannot be established, or the increment would be ambiguous, stop and ask the user instead of guessing.

## Prepare the release branch

Create `release/<version>` from the updated `develop` only after the base confirmation and version decision. Do not reuse an existing release branch or published version without verifying that it is the exact candidate and that the repository policy permits continuation.

Update `CHANGELOG.md` when it exists. Preserve its existing format, add the selected version and date, include only changes contained in the candidate, and retain real Markdown links and line breaks. Update other version artifacts only when the repository policy or project structure requires them. Do not create a changelog when none exists without user direction.

Inspect the final diff and run only the relevant validation required by the changed artifacts and repository policy. At minimum, verify the version format, branch source and target, changelog entry, issue and Pull Request references, and any repository-provided validation for release metadata.

Use a Conventional Commit for local changes. Push the release branch only when the user requested the Pull Request workflow. Keep credentials, tokens, and unnecessary personal data out of files, command arguments, logs, and reports.

## Open the Pull Request

Open one Pull Request from `release/<version>` to `master` with `gh pr create` after inspecting the final diff. The title must identify the release version. The description must contain:

- the selected version and a concise evidence-based SemVer rationale;
- the changes included in the candidate;
- the changelog and version artifacts updated;
- validations executed and their results;
- relevant risks or unresolved blockers;
- every delivery issue and Pull Request required by repository policy;
- `Closes #<number>` when an associated issue exists and automatic closure is appropriate.

Send the description with Markdown and real paragraph breaks, preferably through `--body-file`. Re-read the created Pull Request and verify its source branch, base branch, title, body, issue references, and current checks.

If checks fail, the candidate revision changes, the branch source or target is wrong, the version is invalid, the changelog is inconsistent, or required traceability is missing, stop and report the exact blocker. Do not merge or repair unrelated implementation through this skill.

## Completion report

Report the issue, release branch, candidate revision, selected version, changed artifacts, Pull Request URL, validations, unresolved risks, and operations intentionally left for separate authorization.
