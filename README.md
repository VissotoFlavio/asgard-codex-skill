<p align="center">
  <img src="./assets/asgard-agents.png" alt="Asgard agents, responsibilities, and delivery flow" width="760">
</p>

# Asgard for Codex

Asgard is a risk-based, multi-agent discovery and software delivery workflow for Codex. Odin frames decisions, decomposes substantial work into bounded activities, assigns focused specialists, reviews their evidence, coordinates independent gates, and remains accountable for final acceptance.

The workflow is intentionally proportional: routine changes should stay simple, while complex or high-risk deliveries receive stronger implementation, contract, adversarial, security, governance, and publication controls.

## When to use Asgard

Use Asgard when it is explicitly requested for discovery, delivery, review, infrastructure, deploy, release, or monitoring, or when work benefits from one or more of the following:

- decision-ready discovery before implementation;
- multiple bounded implementation activities;
- coordinated application and infrastructure work;
- explicit acceptance criteria and dependency ordering;
- independent behavioral, contract, or security review;
- high-assurance deployment or release promotion with traceable evidence;
- explicit monitoring or monitoring within a governed delivery or release flow.

Do not select it implicitly for routine single-file edits, isolated diagnosis, ordinary maintenance, or standalone release observation that one agent can handle safely. Explicit monitoring remains supported. Asgard should reduce delivery risk, not add ceremony without a concrete reason.

## Roles

| Role | Responsibility |
| --- | --- |
| **Odin** | Plans the execution graph, coordinates specialists, reviews evidence, and owns final acceptance. |
| **Brokkr** | Implements bounded application work within an established architecture. |
| **Sindri** | Implements one inseparable application activity that requires architectural ownership. |
| **Ymir** | Discovers, plans, applies authorized infrastructure changes, and verifies the resulting environment. |
| **Mimir** | Resolves a stated code, documentation, or technical uncertainty. |
| **Tyr** | Independently validates material rules, contracts, compatibility, and consistency. |
| **Loki** | Searches adversarially for behavioral gaps and edge cases. |
| **Bragi** | Reviews completed code for human readability and maintainability using context-sensitive SOLID, DRY, KISS, YAGNI, and Tell, Don't Ask. |
| **Heimdall** | Independently reviews security, privacy, isolation, abuse, and availability risks. |
| **Forseti** | Enforces issue, pull-request, changelog, and release traceability, including the narrowly authorized automatic `Closes #<issue>` repair. |
| **Hermod** | Promotes an approved revision through explicitly authorized version-control and release operations. |

Specialists receive task-local context rather than the entire conversation. Their reports and passing tests are evidence; Odin still owns product decisions, inspects the candidate, and makes the acceptance decision. Mimir only resolves stated technical uncertainty read-only.

Odin applies Asgard once: specialist tasks do not invoke `$asgard` again. Multi-phase deliveries use compact checkpoints, fresh agent contexts, bounded reports, and a proportional default budget of three simultaneous agents and one grouped correction cycle. Exact paths, revisions, run URLs, and validation conclusions replace copied transcripts, full diffs, and successful logs.

## Intent catalog

Asgard recognizes natural-language requests as `DISCOVERY`, `DELIVERY`, `REVIEW`, `INFRASTRUCTURE`, `DEPLOY`, `RELEASE`, or `MONITOR`. It infers a clear intent and asks only when ambiguity would materially change the result, scope, environment, or authority.

Intent never grants authority. Discovery produces a concise, decision-ready brief and stops for approval; it does not create issues or implement. After approval, Asgard may prepare or create issues only when authorized, then enter delivery. Application promotion belongs to Hermod, while infrastructure work belongs to Ymir. Release publication and infrastructure mutation remain separately protected operations.

Natural examples:

- “Use Asgard para explorar esta ideia.”
- “Use Asgard para desenvolver esta funcionalidade.”
- “Faça o discovery e pare antes de criar as issues.”
- “Faça o discovery e, se eu aprovar, prepare as issues.”
- “Revise este PR quanto a comportamento e segurança.”
- “Planeje esta mudança de infraestrutura, mas não aplique.”
- “Faça deploy da revisão aprovada em staging.”
- “Prepare a release 2.4.0 sem publicar.”
- “Monitore o CI do PR 42.”

## Delivery modes

- **Lean:** one bounded, low-risk activity with an implementer and Odin review. Add a specialist gate only for an identified risk, including Bragi when maintainability is a stated concern.
- **Standard:** multiple activities or material behavioral risk, with independent Loki and Heimdall review, Tyr when contracts or rules are affected, and Bragi when production code is added or structurally changed.
- **Critical:** security-sensitive, persistent, concurrent, irreversible, regulated, or broadly exposed work, using every applicable independent gate.
- **Release:** an approved candidate promoted by Hermod after required Forseti traceability and explicit mutation authority are recorded.

## Core flow

```text
Natural-language request
  -> Odin infers intent and records the separate authority ceiling
  -> DISCOVERY produces a decision-ready brief and stops for approval, when requested
  -> approved issue preparation or creation occurs only when authorized
  -> Odin defines the delivery execution graph and Definition of Done
  -> Brokkr or Sindri implements application work
     and/or Ymir performs authorized infrastructure work
  -> implementers validate their final activity once
  -> Odin reviews the exact candidate
  -> Tyr validates material contracts when applicable
  -> Loki tests adversarially
  -> Bragi reviews the completed candidate for readability and maintainability when applicable
  -> Heimdall reviews security
  -> Forseti validates required delivery traceability
  -> Odin grants final approval
  -> Hermod promotes the approved revision when authorized

Any confirmed finding
  -> Odin routes a bounded correction to the original implementer
  -> only affected validations and approvals are repeated
```

