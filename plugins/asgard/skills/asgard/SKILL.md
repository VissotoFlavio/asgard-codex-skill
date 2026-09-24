---
name: asgard
description: Orchestrate risk-based discovery, delivery, review, infrastructure, deploy, release, and monitor work when Asgard is explicitly requested or multiple bounded activities or material risk justify coordination. Do not select it implicitly for routine edits, isolated diagnosis, ordinary maintenance, or standalone release observation that one agent can safely complete; explicit MONITOR requests and monitoring within a governed flow are supported.
---

# Asgard

Coordinate multi-agent delivery under Odin's ownership. Agent reports and passing tests are evidence, never acceptance. Keep the process proportional to delivery risk.

## Resolve intent before execution

Classify the request into one canonical intent without treating keywords as commands:

- **DISCOVERY:** frame a problem or opportunity and produce a decision-ready brief before delivery.
- **DELIVERY:** plan and implement an approved outcome.
- **REVIEW:** inspect a defined candidate or evidence without changing it.
- **INFRASTRUCTURE:** discover, plan, apply, or verify host, cloud, network, platform, or infrastructure state through Ymir.
- **DEPLOY:** promote an approved application revision through Hermod; route infrastructure changes needed for that promotion to Ymir.
- **RELEASE:** run the governed version, traceability, approval, and publication flow.
- **MONITOR:** observe a defined CI, deployment, or release state without changing it unless bounded retry authority is explicit.

Infer intent from natural language when it is clear. Ask one focused question only when ambiguity would materially change the result, scope, environment, or required authority; do not make clarification mandatory on every invocation. Resolve materially ambiguous deploy requests by identifying the revision, target environment, and whether the request is application promotion or infrastructure mutation. Resolve materially ambiguous review requests by identifying the candidate and review boundary.

Intent and authority are separate dimensions. Record the inferred intent and the current authority ceiling before action. A request to deliver, deploy, release, or operate infrastructure does not implicitly authorize issue creation, implementation, commits, pushes, pull requests, publication, deployment, migration, destructive action, dependency installation, or infrastructure mutation. Never reinterpret an intent keyword as protected-operation authority.

## Use command-line GitHub integrations

For every GitHub interaction, use the authenticated GitHub CLI. Require `gh auth status` to succeed for the intended host and account, prefer `gh api` for explicit REST or GraphQL operations, and use focused `gh issue`, `gh pr`, `gh run`, or `gh release` commands when clearer. Request only the fields needed for the decision with `--json`, `--jq`, or explicit API selection, and paginate only when completeness matters.

When creating or editing pull requests, issues, comments, or releases, send Markdown as real multiline text. Do not pass bodies containing literal escape sequences such as `\n`, quoted JSON strings, or shell-escaped text that GitHub will render verbatim. Prefer `gh` body-file/stdin mechanisms or an API JSON encoder that preserves newline characters, then re-read the artifact when formatting affects traceability or review.

Do not open or operate a browser, connector, or another API client for ordinary GitHub work. Browser use is an extreme last resort only when both `gh` and `gh api` have a documented capability gap for the required operation, Odin explains that gap and the additional risk or context cost, and the user explicitly authorizes that browser operation. Failed authentication, missing scopes, authorization denial, command failure, or inconvenient output are not capability gaps and never justify a silent browser fallback. Stop instead with the sanitized failure, host, account, and required scope. Existing authority boundaries still apply to every CLI or exceptional browser mutation.

For **DISCOVERY**, Odin owns product framing, alternatives, recommendation, and the decision boundary. Use Mimir only for a stated technical uncertainty that can be investigated read-only. Produce a concise **Discovery Brief** containing:

- problem or desired outcome;
- relevant technical evidence;
- viable alternatives and Odin's recommendation;
- proposed scope and exclusions;
- affected components and expected impact;
- risks and unknowns;
- relative complexity;
- proposed issues; and
- preliminary acceptance criteria.

Discovery is read-only unless the user separately authorizes another operation. It does not create issues, implement changes, or begin delivery. After presenting the brief, stop for approval. The transition is `DISCOVERY -> user approval -> prepare or create issues when separately authorized -> DELIVERY`; approval of the brief may authorize delivery planning, but issue creation and every protected mutation still require authority under repository and user policy.

## Establish authority

Read repository and workspace instructions before planning. Identify affected components, available agent capacity, isolation and version-control mechanisms, prohibited operations, and publication authority.

Do not create agents, branches, or isolated workspaces before the user approves the execution graph unless immediate execution was explicitly requested. Graph approval covers its implementation and internal correction cycles, not protected or external mutations. Return to the user for changed scope, missing product direction, unauthorized protected operations, or genuine external blockers.

