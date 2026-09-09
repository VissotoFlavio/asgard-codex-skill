<p align="center">
  <img src="./assets/asgard-agents.png" alt="Asgard agents, responsibilities, and delivery flow" width="760">
</p>

# Asgard for Codex

Asgard is a risk-based, multi-agent software delivery workflow for Codex. Odin decomposes substantial work into bounded activities, assigns focused specialists, reviews their evidence, coordinates independent gates, and remains accountable for final acceptance.

The workflow is intentionally proportional: routine changes should stay simple, while complex or high-risk deliveries receive stronger implementation, contract, adversarial, security, governance, and publication controls.

## When to use Asgard

Use Asgard for deliveries that benefit from one or more of the following:

- multiple bounded implementation activities;
- coordinated application and infrastructure work;
- explicit acceptance criteria and dependency ordering;
- independent behavioral, contract, or security review;
- high-assurance release promotion with traceable evidence.

Do not use it for routine single-file edits or ordinary work that one agent can implement and verify safely. Asgard should reduce delivery risk, not add ceremony without a concrete reason.

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
| **Forseti** | Verifies issue, pull-request, changelog, and release traceability without accepting or publishing the delivery. |
| **Hermod** | Promotes an approved revision through explicitly authorized version-control and release operations. |

Specialists receive task-local context rather than the entire conversation. Their reports and passing tests are evidence; Odin still inspects the candidate and makes the acceptance decision.

## Delivery modes

- **Lean:** one bounded, low-risk activity with an implementer and Odin review. Add a specialist gate only for an identified risk, including Bragi when maintainability is a stated concern.
- **Standard:** multiple activities or material behavioral risk, with independent Loki and Heimdall review, Tyr when contracts or rules are affected, and Bragi when production code is added or structurally changed.
- **Critical:** security-sensitive, persistent, concurrent, irreversible, regulated, or broadly exposed work, using every applicable independent gate.
- **Release:** an approved candidate promoted by Hermod after required Forseti traceability and explicit mutation authority are recorded.

## Core flow

```text
Odin defines the execution graph and Definition of Done
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

## Definitions of Done and authority

Every activity receives an observable objective, bounded artifact ownership, dependencies, primary failure mode, focused validation, rejection conditions, and applicable reviewers. Tests normally run once after the implementer has inspected the final diff.

Approval never grants authority to commit, push, open or merge pull requests, publish releases, deploy, migrate data, mutate infrastructure, add dependencies, or perform destructive operations. Repository instructions and explicit user authority remain controlling.

## Delivery governance

When the repository requires traceability, Forseti checks the evidence available at each lifecycle phase:

1. one bounded issue defines new delivery work and its acceptance criteria when repository policy requires it;
2. the delivery branch and pull request identify that issue;
3. required labels, templates, reviews, and checks are present;
4. the changelog links the issue and pull request;
5. the final published release description explicitly enumerates every included delivery issue and pull request;
6. operational release and backport pull requests do not require separate issues unless repository policy explicitly overrides that exemption.

Missing evidence that cannot exist yet is reported as `PENDING`; a violated invariant is `CHANGES_REQUIRED`. Forseti is read-only and its approval covers governance only.

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
- `feature/*`, `fix/*`, `docs/*`, and related delivery branches originate from and return to `develop`.
- `release/<version>` originates from `develop` and targets `master`.
- `hotfix/<version>` originates from and targets `master`.
- `master` contains stable, versioned releases.
- [CHANGELOG.md](./CHANGELOG.md) records deliveries with issue and pull-request links.
- [GitHub Releases](https://github.com/VissotoFlavio/asgard-codex-skill/releases) contains stable release notes.

After an approved release merge reaches `master`, the repository workflow validates the version, creates the immutable tag and GitHub Release, and opens a `master` to `develop` backport pull request. Release and backport pull requests are operational and do not require their own issues by default. Before completion, the final release description must explicitly list every delivery issue and pull request included in production. Production publication failures leave the tag in place and require a new corrective version.

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
