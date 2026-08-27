# Definition of Done

Create a task-local contract before implementation. Include only fields that change execution or acceptance; use `not applicable` only when omitting a field would be ambiguous.

## Required core

```text
Activity:
Objective and observable outcome:
Owned production and test artifacts:
Dependencies and base state:
Discipline and rationale:
Required skills and availability:
Primary failure mode:
Applicable invariants:
Focused validation and end-of-activity command:
Rejection conditions:
Implementer: Brokkr | Sindri
Mode: Lean | Standard | Critical | Release
Required reviewers and rationale:
Excluded or unauthorized operations:
```

Add execution directory, isolation, branch or revision, shared files, conflict risk, publication target, or external authority only when applicable.

Omit discipline and required skills when they do not change execution. For a .NET backend activity, record `Backend` and `$dotnet-best-practices: AVAILABLE` before dispatch. For frontend work, record the applicable implementation and independent review skills from the frontend discipline packet. Treat an unavailable required skill or review source as a planning blocker unless the user approves a stated fallback.

## Scale detail to risk

- **Lean:** record the observable outcome, owned artifacts, focused validation, primary failure mode, and exclusions. Add a specialist reviewer only for an identified risk.
- **Standard:** also record material compatibility, domain, authorization, data, concurrency, and cross-boundary invariants; require Loki and Heimdall, and Tyr when contracts or rules are material.
- **Critical:** make every relevant security, privacy, persistence, transaction, isolation, abuse, availability, rollback, and negative-test expectation explicit.
- **Release:** additionally record the exact approved revision and authority for each repository or publication mutation.

Avoid generic invariant checklists. An invariant belongs in the contract only when the activity can affect it.

Schedule executable validation once at the end of implementation. If an earlier run is required to reproduce a defect or test a high-risk assumption, record that exception in the contract.

## Completion evidence

Record the exact candidate revision or diff, changed artifacts, DoD result, focused validation, required reviewer decisions, deviations, out-of-scope changes, and residual risks. A single `APPROVED` may cover a reviewer with no findings; do not repeat its full packet.

Odin accepts only evidence for the same candidate. Passing tests, implementer completion, or one reviewer approval is insufficient when other gates are required.
