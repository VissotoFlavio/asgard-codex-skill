---
name: eir
description: Deliver a defined GitHub issue through Pull Request review, authorized corrections, published reviewer feedback and solution replies, and final verification. Use for an issue-to-PR lifecycle or one of its explicit phases; not for release PR preparation.
metadata:
  short-description: Run the issue-to-PR review lifecycle
---

# Eir

Run a bounded GitHub delivery lifecycle from an authoritative issue through Pull Request creation, published review feedback, correction, and verification. Use Eir when the user wants the complete issue-to-PR loop or one of its explicit phases.

Eir complements Asgard; it does not replace Asgard's intent classification, proportional orchestration, specialist routing, or final acceptance. When Asgard is requested, preserve its execution graph and review gates. Do not invoke Asgard recursively from specialist tasks.

## Route the request

Select the narrowest applicable mode:

- **DELIVER**: read an issue, implement its approved scope, validate the candidate, and open a Pull Request when requested by the user.
- **REVIEW**: inspect a specified Pull Request and publish the evidence-backed review feedback on that Pull Request without changing the candidate.
- **CORRECT**: implement explicitly authorized, valid review corrections, then reply to every corrected review comment with the solution and its validation evidence.
- **VERIFY**: validate that corrections address the review findings and do not introduce regressions, without changing the candidate or Pull Request.

Do not infer that one mode authorizes the next. Opening a Pull Request is authorized only when requested as part of the delivery activity. A request to run **REVIEW** on a specified Pull Request authorizes Eir to submit that review's comments unless the user asks for a preview or dry run. Merge, deploy, release publication, migrations, data changes, infrastructure changes, dependency installation, and destructive actions require separate explicit authority.

## Common controls

Read repository instructions before acting. For GitHub, use only `gh` and run `gh auth status` before GitHub operations. If authentication, authorization, scopes, or a command fails, report the sanitized failure and stop; do not silently switch to a browser or another client.

Use the repository's issue, branch, changelog, Pull Request, and release policy. When the repository instructions require it:

- confirm that an authoritative issue exists before creating a delivery branch;
- confirm the branch base before creating any branch;
- never commit directly to protected branches;
- use the required branch naming convention and keep it within the repository limit;
- inspect the final diff before opening or updating a Pull Request;
- use Conventional Commits for local commits;
- include `Closes #<issue-number>` in eligible Pull Request descriptions;
- update an existing changelog when opening a Pull Request if the project has one;
- send GitHub Markdown with real line breaks, never literal `\\n` text.

Use native Pull Request reviews and review-thread replies through `gh` or `gh api`; use `gh api` when inline review comments or replies require it. Re-read each published review or reply and verify its Pull Request, target, body, and location when applicable. Never edit, delete, or resolve someone else's comment or review thread merely because a code change exists.

## Delivery completion

For **DELIVER**, read the issue and applicable repository instructions, define a proportional Definition of Done, implement only the issue scope, validate the final candidate, inspect the diff, and open the Pull Request if authorized. The Pull Request must identify the issue, summarize the change, list validations, disclose relevant risks, and contain the required closing reference.

Read [delivery.md](references/delivery.md) for the detailed delivery contract.

## Review feedback and correction

For **REVIEW**, read the issue, current Pull Request, previous reviews, general comments, inline comments, requested changes, current diff, and relevant checks. Classify existing feedback and identify new findings. Publish one native Pull Request review with a `COMMENT` event after the analysis: use inline comments only for findings that map to an exact line in the current diff, and use the review summary for findings without a stable inline location. Do not change the candidate, edit existing comments, resolve threads, approve, or request changes.

For **CORRECT**, require explicit authority to change the candidate. Group compatible accepted findings into one bounded correction pass, preserve the issue scope, run only affected validations, and inspect the diff. After sufficient validation, reply to every corrected finding on the Pull Request with the implemented solution and validation evidence. Reply in the original inline review thread when it exists; for a non-threaded Pull Request comment, publish a new general Pull Request comment that links to the original comment. Do not claim a correction is complete when its validation failed or is inconclusive, and do not mark a thread resolved without evidence that its exact concern is addressed.

Read [review.md](references/review.md) for review publication, classification, and correction-response rules.

## Final verification

For **VERIFY**, compare the current candidate with the prior reviewed state and map every correction to its original finding. Confirm behavior, tests, contracts, security properties, compatibility, and absence of regressions proportional to risk. Re-run only validations affected by the correction or required by repository policy.

Read [verification.md](references/verification.md) for the verification contract.

## Reporting

Keep reports evidence-based and delta-focused. Include the selected mode, authority ceiling, issue and Pull Request identifiers, changed artifacts, published review or response URLs, validations and results, unresolved risks, blockers, and the final recommendation. For findings, include severity, file and line when available, impact, evidence, and recommended action.
