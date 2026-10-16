<p align="center">
  <img src="./assets/asgard-agents.png" alt="Asgard agents, responsibilities, and delivery flow" width="760">
</p>

# Asgard for Codex

Asgard is a risk-based, multi-agent discovery and software delivery workflow for Codex. Odin frames decisions, decomposes substantial work into bounded activities, assigns focused specialists, reviews their evidence, coordinates independent gates, and remains accountable for final acceptance.

The workflow is intentionally proportional: routine changes should stay simple, while complex or high-risk deliveries receive stronger implementation, contract, adversarial, security, governance, and publication controls.

## When to use Asgard

Use Asgard when it is explicitly requested for discovery, delivery, review, infrastructure, deploy, or monitoring, or when work benefits from one or more of the following:

- decision-ready discovery before implementation;
- multiple bounded implementation activities;
- coordinated application and infrastructure work;
- explicit acceptance criteria and dependency ordering;
- independent behavioral, contract, or security review;
- high-assurance deployment promotion with traceable evidence;
- explicit monitoring or monitoring within a governed delivery or release flow.

Do not select it implicitly for routine single-file edits, isolated diagnosis, ordinary maintenance, or standalone release observation that one agent can handle safely. Explicit monitoring remains supported. Asgard should reduce delivery risk, not add ceremony without a concrete reason.

## Roles

| Role | Responsibility |
| --- | --- |
| **Odin** | Plans the execution graph, coordinates specialists, reviews evidence, and owns final acceptance. |
| **Brokkr** | Implements bounded application work within an established architecture. |
| **Sindri** | Implements one inseparable application activity that requires architectural ownership. |
| **Regin** | Owns database architecture and safe schema evolution, including tables, keys, constraints, indexes, relationships, migrations, and data backfills. |
| **Ymir** | Discovers, plans, applies authorized infrastructure changes, and verifies the resulting environment. |
| **Mimir** | Resolves a stated code, documentation, or technical uncertainty. |
| **Tyr** | Independently validates material rules, contracts, compatibility, and consistency. |
| **Loki** | Searches adversarially for behavioral gaps and edge cases. |
| **Bragi** | Reviews completed code for human readability and maintainability using context-sensitive SOLID, DRY, KISS, YAGNI, and Tell, Don't Ask. |
| **Heimdall** | Independently reviews security, privacy, isolation, abuse, availability, and risk-justified deep vulnerability analysis. |
| **Forseti** | Verifies repository-required delivery and release traceability, including a narrowly authorized metadata repair when policy permits it. |

Specialists receive task-local context rather than the entire conversation. Their reports and passing tests are evidence; Odin still owns product decisions, inspects the candidate, and makes the acceptance decision. Mimir only resolves stated technical uncertainty read-only. Regin may design and author versioned database changes, but connecting to or mutating any durable, runtime, or non-isolated database, applying or retrying a migration, and executing a rollback each require explicit authority for the exact environment and candidate.

On first use of each database profile, Regin requests separate read-only discovery authority and consent before persisting a local inventory. Later activities load a compact summary and only relevant object details, refreshing stale, incomplete, affected, or drifted sections instead of rediscovering the whole database. Profiles and inventories live outside the repository and installed plugin under `ASGARD_CONFIG_HOME/databases` when configured, otherwise the platform-local Asgard data directory. They contain no credentials or row data, never replace the runtime database as source of truth, and never authorize `APPLY`; live preflight remains mandatory.

For a database container on a VPS, keep its port private or bound only to VPS loopback and connect through a loopback-only SSH local forward. Ymir owns the verified VPS, tunnel, Docker/network exposure, and external credential mechanisms; Regin separately verifies the database and uses distinct least-privilege principals for application runtime, `DISCOVER`, isolated `VALIDATE`, migration `APPLY`, and emergency administration. Profiles retain only opaque credential references. Tunnel access never authorizes a database phase, and public exposure, identity drift, excess privilege, or tunnel loss fails closed.

