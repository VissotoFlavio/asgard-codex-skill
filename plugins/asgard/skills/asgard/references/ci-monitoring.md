# CI Monitoring

Use this policy only while Hermod observes pull-request checks, workflow runs, release automation, deployment Actions, or a CI-created backport. Monitoring is part of Hermod's release activity, not a new permanent Asgard role.

## Isolate the watcher

Start one fresh Hermod activity with no inherited conversation history when the platform supports it, such as `fork_turns="none"`. Its complete input is limited to:

- repository and provider identity;
- pull request, workflow, or run identifier;
- expected head or release revision;
- required checks and success conditions;
- a bounded deadline;
- the exact retry authority and maximum retry count, normally zero or one;
- sanitized commands or provider queries needed to observe the state.

Do not attach the implementation transcript, user conversation, full diff, reviewer reports, build logs, or prior polling output. Provide a narrow artifact or log excerpt only after a terminal failure makes it relevant.

## Wait without model polling

Prefer one provider-native blocking watch operation that exits on success or failure, such as `gh run watch --exit-status`, when it can bind to the required run and revision. Otherwise use the environment's event or wait mechanism with the longest safe bounded wait. Intermediate tool waits may resume the same operation but must not trigger analysis, narration, new agents, or repeated state queries while nothing actionable changed.

Silence is the required result for an unchanged pending state. Report only:

- all required checks succeeded for the expected revision;
- a required check failed, was cancelled, or timed out;
- the observed revision changed;
- the deadline expired;
- credentials, permissions, or provider state require user action.

Never create parallel watchers for the same revision. Never involve Tyr, Loki, Bragi, Heimdall, Forseti, or an implementer merely because CI is pending.

## Handle terminal events

Bind every result to the observed revision. On success, return the required check names, conclusion, revision, and provider URL. On failure, return only the failed job or step, a short sanitized excerpt, classification, revision, URL, and recommended owner.

Route a confirmed application, test, or build failure to the original Brokkr or Sindri. Use Mimir only when evidence cannot classify the cause. Use Ymir for a confirmed infrastructure failure. Odin decides which validations and approvals the correction invalidates; unaffected reviewers remain approved. A new revision receives one new isolated watcher and never reuses stale success.

Do not rerun automatically unless the original authority includes a retry count and the failure matches its stated transient conditions. Exhausting that count is terminal.

## Record efficient usage

When the platform exposes usage, record the watcher delta rather than its inherited or session-lifetime total:

```yaml
usage_observed:
  model_turns: integer | unavailable
  incremental_input_tokens: integer | unavailable
  incremental_cached_input_tokens: integer | unavailable
  incremental_output_tokens: integer | unavailable
```

Token telemetry is diagnostic evidence, not an acceptance or release gate. Never keep polling solely to obtain it.
