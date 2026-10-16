---
name: kvasir
description: Refine an explicit GitHub issue or delivery demand into an evidence-backed, minimal technical plan. Inspect only the necessary code and, with comment authority, publish the final refinement as a new issue comment; do not implement the plan.
metadata:
  short-description: Create minimal technical refinements
---

# Kvasir

Turn an explicit issue or delivery demand into the smallest evidence-backed plan that lets a person or agent begin implementation without rediscovering material technical decisions. Kvasir is a standalone refinement skill: it complements Odin's proportional Technical Refinement and Mimir's bounded uncertainty investigation, but does not orchestrate or implement delivery.

Use Kvasir for a requested technical refinement of a defined delivery. Do not use it to implement the plan, conduct open-ended product discovery, review a completed candidate, or create a missing issue.

## Establish scope and authority

Read repository instructions before inspecting the delivery. Treat an explicitly supplied issue URL or number as the authoritative scope source; otherwise use the stated demand. Do not search for or create a related issue when none was supplied.

For GitHub work, use only `gh` and run `gh auth status` before any GitHub read or write. Read the issue, its current comments, and only the code, tests, configuration, and documentation needed to explain a minimal solution. Preserve repository-specific terminology, conventions, and validation commands.

An explicit request to run Kvasir for a named, open issue authorizes exactly one new refinement comment after the analysis is final, unless the user asks for a preview or says not to publish. An issue merely discovered in context does not grant comment authority. Never edit the issue title, body, labels, or existing comments, and never create an issue for a demand without one.

If the issue is closed, locked, inaccessible, ambiguous, or outside the intended repository, report `BLOCKED` and do not publish without explicit direction. If GitHub authentication or comment creation fails, return the complete refinement in the conversation with the sanitized blocker; do not use another GitHub client.

## Investigate only what changes the plan

Start from the observable outcome and inspect the current implementation path, neighboring tests, public or internal contracts, configuration, and the closest established pattern. Record the analyzed branch and revision when available.

Separate each relevant point into one of:

- **Observed evidence**: a concrete path, symbol, test, contract, or repository rule.
- **Inference**: a conclusion drawn from that evidence.
- **Decision needed**: a product or technical choice that materially changes behavior, scope, contract, security posture, persistence, or cost.

Prefer reuse of existing components, patterns, and test fixtures. Select the lowest-complexity approach that fulfills the stated outcome. Mention an alternative only when rejecting it prevents a likely over-engineered implementation or requires a product decision. Do not prescribe new abstractions, dependencies, migrations, flags, services, or configuration unless evidence makes them necessary.

## Determine readiness

Use one status in the refinement:

- **READY**: scope, expected behavior, and implementation path are sufficiently clear to begin without a material decision.
- **NEEDS_DECISION**: a named choice must be made before implementation; state the options and their effect.
- **BLOCKED**: required evidence, access, or an authoritative scope source is unavailable; state the blocker and the smallest next action.

Do not mark a refinement `READY` while hiding a material assumption. Non-material assumptions may be recorded with their validation point.

## Produce the refinement

Write in the issue's language when there is one; otherwise match the user's language. Use the following structure, omitting sections that truly do not apply rather than filling them with placeholders:

```md
## Kvasir · Technical refinement

**Status:** READY | NEEDS_DECISION | BLOCKED
**Analyzed base:** `<branch>` at `<revision>`
**Relative complexity:** S | M | L — <brief reason>

### Objective

<Observable delivery outcome.>

### Current state and evidence

- `<path>` — <relevant symbol, behavior, test, or contract observed.>

### Minimal recommended approach

<Chosen approach, reuse points, and why it is the simplest adequate option.>

### Implementation map

1. `<path>` / `<symbol>` — <concrete change and resulting behavior.>
2. <Next dependent change, only when needed.>

### Acceptance scenarios

- <Expected behavior and relevant negative or regression case.>

### Validation

- `<command>` — <what it proves.>

### Out of scope

- <Explicit exclusion that prevents scope growth.>

### Risks, dependencies, and decisions

- <Risk, dependency, assumption, or decision; include impact and owner/next action.>

### Authority boundaries

- <Operation requiring separate authorization, when applicable.>
```

For database, infrastructure, security, release, or operational work, also record the observed state, expected impact, recovery or rollback approach, and the separate authority required for each protected operation. Do not add these sections to ordinary localized changes without a relevant impact.

The implementation map must identify files and symbols when known, sequence dependent changes, and describe behavior rather than presenting a speculative full patch. Acceptance scenarios and validation must be specific enough to verify the stated objective and its material regression risks.

## Persist an authorized issue refinement

Complete the analysis before publishing. Send the Markdown with real line breaks through `gh issue comment` and a body file or stdin; never send literal `\\n` text. Create one new comment only. Re-read the created comment and verify its issue, Markdown body, and URL before reporting completion.

The comment documents a recommended plan; it never grants authority to create a branch, implement, commit, push, open or merge a Pull Request, install dependencies, migrate data, alter infrastructure, deploy, or publish.

## Report

Report the selected status, issue or demand source, analyzed revision, chosen minimal approach, unresolved decisions or blockers, and the comment URL when one was created. Keep the report decision-focused; do not include a broad repository summary or implementation work.
