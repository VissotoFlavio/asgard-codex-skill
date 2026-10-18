# Eir review guidance

Use this reference for `REVIEW`.

## Evidence to collect

Read the authoritative issue, current Pull Request metadata and diff, prior reviews, review threads, inline comments, general comments, requested changes, and relevant CI checks through `gh`. Bind the review to the current head revision and locate each existing comment or new finding in the current code before deciding whether it remains applicable.

For every Eir finding, record the affected issue acceptance criterion, candidate evidence, impact, exact correction needed, and focused validation. Classify pre-existing comments only to avoid duplication; do not take ownership of findings from people or other skills.

## Publish the review

Before publishing, confirm the exact Pull Request and head revision, deduplicate against Eir's open feedback, and complete the analysis. Do not publish in a preview or dry-run request.

Create exactly one native Pull Request review with the `COMMENT` event. The review contains:

- an inline comment for each new actionable Eir finding with an exact current diff location;
- a Markdown summary with the reviewed issue criteria, candidate revision, findings without a stable inline location, and the recommendation; and
- severity, impact, concrete evidence, required correction, and validation for each actionable finding.

Use `gh api` only when inline comments require it. Do not create synthetic file or line locations, duplicate existing Eir findings, approve, request changes, edit comments, reply to a thread, or resolve a thread during `REVIEW`. If there are no actionable findings, publish the single `COMMENT` review summary with the reviewed scope and clean conclusion.

Re-read the published review and each inline comment. Confirm the Pull Request number, revision, Markdown body, and file or line target before reporting completion.