Odin applies Asgard once: specialist tasks do not invoke `$asgard` again. Multi-phase deliveries use compact checkpoints, fresh agent contexts, bounded reports, and a proportional default budget of three simultaneous agents and one grouped correction cycle. Exact paths, revisions, run URLs, and validation conclusions replace copied transcripts, full diffs, and successful logs.

When a user requests vulnerability discovery or Heimdall identifies a need for deeper analysis, Asgard can route a bounded `Security` discipline review. Heimdall uses `$api-security-review` for API surfaces and `$web-security-review` for web application surfaces when those skills are installed. If a relevant skill is missing, Odin asks whether to install it; when installation is declined or unavailable, Heimdall continues with the native security review and records the fallback rather than claiming the specialized skill was applied.

Deep security review is not run for every ordinary delivery. Run it when requested, required by repository policy, or justified by material risk. Confirmed blocking vulnerabilities stop the affected promotion step so corrections can land first.

## Technical refinement

Before a material mutation, Asgard prepares a proportional technical refinement when it improves the delivery decision. It records the intended outcome, affected artifacts or resources, validation, primary risks, exclusions, dependencies, and authority boundary. Lean work remains concise; infrastructure, database, security, release, and operational work additionally records observed state, expected impact, rollback or recovery, and the approval required for each protected operation.

When repository policy or the user requires a persisted plan, Asgard uses the designated artifact and format. It does not assume an issue, GitHub, or a comment structure. A refinement documents a plan and never grants authority to execute it.

For a standalone, implementation-ready refinement of a specific delivery, invoke **Kvasir**. Kvasir inspects the issue and only the necessary code, selects the smallest adequate approach, and records the resulting plan in a new issue comment when the issue and comment authority are explicit. It does not implement the plan or alter Asgard's general refinement policy.

<p align="center">
  <img src="./plugins/asgard/skills/kvasir/assets/kvasir.png" alt="Kvasir, the Technical Cartographer" width="460">
</p>

```text
Use $kvasir to refine issue #123 before implementation.
```

### Kvasir usage rules

- Use Kvasir for an explicit GitHub issue or a defined delivery demand that needs an implementation-ready technical refinement; do not use it to implement, review completed code, or conduct open-ended product discovery.
- It reads repository instructions and only the issue context, code, tests, contracts, configuration, and documentation that can change the recommended plan.
- With an explicitly named, open issue, Kvasir creates exactly one new Markdown comment after the refinement is final. It never edits the issue body, title, labels, or existing comments. A related issue discovered during analysis is not enough to authorize a comment.
- Without an issue, Kvasir returns the refinement in the conversation and does not create a GitHub artifact.
- The result is `READY` only when implementation can begin without a material decision. Otherwise it is `NEEDS_DECISION` or `BLOCKED`, with the unresolved choice or smallest next action stated explicitly.
- Kvasir records the analyzed base, evidence, minimal recommended approach, implementation map, acceptance scenarios, validation, exclusions, risks, dependencies, and authority boundaries. Database, infrastructure, security, release, and operational work also include observed state, impact, recovery or rollback, and required approvals.
- A refinement never authorizes branches, implementation, commits, Pull Requests, dependency installation, migrations, data changes, infrastructure changes, deployment, or publication.

## Intent catalog

Asgard recognizes natural-language requests as `DISCOVERY`, `DELIVERY`, `REVIEW`, `INFRASTRUCTURE`, `DEPLOY`, or `MONITOR`. It infers a clear intent and asks only when ambiguity would materially change the result, scope, environment, or authority.

Intent never grants authority. Discovery produces a concise, decision-ready brief and stops for approval; it does not create issues or implement. After approval, Asgard may prepare or create issues only when authorized, then enter delivery. Application promotion follows the repository's authorized workflow, while infrastructure work belongs to Ymir. Release PR preparation is handled by the standalone Hermod skill.

Natural examples:

