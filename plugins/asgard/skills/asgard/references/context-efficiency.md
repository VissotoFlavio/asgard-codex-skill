# Context Efficiency

Use this policy when a delivery crosses multiple activities, agents, correction cycles, or major phases. Its budgets control orchestration cost; they never weaken acceptance criteria, conceal errors, or authorize excluded operations.

## Budget before dispatch

Add this task-local block to the execution graph:

```yaml
execution_budget:
  simultaneous_agents: 3
  correction_cycles: 1
  report_words:
    monitor_or_status: 50
    implementer: 150
    reviewer_with_findings: 250
    odin_final: 300
  inherited_history: none
  rationale_for_exceptions: none
```

These defaults are decision limits rather than platform-enforced token caps. A reviewer with no findings returns one decision line: `APPROVED — <primary evidence>`. Select fewer agents when the required work permits it. Increase only the constrained field justified by a concrete risk, unavailable evidence source, or indivisible dependency, and record that reason before dispatch. Do not increase a budget merely because capacity is available or an agent timed out.

After the allowed grouped correction cycle, unresolved material findings return to Odin for graph reassessment. Do not create an open-ended chain of replacement implementers, investigators, and reviewers.

## Dispatch without orchestration recursion

Odin applies Asgard once. Delegated skill prompts must not mention or invoke `$asgard:asgard`; doing so can reload the orchestration entrypoint and conditional references inside every child context. Dispatch only the chosen bounded skill with its task-local activity contract, applicable repository rules, bounded paths or revision, validation, and exclusions.

Use no inherited conversation history when the platform supports it. If a specialist needs prior evidence, include the compact checkpoint or an exact artifact reference. Never solve missing context by attaching the entire parent transcript.

## Checkpoint phase transitions

Create one compact checkpoint when moving between material phases such as discussion to implementation or implementation to integrated review:

```yaml
phase_checkpoint:
  phase_completed: value
  candidate_revision: sha | diff reference | not created
  decisions: concise list
  changed_artifacts: bounded paths
  validation: command and conclusion or artifact reference
  approvals: skill and decision
  deviations: material delta only
  open_risks: actionable items only
  next_activity: objective and owner
  authority_remaining: explicitly authorized operations
```

Omit empty fields. The checkpoint replaces completed narrative for subsequent dispatch; do not append transcripts, full logs, full diffs, or repeated leaf-skill reports. Retain an exact path, revision, run URL, or command so evidence remains verifiable.

## Bound inputs and reports

Provide a bounded diff command or changed-path list instead of embedding a full repository diff. Successful validations need the command, conclusion, and optional artifact or run URL. Include only the smallest sanitized failure excerpt that lets the owner reproduce or classify an error.

Leaf-skill reports use the budget above and return the applicable terminal status without suppressing its required evidence. Omit only fields that do not apply to that status:

```yaml
decision: IMPLEMENTER_COMPLETE | FINDINGS_COMPLETE | APPROVED | CHANGES_REQUIRED | PENDING | HANDOFF_REQUIRED | BLOCKED
changed: bounded paths | none
validation: command and conclusion | not run
findings: actionable findings only
risks: material residual risks only
handoff: # required when decision is HANDOFF_REQUIRED
  recommended_skill: $skill
  reason: bounded explanation
  evidence: paths, observed state, or candidate facts
  prerequisites: required information, stable state, or artifacts
  authority_required: exact protected authority | none
```

`APPROVED` with no findings is one decision line. `HANDOFF_REQUIRED` always includes every `handoff` field above. Do not repeat the prompt, leaf-skill guidance, DoD, unchanged state, successful tool output, or a narrative summary after each command. Emit a report only at activity completion, a material phase checkpoint, or a terminal or actionable monitoring event. Stop investigating when the activity contract has sufficient evidence; do not explore unrelated alternatives or improvements.

## Odin post-processing summary

After preserving the leaf terminal report, Odin may prepare a compact orchestration summary containing the decision, changed artifacts, validation, actionable findings, residual risks, next owner, and remaining authority. This summary never replaces, normalizes away, or omits a leaf terminal status or its required handoff fields.

## Scale reasoning to risk

When the platform supports per-agent reasoning effort, use the lowest level that preserves the activity's acceptance criteria:

- `minimal` for passive monitoring or status observation;
- `low` for deterministic Git, GitHub, release, formatting, or traceability operations;
- `medium` for ordinary implementation, discovery, and behavioral review;
- `high` only for a recorded security, concurrency, architecture, persistence, irreversible, or cross-boundary risk.

Do not use `high` by default for every specialist. Increase effort only for the agent and activity owning the concrete risk. Prefer deterministic commands or scripts for state comparison, filtering, and schema checks; invoke model reasoning only when evidence changed or a decision is required.

## Measure deltas

When usage is exposed, record increments for the work performed after dispatch rather than session-lifetime or inherited totals:

```yaml
usage_observed:
  intent: value
  phase: value
  leaf_skill: value
  model_turns: integer | unavailable
  incremental_input_tokens: integer | unavailable
  incremental_cached_input_tokens: integer | unavailable
  incremental_output_tokens: integer | unavailable
  incremental_reasoning_output_tokens: integer | unavailable
```

Aggregate by phase and selected skill only at the final checkpoint. Telemetry is diagnostic: do not spend additional model turns polling, reconstructing, or explaining unavailable usage.
