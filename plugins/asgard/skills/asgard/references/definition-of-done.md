# Definition of Done

Complete every field before dispatching implementation. Use `not applicable` where a capability or publication mechanism is absent.

```text
Activity:
Objective:
Execution directory:
Isolation mechanism: worktree | sandbox | checkout | other | none
Version-control system: value | not applicable
Base revision: value | not applicable
Working branch or change: value | not applicable
Publication target: PR | MR | change request | other | not applicable
Implementer: Brokkr | Sindri
Dependencies:
```

## Expected outcome

Describe observable behavior and the primary failure mode.

## Included and excluded scope

List required behavior, owned production and test artifacts, allowed integration points, forbidden shared artifacts, adjacent features, refactors, migrations, deployments, infrastructure, and destructive actions.

## Invariants

Record compatibility, public contract, stored-data, configuration, domain-rule, authorization, ownership, isolation, confidentiality, logging, fail-closed, abuse-resistance, transaction, and concurrency invariants as applicable.

## Required validation

Name focused suites, scenarios, expected results, negative cases, regression cases, concurrency checks, and security evidence proportional to risk.

## Specialist routing

```text
Mimir required: yes/no and uncertainty
Tyr required: yes/no and invariant
Loki required: yes
Heimdall required: yes
Independent review available: yes/no and limitation
```

## Rejection conditions

Reject missing behavior or validation, out-of-scope changes, broken invariants, unresolved findings, hidden deviations, sensitive leakage, false claims of independent review, or unauthorized operations.

## Completion record

```text
Candidate revision or diff:
DoD satisfied:
Odin review:
Tyr review: approved | not applicable
Loki review:
Heimdall review:
Affected validation passed:
Documentation synchronized:
Out-of-scope changes: none | details
Residual risks:
Odin final approval:
Delivery complete:
Publication authorized: yes | no | not applicable
```