- “Use Asgard para explorar esta ideia.”
- “Use Asgard para desenvolver esta funcionalidade.”
- “Faça o discovery e pare antes de criar as issues.”
- “Faça o discovery e, se eu aprovar, prepare as issues.”
- “Revise este PR quanto a comportamento e segurança.”
- “Planeje esta mudança de infraestrutura, mas não aplique.”
- “Faça deploy da revisão aprovada em staging.”
- “Monitore o CI do PR 42.”

## Delivery modes

- **Lean:** one bounded, low-risk activity with an implementer and Odin review. Add a specialist gate only for an identified risk, including Bragi when maintainability is a stated concern.
- **Standard:** multiple activities or material behavioral risk, with independent Loki and Heimdall review, Tyr when contracts or rules are affected, and Bragi when production code is added or structurally changed.
- **Critical:** security-sensitive, persistent, concurrent, irreversible, regulated, or broadly exposed work, using every applicable independent gate.

## Core flow

```text
Natural-language request
  -> Odin infers intent and records the separate authority ceiling
  -> DISCOVERY produces a decision-ready brief and stops for approval, when requested
  -> repository-policy artifacts are prepared only when authorized
  -> Odin prepares proportional Technical Refinement when useful or policy-required
  -> Odin defines the delivery execution graph and Definition of Done
  -> Brokkr or Sindri implements application work,
     Regin authors database evolution,
     and/or Ymir performs authorized infrastructure work
  -> implementers validate their final activity once
  -> Odin reviews the exact candidate
  -> Tyr validates material contracts when applicable
  -> Loki tests adversarially
  -> Bragi reviews the completed candidate for readability and maintainability when applicable
  -> Heimdall reviews security
  -> Forseti validates required delivery traceability
  -> Odin grants final approval

Any confirmed finding
  -> Odin routes a bounded correction to the original implementer
  -> only affected validations and approvals are repeated
```

Asgard classifies dependencies as sequential, parallel-safe, parallel-with-coordination, or deferred. It does not parallelize work merely to fill agent slots, and it avoids repeating complete reviews when integration creates no new diff or invariant.

CI monitoring remains a bounded operational activity. The watcher stays silent while CI is pending; unchanged CI never summons reviewers or restarts the orchestration graph.

At discussion-to-implementation and implementation-to-review boundaries, Odin replaces accumulated narrative with a compact phase checkpoint containing only the candidate, decisions, changed artifacts, validation, approvals, deviations, open risks, next activity, and remaining authority. When usage is available, final reporting aggregates incremental tokens by role and phase without spending extra turns to reconstruct missing telemetry.

## Definitions of Done and authority

Every activity receives an observable objective, proportionate refinement when useful or policy-required, bounded artifact ownership, dependencies, primary failure mode, focused validation, rejection conditions, and applicable reviewers. Tests normally run once after the implementer has inspected the final diff.

Approval never grants authority to commit, push, open or merge pull requests, publish releases, deploy, migrate data, mutate infrastructure, add dependencies, or perform destructive operations. Repository instructions and explicit user authority remain controlling.

For GitHub, Asgard uses the repository's authorized tooling. It does not silently fall back to an unapproved client when authentication, authorization, scopes, or commands fail. Browser operation is reserved for a documented capability gap and requires an explanation plus explicit user authorization for that exceptional operation.

## Delivery governance

When the repository requires traceability, Forseti checks the policy-required evidence available at each lifecycle phase. That can include issues, branches, pull requests, closing relationships, labels, changelogs, release notes, or checks, but Asgard does not define the taxonomy or make any of them universal.

When policy requires a provider-recognized closing reference, Forseti may repair one absent, unambiguous reference only with authority for that exact edit. Missing evidence that cannot exist yet is `PENDING`; a violated repository invariant is `CHANGES_REQUIRED`. Forseti's approval covers governance only.

## Install the plugin

The `master` branch contains the latest stable release:

```bash
git clone --branch master https://github.com/VissotoFlavio/asgard-codex-skill.git
cd asgard-codex-skill
codex plugin marketplace add .
codex plugin add asgard@asgard-community
```

Start a new Codex task after installation so the plugin and its skill are loaded.

Invoke Asgard explicitly:

```text
Use $asgard to plan and coordinate this software delivery.
```

