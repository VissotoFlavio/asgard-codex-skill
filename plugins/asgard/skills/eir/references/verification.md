# Final verification contract

Use this reference for `VERIFY` after a correction pass.

## Verification boundary

Compare the current candidate with the state that received the published review. Use the original issue, the original review comments, the correction diff, and current checks as the evidence set. Validate the same candidate across all conclusions; do not rely on a stale diff or an earlier test result when the relevant invariant changed.

## Per-finding verification

For every accepted review finding:

1. Identify the exact correction.
2. Re-check the original failure scenario or invariant.
3. Confirm the correction is sufficient rather than merely cosmetic.
4. Check nearby behavior for regressions and unintended contract changes.
5. Confirm focused tests or other evidence cover the correction.
6. Classify the result as corrected, partially corrected, not corrected, inadequate correction, obsolete, or inconclusive.

## Final checks

Also verify, proportional to risk:

- issue acceptance criteria;
- affected APIs, contracts, persistence, and compatibility;
- security, authorization, privacy, and availability properties;
- relevant build, test, lint, static analysis, and CI results;
- absence of unrelated changes;
- remaining unresolved comments and risks.

The final report must state a recommendation: approve, request further corrections, or inconclusive. This mode is read-only: do not modify code, comments, issues, Pull Requests, or thread state.
