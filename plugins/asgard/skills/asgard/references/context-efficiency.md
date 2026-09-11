# Context Efficiency

Use this policy when a delivery crosses multiple activities, agents, correction cycles, or major phases. Its budgets control orchestration cost; they never weaken acceptance criteria, conceal errors, or authorize excluded operations.

## Budget before dispatch

Add this task-local block to the execution graph:

```yaml
execution_budget:
  simultaneous_agents: 3
  correction_cycles: 1
  report_words_per_agent: 400
  inherited_history: none
  rationale_for_exceptions: none
```

These defaults are decision limits rather than platform-enforced token caps. Select fewer agents when the required work permits it. Increase only the constrained field justified by a concrete risk, unavailable evidence source, or indivisible dependency, and record that reason before dispatch. Do not increase a budget merely because capacity is available or an agent timed out.

After the allowed grouped correction cycle, unresolved material findings return to Odin for graph reassessment. Do not create an open-ended chain of replacement implementers, investigators, and reviewers.

## Dispatch without orchestration recursion

Odin applies Asgard once. Specialist prompts must not mention or invoke `$asgard`; doing so can reload the orchestration entrypoint and conditional references inside every child context. Send only the chosen role packet, task-local activity contract, applicable repository rules, bounded paths or revision, validation, and exclusions.

Use no inherited conversation history when the platform supports it. If a specialist needs prior evidence, include the compact checkpoint or an exact artifact reference. Never solve missing context by attaching the entire parent transcript.

## Checkpoint phase transitions

Create one compact checkpoint when moving between material phases such as discussion to implementation, implementation to integrated review, or approval to release:

```yaml
phase_checkpoint:
  phase_completed: value
  candidate_revision: sha | diff reference | not created
  decisions: concise list
  changed_artifacts: bounded paths
  validation: command and conclusion or artifact reference
  approvals: role and decision
  deviations: material delta only
  open_risks: actionable items only
  next_activity: objective and owner
  authority_remaining: explicitly authorized operations
```

Omit empty fields. The checkpoint replaces completed narrative for subsequent dispatch; do not append transcripts, full logs, full diffs, or repeated role reports. Retain an exact path, revision, run URL, or command so evidence remains verifiable.

## Bound inputs and reports

Provide a bounded diff command or changed-path list instead of embedding a full repository diff. Successful validations need the command, conclusion, and optional artifact or run URL. Include only the smallest sanitized failure excerpt that lets the owner reproduce or classify an error.

Agent reports default to 400 words and contain only decisions, changed artifacts, material findings, validation conclusions, deviations, risks, and blockers. `APPROVED` with no findings is one decision line. Do not repeat the prompt, role packet, DoD, unchanged state, or successful tool output.

## Measure deltas

When usage is exposed, record increments for the work performed after dispatch rather than session-lifetime or inherited totals:

```yaml
usage_observed:
  phase: value
  role: value
  model_turns: integer | unavailable
  incremental_input_tokens: integer | unavailable
  incremental_cached_input_tokens: integer | unavailable
  incremental_output_tokens: integer | unavailable
```

Aggregate by phase and role only at the final checkpoint. Telemetry is diagnostic: do not spend additional model turns polling, reconstructing, or explaining unavailable usage.