Codex may also select Asgard automatically when a request clearly matches its scope.

## Update the plugin

Update the stable checkout and reinstall the marketplace entry:

```bash
cd asgard-codex-skill
git switch master
git pull --ff-only origin master
codex plugin add asgard@asgard-community
```

Open a new Codex task after reinstalling.

## Use Hermod directly

Hermod is a standalone skill distributed by this repository. Use it when the task is to prepare and open a release Pull Request without invoking Asgard or Odin:

```text
Use $hermod to prepare and open the release Pull Request from develop to master.
```

Hermod analyzes the candidate changes, selects the next Semantic Version, updates the changelog, validates the final diff, and opens the Pull Request. Merge, tag, publication, deploy, and infrastructure changes require separate authorization.

## Use Eir directly

Eir delivers a defined issue through a Pull Request, publishes evidence-backed review feedback on the Pull Request, applies authorized corrections, replies to the addressed feedback with the solution and validation evidence, and verifies the resulting candidate. It does not merge, deploy, release, or resolve review threads automatically.

<p align="center">
  <img src="./assets/eir.png" alt="Eir, the delivery corrector" width="460">
</p>

```text
Use $eir to review this Pull Request and publish the findings.
```

## Install only the skill

To install the standalone skill instead of the plugin, ask Codex to install:

```text
https://github.com/VissotoFlavio/asgard-codex-skill/tree/master/plugins/asgard/skills/asgard
```

Start a new task after installation and invoke `$asgard`.

To install only Hermod, use:

```text
https://github.com/VissotoFlavio/asgard-codex-skill/tree/master/plugins/asgard/skills/hermod
```

To install only Kvasir, use:

```text
https://github.com/VissotoFlavio/asgard-codex-skill/tree/master/plugins/asgard/skills/kvasir
```

To install only Eir, use:

```text
https://github.com/VissotoFlavio/asgard-codex-skill/tree/master/plugins/asgard/skills/eir
```

Start a new task after installation and invoke `$hermod`, `$kvasir`, or `$eir`.

## Repository and release workflow

- `develop` contains the next candidate changes.
- Every delivery branch follows `{prefix}/{issue-id}-{name}`, where `name` is a short lowercase kebab-case slug and the ID belongs to its authoritative issue. Release branches use `release/<version>` and do not require an issue.
- `feature/<issue-id>-<name>`, `fix/<issue-id>-<name>`, `docs/<issue-id>-<name>`, and related delivery branches originate from and return to `develop`.
- `release/<version>` originates from `develop` and targets `master`.
- `hotfix/<issue-id>-<version>` originates from and targets `master`.
- `master` contains stable, versioned releases.
- Squash is reserved for delivery pull requests created from `develop` and targeting `develop`; release and backport pull requests always use merge commits.
- [CHANGELOG.md](./CHANGELOG.md) is updated for every delivery PR and records each release version; delivery entries include issue and pull-request links.
- [GitHub Releases](https://github.com/VissotoFlavio/asgard-codex-skill/releases) contains stable release notes.

After an approved release merge reaches `master`, the repository workflow validates the version, creates the immutable tag and GitHub Release, and opens a `master` to `develop` backport pull request. The release creates no issue; the backport creates no additional branch or issue. Before completion, the final release description must explicitly list every delivery issue and pull request included in production. Production publication failures leave the tag in place and require a new corrective version.

## Prepare a version

Maintainers can update the authoritative plugin version without creating a commit, tag, or release automatically:

```bash
python scripts/bump_version.py patch
python scripts/bump_version.py minor
python scripts/bump_version.py major
python scripts/bump_version.py 1.2.3
python scripts/bump_version.py patch --dry-run
```

The release workflow creates the tag and GitHub Release only after the version change is approved and merged through the normal release pull request.

## Portability

Asgard adapts to the available agent capacity, version-control system, isolation mechanism, repository policy, and publication workflow. GitHub-specific mechanics are used only when the repository and authorized tooling support them.

## License

[MIT](./LICENSE)
