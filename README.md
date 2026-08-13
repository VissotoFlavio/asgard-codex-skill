<p align="center">
  <img src="./assets/logo_asgard.png" alt="Asgard for Codex" width="760">
</p>

# Asgard for Codex

Asgard is a multi-agent software delivery workflow for Codex. It separates implementation from acceptance and coordinates focused specialists through explicit Definitions of Done, adversarial testing, security review, correction loops, and optional publication gates.

## Roles

- **Odin** orchestrates the delivery and owns final acceptance.
- **Brokkr** implements bounded work with an established architecture.
- **Sindri** owns complex architectural implementation.
- **Mimir** investigates code, documentation, and technical uncertainty.
- **Tyr** validates rules, contracts, compatibility, and consistency.
- **Loki** searches for edge cases and tries to break the candidate.
- **Heimdall** performs independent security review and reports every finding.

<p align="center">
  <img src="./assets/asgard-agents.png" alt="Asgard agents, responsibilities, and delivery flow" width="720">
</p>

## Core flow

```text
Odin plans and defines the DoD
  -> Brokkr or Sindri implements
  -> Odin reviews against the DoD
  -> Tyr validates contracts when applicable
  -> Loki tests adversarially
  -> Heimdall reviews security
  -> Odin grants final approval

Any finding -> Odin -> original implementer -> affected reviews
```

Approval of the execution graph covers the described implementation and internal correction cycles. The workflow returns to the user for changed scope, product decisions, protected operations, or genuine blockers—not for every internal handoff.

## Install the plugin

The `master` branch contains the latest stable release. Clone it, register the repository as a Codex marketplace, and install Asgard:

```bash
git clone --branch master https://github.com/VissotoFlavio/asgard-codex-skill.git
cd asgard-codex-skill
codex plugin marketplace add .
codex plugin add asgard@asgard-community
```

Start a new Codex task after installation so the plugin and its skill are loaded. You can then invoke it explicitly:

```text
Use $asgard to plan and coordinate this software delivery.
```

You can also describe a substantial multi-agent delivery naturally; Codex may select Asgard when the request matches its purpose.

## Update the plugin

Pull the latest stable release and reinstall the marketplace entry:

```bash
cd asgard-codex-skill
git switch master
git pull --ff-only origin master
codex plugin add asgard@asgard-community
```

Open a new Codex task after updating so the new version is picked up.

## Install only the skill

If you do not want the complete plugin, ask Codex to install the skill directly from:

```text
https://github.com/VissotoFlavio/asgard-codex-skill/tree/master/plugins/asgard/skills/asgard
```

Then start a new task and invoke `$asgard`.

## Repository channels

- `master`: stable, versioned releases intended for installation.
- `develop`: upcoming changes that may not yet be released.
- [GitHub Releases](https://github.com/VissotoFlavio/asgard-codex-skill/releases): published versions and release history.

## Portability

Asgard adapts to available agent slots, version-control systems, isolation mechanisms, and publication workflows. Git branches, worktrees, pull requests, and merges are optional. Repository instructions and user permissions always take precedence.

## License

MIT
