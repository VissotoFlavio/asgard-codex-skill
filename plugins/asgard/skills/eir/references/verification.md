# Eir verification guidance

Use this reference for `VERIFY` after a correction.

## Verification boundary

Compare the current candidate with the revision that received Eir's review. Use the authoritative issue, Eir's original findings, the correction diff, and current checks as the evidence set. Validate the same candidate across all conclusions; do not rely on a stale diff or an earlier test result when the relevant invariant changed.

For every Eir finding:

1. Identify the exact correction.
2. Re-check the original acceptance criterion or failure scenario.
3. Confirm the correction is sufficient rather than cosmetic.
4. Check nearby behavior for regressions and unintended contract changes.
5. Confirm focused tests or other evidence cover the correction.
6. Classify the result as corrected, partially corrected, not corrected, inadequate correction, obsolete, or inconclusive.

## Publish the outcome

If a finding is partially corrected, not corrected, inadequate, or inconclusive, publish one new evidence-backed `COMMENT` review or current-diff inline comment for the remaining concern. Keep the original Eir thread open and do not approve.

When every Eir finding is corrected or obsolete, resolve only an Eir-created thread after verifying that its exact concern is addressed. Confirm the thread author and original finding before resolution; never resolve threads created by a person or another skill. This mutation and the final approval require explicit authority for the exact Pull Request and candidate revision.

Submit one native `APPROVE` review with a concise summary of the issue criteria checked, correction revision, validation evidence, resolved Eir threads, and remaining non-blocking risks. Re-read the approval review and resolved-thread state before reporting `EIR_APPROVED`.

If approval or thread-resolution authority is absent, report `EIR_READY_FOR_APPROVAL` with the same evidence and leave all thread state unchanged.
