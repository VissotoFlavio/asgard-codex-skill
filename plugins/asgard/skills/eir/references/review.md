# Review and correction contract

Use this reference for `REVIEW` and `CORRECT`.

## Evidence to collect

Read the issue, current Pull Request metadata and diff, prior reviews, review threads, inline comments, general comments, requested changes, and relevant CI checks through `gh`. Bind the review to the current head revision and locate each existing comment or new finding in the current code before deciding whether it remains applicable.

For each existing comment or new finding, record:

- identifier or URL, author when applicable, file, and line when available;
- original concern or observed behavior and the affected invariant;
- current-code evidence;
- classification: accept, clarify, reject with technical evidence, already resolved, obsolete, or out of scope;
- severity and whether it blocks approval;
- required correction or response; and
- validation needed.

Do not accept a comment merely because it is written by a reviewer. Do not reject it merely because the implementation passes tests. Resolve disagreements with the issue, repository policy, contracts, runtime behavior, and focused evidence.

## Publish an authorized review

Before publishing, confirm the exact Pull Request and head revision, deduplicate against existing open feedback, and complete the analysis. Do not publish in a preview or dry-run request.

Create exactly one native Pull Request review with the `COMMENT` event. The review must contain:

- an inline comment for every new actionable finding that has an exact, current diff location;
- a Markdown summary that states the review scope, candidate revision, classified existing feedback, findings without a safe inline location, and the overall recommendation; and
- for each actionable finding, severity, impact, concrete evidence, and recommended action.

Use `gh api` when inline review comments or their replies are required. Do not create a synthetic file/line location, duplicate an existing finding, approve, request changes, edit existing comments, or resolve a thread. If there are no actionable findings, still publish the single `COMMENT` review summary with the reviewed scope and conclusion.

Re-read the published review and every inline comment. Confirm the Pull Request number, revision, Markdown body, and file/line target for inline comments before reporting completion.

## Correction pass and replies

Only enter `CORRECT` when the user authorizes implementation. Group compatible accepted findings into one bounded pass and preserve the issue's scope. Ask for a decision when a comment changes product behavior, public contracts, persistence, security posture, or the issue's scope.

After correction:

- run only validations affected by the changed invariant, plus required repository checks;
- inspect the diff and confirm no unrelated changes entered;
- for every corrected inline review comment, post a reply in its original review thread;
- for every corrected non-threaded Pull Request comment, post one new general Pull Request comment that links to the original comment;
- make each reply concise and state the solution, affected artifact when useful, validation command or evidence, and result;
- report partial, failed, or inconclusive corrections honestly instead of claiming that they are complete; and
- preserve unresolved or disputed comments for explicit follow-up.

Do not mark a thread resolved without evidence that its exact concern is addressed. Before reporting, re-read every posted reply and confirm that it is attached to the intended thread or references the intended general comment.