Asgard classifies dependencies as sequential, parallel-safe, parallel-with-coordination, or deferred. It does not parallelize work merely to fill agent slots, and it avoids repeating complete reviews when integration creates no new diff or invariant.

CI monitoring stays inside Hermod as one context-isolated, blocking `gh pr checks --watch` or `gh run watch` process per revision. Hermod is the sole owner of live Actions queries and returns revision-bound terminal evidence, then performs one final head and merge-gate read immediately before an authorized merge. Odin coordinates from that evidence and Forseti validates its coverage without querying Actions again. The watcher remains silent while CI is pending; unchanged CI never summons reviewers or restarts the orchestration graph.

At discussion-to-implementation, implementation-to-review, and approval-to-release boundaries, Odin replaces accumulated narrative with a compact phase checkpoint containing only the candidate, decisions, changed artifacts, validation, approvals, deviations, open risks, next activity, and remaining authority. When usage is available, final reporting aggregates incremental tokens by role and phase without spending extra turns to reconstruct missing telemetry.

## Definitions of Done and authority

Every activity receives an observable objective, bounded artifact ownership, dependencies, primary failure mode, focused validation, rejection conditions, and applicable reviewers. Tests normally run once after the implementer has inspected the final diff.

Approval never grants authority to commit, push, open or merge pull requests, publish releases, deploy, migrate data, mutate infrastructure, add dependencies, or perform destructive operations. Repository instructions and explicit user authority remain controlling.

For GitHub, Asgard uses the authenticated `gh` CLI for issues, pull requests, reviews, checks, workflows, merges, tags, and releases, requesting only the structured fields needed. It does not silently fall back to a browser when authentication, authorization, scopes, or commands fail. Browser operation is reserved for a documented CLI/API capability gap and requires an explanation plus explicit user authorization for that exceptional operation.

## Delivery governance

When the repository requires traceability, Forseti checks the evidence available at each lifecycle phase:

1. one bounded issue defines new delivery work and its acceptance criteria when repository policy requires it;
2. every created branch is named `{prefix}/{issue-id}-{name}` using its authoritative issue, and the pull request identifies the same issue with a provider-recognized `Closes #<issue>` relationship;
3. required labels, templates, reviews, and checks are present;
4. the changelog links the issue and pull request;
5. the final published release description explicitly enumerates every included delivery issue and pull request;
6. a release has its own authoritative issue and uses `release/<issue-id>-<version>`; the CI-created `master` to `develop` backport creates no additional branch and reuses that issue.

GitHub classification uses two cumulative axes. Every authoritative issue and eligible pull request has at least one nature label, such as `bug`, `enhancement`, `documentation`, or `release`, plus every materially affected discipline. Database schema, tables, columns, keys, constraints, indexes, relationships, migrations, backfills, or compatibility work always requires `database`. Cross-boundary work may also carry labels such as `backend` or `infrastructure`; one discipline never hides another. Required nature and discipline labels must agree between the issue and its pull request, while operational labels may differ.

When an eligible delivery PR lacks its closing reference, Forseti appends a standalone `Closes #<issue>` line automatically if exactly one open, same-repository issue is authoritative and PR edit authority is already recorded. It preserves the existing body, performs at most one edit, and verifies the provider-recognized relationship afterward. Ambiguous or conflicting issue candidates require correction instead of guessing. Missing evidence that cannot exist yet is `PENDING`; a violated invariant is `CHANGES_REQUIRED`. Forseti's approval covers governance only.

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

## Install only the skill

To install the standalone skill instead of the plugin, ask Codex to install:

```text
https://github.com/VissotoFlavio/asgard-codex-skill/tree/master/plugins/asgard/skills/asgard
```

Start a new task after installation and invoke `$asgard`.

## Repository and release workflow

- `develop` contains the next candidate changes.
- Every created branch follows `{prefix}/{issue-id}-{name}`, where `name` is a short lowercase kebab-case slug and the ID belongs to its authoritative issue.
- `feature/<issue-id>-<name>`, `fix/<issue-id>-<name>`, `docs/<issue-id>-<name>`, and related delivery branches originate from and return to `develop`.
- `release/<issue-id>-<version>` originates from `develop` and targets `master`.
- `hotfix/<issue-id>-<version>` originates from and targets `master`.
- `master` contains stable, versioned releases.
- Squash is reserved for delivery pull requests created from `develop` and targeting `develop`; release and backport pull requests always use merge commits.
- [CHANGELOG.md](./CHANGELOG.md) records deliveries with issue and pull-request links.
- [GitHub Releases](https://github.com/VissotoFlavio/asgard-codex-skill/releases) contains stable release notes.

After an approved release merge reaches `master`, the repository workflow validates the version, creates the immutable tag and GitHub Release, and opens a `master` to `develop` backport pull request. The release requires an authoritative issue; the backport creates no additional branch and reuses that issue. Before completion, the final release description must explicitly list every delivery issue and pull request included in production. Production publication failures leave the tag in place and require a new corrective version.

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