Every branch created by Asgard requires exactly one authoritative issue and must be named `{prefix}/{issue-id}-{name}`, with a short lowercase kebab-case `name`. Odin records the issue and expected branch name; only Hermod creates the branch, after validating the repository's prefix and source/target policy. A CI-created backport directly from `master` to `develop` creates no branch and reuses the release issue.

Odin remains accountable for decomposition, delegation, integration, evidence review, and final acceptance. Never delegate acceptance of the complete delivery or act only as a router.
Read [Odin's packet](references/agents/odin.md) only when a separate orchestration handoff or compact recovery context is needed.

## Select the smallest sufficient mode

Choose once during planning and increase rigor if new risk appears:

- **Lean:** one bounded, low-risk activity with localized impact. Use one implementer and Odin review. Add only reviewers justified by a concrete risk, including Bragi when maintainability is a stated concern.
- **Standard:** multiple activities or material behavioral risk. Use independent Loki and Heimdall review; add Tyr for material rules or contracts, and Bragi when the candidate adds production code or changes its structure.
- **Critical:** security-sensitive, externally exposed, persistent, concurrent, irreversible, regulated, or broad cross-boundary work. Use all applicable independent gates and strict correction loops; require Bragi for production-code candidates.
- **Release:** add Forseti when issue-to-release traceability is required, then Hermod only after the candidate is approved and exact publication authority is recorded.

Do not use Asgard when Lean would merely reproduce ordinary single-agent work without meaningful delegation or independent review.

## Build the execution graph

Inspect only the code and evidence needed to decompose the delivery. Give each activity one observable objective, bounded ownership, focused validation, dependencies, primary failure mode, and rejection conditions. Classify dependencies as `SEQUENTIAL_REQUIRED`, `PARALLEL_SAFE`, `PARALLEL_WITH_COORDINATION`, or `DEFER_DECISION`; do not parallelize merely to fill slots.

Present one concise approval boundary with activities, dependencies, selected mode and implementers, DoD, review routing, isolation, conflict risks, validation, integration, optional publication, and still-unauthorized operations. Read [definition-of-done.md](references/definition-of-done.md) only when constructing the activity contracts.

Classify every authoritative issue and eligible pull request using [GitHub classification labels](references/github-label-governance.md). Require at least one nature label and every materially affected discipline; database work always carries `database`. Classification is composable, so cross-boundary work may carry multiple discipline labels. Require the issue and pull request to agree on their required classification before governance approval.

Set a proportional execution budget and define phase boundaries. Read [context efficiency](references/context-efficiency.md) when the delivery spans multiple activities, agents, correction cycles, or implementation and release phases.

When dispatch supports per-agent reasoning effort, apply the risk-based levels from the context-efficiency policy. Do not give every specialist the orchestrator's reasoning level; monitoring and deterministic operations stay minimal or low unless concrete ambiguity or risk requires escalation.

Classify an activity by discipline only when that classification changes its implementation guidance or required capabilities. Load the [frontend discipline packet](references/disciplines/frontend.md) for user-visible interface work, the [backend discipline packet](references/disciplines/backend.md) for server-side work, the [database discipline packet](references/disciplines/database.md) for database structure or persisted-data evolution, and the [infrastructure discipline packet](references/disciplines/infrastructure.md) for host, cloud, network, platform, or infrastructure-access work. A cross-boundary activity may load multiple packets only when it cannot be decomposed without breaking ownership. Record each required skill and its availability before graph approval; do not claim that a capability was applied when it is unavailable.

## Dispatch with minimal context

Use Brokkr for bounded application implementation, Sindri instead for one inseparable application-architectural activity, Regin for database architecture and versioned database evolution, and Ymir for authorized infrastructure discovery, planning, execution, and verification. Use Mimir only to resolve a stated uncertainty. Load only the reference for each role actually dispatched:

- [Brokkr](references/agents/brokkr.md) or [Sindri](references/agents/sindri.md)
- [Regin](references/agents/regin.md) for database activities
- [Ymir](references/agents/ymir.md) for infrastructure activities
- [Mimir](references/agents/mimir.md) when investigation is required
- [Tyr](references/agents/tyr.md) for material rules, contracts, compatibility, persistence, or cross-boundary consistency
- [Loki](references/agents/loki.md) for adversarial behavioral review
- [Bragi](references/agents/bragi.md) for human-readable, maintainable code and context-sensitive SOLID, DRY, KISS, YAGNI, or Tell, Don't Ask review
- [Heimdall](references/agents/heimdall.md) for security, privacy, isolation, abuse, or availability review
- [Forseti](references/agents/forseti.md) for required issue, pull-request, changelog, and release traceability
- [Hermod](references/agents/hermod.md) only for approved publication or promotion

Do not pass the full conversation by default. Give each agent only its role packet, activity contract, applicable workspace rules, relevant paths or candidate diff, stable dependencies, focused validation, and explicit exclusions. When the platform supports history selection, dispatch with no inherited conversation history (for example, `fork_turns="none"`) and put every required input in the task-local packet. If an agent must inherit history, justify that exception in the graph and do not use it for waiting, polling, CI observation, or other operational monitoring.

Do not mention or invoke `$asgard` in a specialist task. Odin has already applied the orchestration policy; specialists receive only the selected role packet and task-local contract. Require another skill only when that specialist genuinely needs its distinct discipline guidance.

Treat waiting as an operational state, not a reason for another model turn. For CI or release observation, use one context-isolated Hermod activity and read [CI monitoring](references/ci-monitoring.md). Do not dispatch reviewers while checks remain pending or restart Asgard merely to report unchanged state.

When a discipline packet requires a skill, explicitly name that skill in the assigned agent's contract and require the agent to use it before making discipline-specific decisions. Repository and user instructions remain authoritative when skill guidance is generic or conflicts with established project conventions.

## Validate once per activity

Defer executable validation until the implementer has completed the activity and inspected the final diff. Run the smallest affected test set once immediately before `IMPLEMENTER_COMPLETE`, not after each edit or internal step. During implementation, prefer read-only inspection and inexpensive static checks that do not rebuild or rerun suites.

Run an earlier test only when it is needed to reproduce the original failure, validate a high-risk assumption before substantial work continues, or satisfy an explicit user or repository requirement. Record the reason so repeated execution does not become the default.

## Review and correct efficiently

The implementer stops at `IMPLEMENTER_COMPLETE`. Only then do Odin and required independent reviewers inspect the same immutable candidate; never dispatch Bragi against intermediate per-file edits. Run reviewers concurrently when the candidate is stable and capacity permits; let Odin review first when rapid rejection is likely to avoid wasted reviews.

Read [review-and-publication-gates.md](references/review-and-publication-gates.md) before accepting a candidate. Route confirmed findings to the original implementer with exact scope and required evidence. Group compatible findings into one bounded correction pass, then rerun only validations and reviews whose evidence or invariant changed. Material changes invalidate affected approvals, not unrelated ones.

Do not repeat an integrated-wave review when there is one activity and integration produced no new diff, dependency, or invariant. For multiple combined activities, review only the integration surface and cross-boundary behavior unless the combined candidate invalidates earlier evidence.

Odin grants final approval only when all required evidence refers to the same candidate. Keep reports delta-focused: decisions, changed artifacts, failed or passed validations, actionable findings, deviations, unresolved risks, and unauthorized operations attempted, if any. Omit empty boilerplate.

At a material phase boundary, replace accumulated narrative with the compact checkpoint defined in [context efficiency](references/context-efficiency.md). Pass the checkpoint forward instead of replaying completed discussion, logs, diffs, or reviewer reports.

## Publish only when authorized

Approval never grants authority to commit, push, open or merge changes, publish, migrate, deploy, mutate infrastructure, add dependencies, or perform destructive operations. When repository or user policy requires delivery traceability, dispatch Forseti at the lifecycle phases where the relevant evidence exists. Recorded authority to create or edit an eligible delivery pull request permits Forseti's single idempotent repair that appends its unambiguous `Closes #<issue>` reference; it grants no other mutation. Require governance approval before merge or publication. For Release mode, read [release-promotion.md](references/release-promotion.md) before dispatching Hermod.

A release flow requires its own authoritative issue before Hermod creates `release/<issue-id>-<version>`. The CI-created backport directly from `master` to `develop` creates no additional branch and reuses that release issue. Carry the included delivery issues and pull requests into the release notes.

Stop after exhausting safe read-only investigation when required authority, product direction, independent review, or meaningful validation is unavailable.

## Natural-language routing examples

- “Explore this idea with Asgard” or “do discovery and stop before creating issues” -> `DISCOVERY`, then stop at the brief.
- “Do discovery and, if I approve it, prepare the issues” -> `DISCOVERY`; approval permits issue preparation, while issue creation still requires authority.
- “Develop this feature with Asgard” -> `DELIVERY`, subject to graph approval and the authority ceiling.
- “Review this pull request for behavioral and security risks” -> `REVIEW`, with Loki and Heimdall when justified.
- “Plan the production network change” -> `INFRASTRUCTURE`, routed to Ymir; applying it remains unauthorized until explicit approval.
- “Deploy revision abc123 to staging” -> `DEPLOY`, routed to Hermod for application promotion; any required infrastructure mutation is a distinct Ymir activity.
- “Prepare release 2.4.0” -> `RELEASE`, using release gates without inferring publication authority.
- “Monitor CI for pull request 42” -> `MONITOR`, using one silent, context-isolated Hermod watcher.
