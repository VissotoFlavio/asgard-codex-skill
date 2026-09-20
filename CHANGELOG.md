# Changelog

All notable changes to this project are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Require database-related issues and pull requests to carry the composable `database` discipline label alongside their nature labels ([issue #102](https://github.com/VissotoFlavio/asgard-codex-skill/issues/102), [PR #104](https://github.com/VissotoFlavio/asgard-codex-skill/pull/104)).

## [0.10.5] - 2026-09-15

Release PR: [#95](https://github.com/VissotoFlavio/asgard-codex-skill/pull/95)

### Changed

- Require every Asgard-created branch to include its authoritative issue ID in `{prefix}/{issue-id}-{name}` format ([issue #92](https://github.com/VissotoFlavio/asgard-codex-skill/issues/92), [PR #93](https://github.com/VissotoFlavio/asgard-codex-skill/pull/93)).

## [0.10.4] - 2026-09-14

Release PR: [#90](https://github.com/VissotoFlavio/asgard-codex-skill/pull/90)

### Changed

- Require merge commits for release and backport pull requests, reserving squash for delivery branches created from and targeting `develop` ([issue #88](https://github.com/VissotoFlavio/asgard-codex-skill/issues/88), [PR #89](https://github.com/VissotoFlavio/asgard-codex-skill/pull/89)).

## [0.10.3] - 2026-09-13

Release PR: [#86](https://github.com/VissotoFlavio/asgard-codex-skill/pull/86)

### Changed

- Allow release-only flows to version and publish approved delivery inventories without creating a release issue, while preserving delivery traceability and repository overrides ([issue #84](https://github.com/VissotoFlavio/asgard-codex-skill/issues/84), [PR #85](https://github.com/VissotoFlavio/asgard-codex-skill/pull/85)).

## [0.10.2] - 2026-09-13

Release PR: [#82](https://github.com/VissotoFlavio/asgard-codex-skill/pull/82).

### Changed

- Centralize GitHub Actions observation in Hermod with one blocking watcher per revision, reuse its terminal evidence in Odin and Forseti, and reserve one fresh provider read for the immediate pre-merge gate ([issue #80](https://github.com/VissotoFlavio/asgard-codex-skill/issues/80), [PR #81](https://github.com/VissotoFlavio/asgard-codex-skill/pull/81)).

## [0.10.1] - 2026-09-13

Release PR: [#78](https://github.com/VissotoFlavio/asgard-codex-skill/pull/78).

### Changed

- Make the authenticated GitHub CLI the default for every GitHub interaction, minimize structured output, and reserve browser operation for explicitly authorized, documented CLI/API capability gaps ([issue #76](https://github.com/VissotoFlavio/asgard-codex-skill/issues/76), [PR #77](https://github.com/VissotoFlavio/asgard-codex-skill/pull/77)).

## [0.10.0] - 2026-09-13

Release PR: [#74](https://github.com/VissotoFlavio/asgard-codex-skill/pull/74).

### Added

- Add natural-language routing for discovery, delivery, review, infrastructure, deploy, release, and monitor; introduce an Odin-owned Discovery Brief, keep Mimir limited to read-only technical uncertainty, preserve explicit authority boundaries, and align the README with the skill ([issue #72](https://github.com/VissotoFlavio/asgard-codex-skill/issues/72), [PR #73](https://github.com/VissotoFlavio/asgard-codex-skill/pull/73)).

## [0.9.0] - 2026-09-11

Release PR: [#70](https://github.com/VissotoFlavio/asgard-codex-skill/pull/70).

### Changed

- Reduce orchestration context with phase checkpoints, fresh specialist contexts that do not recursively invoke Asgard, proportional execution budgets, bounded reports and evidence, narrower implicit selection, and incremental usage telemetry by role and phase ([issue #68](https://github.com/VissotoFlavio/asgard-codex-skill/issues/68), [PR #69](https://github.com/VissotoFlavio/asgard-codex-skill/pull/69)).

## [0.8.2] - 2026-09-11

Release PR: [#66](https://github.com/VissotoFlavio/asgard-codex-skill/pull/66).

### Changed

- Isolate Hermod CI monitoring from delivery history, wait silently through unchanged pending states, route failures without restarting every reviewer, bound retries, and record incremental token telemetry ([issue #64](https://github.com/VissotoFlavio/asgard-codex-skill/issues/64), [PR #65](https://github.com/VissotoFlavio/asgard-codex-skill/pull/65)).

## [0.8.1] - 2026-09-09

Release PR: [#62](https://github.com/VissotoFlavio/asgard-codex-skill/pull/62).

### Changed

- Make Forseti automatically add and verify `Closes #<issue>` on eligible delivery pull requests when the authoritative issue is unambiguous and PR edit authority is recorded ([issue #60](https://github.com/VissotoFlavio/asgard-codex-skill/issues/60), [PR #61](https://github.com/VissotoFlavio/asgard-codex-skill/pull/61)).

## [0.8.0] - 2026-09-09

Release PR: [#58](https://github.com/VissotoFlavio/asgard-codex-skill/pull/58).

### Added

- Add Bragi as the independent final-candidate reviewer for human-readable, maintainable code, with context-sensitive SOLID, DRY, KISS, YAGNI, and Tell, Don't Ask guidance and official artwork ([issue #56](https://github.com/VissotoFlavio/asgard-codex-skill/issues/56), [PR #57](https://github.com/VissotoFlavio/asgard-codex-skill/pull/57)).

## [0.7.2] - 2026-09-08

Release PR: [#54](https://github.com/VissotoFlavio/asgard-codex-skill/pull/54).

### Changed

- Exempt operational release and backport pull requests from separate issues while requiring final release notes to enumerate every delivered issue and pull request ([issue #52](https://github.com/VissotoFlavio/asgard-codex-skill/issues/52), [PR #53](https://github.com/VissotoFlavio/asgard-codex-skill/pull/53)).

## [0.7.1] - 2026-09-08

Release tracking: [issue #46](https://github.com/VissotoFlavio/asgard-codex-skill/issues/46), [PR #49](https://github.com/VissotoFlavio/asgard-codex-skill/pull/49).

### Added

- Publish the complete Asgard agent-card artwork in the repository and plugin gallery ([issue #44](https://github.com/VissotoFlavio/asgard-codex-skill/issues/44), [PR #45](https://github.com/VissotoFlavio/asgard-codex-skill/pull/45)).

### Changed

- Refresh the README for the current roles, modes, governance, installation, and release workflow while keeping only the primary image visible ([issue #47](https://github.com/VissotoFlavio/asgard-codex-skill/issues/47), [PR #48](https://github.com/VissotoFlavio/asgard-codex-skill/pull/48)).

## [0.7.0] - 2026-09-08

Release tracking: [issue #40](https://github.com/VissotoFlavio/asgard-codex-skill/issues/40), [PR #41](https://github.com/VissotoFlavio/asgard-codex-skill/pull/41).

### Added

- Add Forseti as the delivery-governance specialist, with independent issue-to-release traceability gates and official artwork ([issue #38](https://github.com/VissotoFlavio/asgard-codex-skill/issues/38), [PR #39](https://github.com/VissotoFlavio/asgard-codex-skill/pull/39)).

[Unreleased]: https://github.com/VissotoFlavio/asgard-codex-skill/compare/v0.10.5...develop
[0.10.5]: https://github.com/VissotoFlavio/asgard-codex-skill/compare/v0.10.4...v0.10.5
[0.10.4]: https://github.com/VissotoFlavio/asgard-codex-skill/compare/v0.10.3...v0.10.4
[0.10.3]: https://github.com/VissotoFlavio/asgard-codex-skill/compare/v0.10.2...v0.10.3
[0.10.2]: https://github.com/VissotoFlavio/asgard-codex-skill/compare/v0.10.1...v0.10.2
[0.10.1]: https://github.com/VissotoFlavio/asgard-codex-skill/compare/v0.10.0...v0.10.1
[0.10.0]: https://github.com/VissotoFlavio/asgard-codex-skill/compare/v0.9.0...v0.10.0
[0.9.0]: https://github.com/VissotoFlavio/asgard-codex-skill/compare/v0.8.2...v0.9.0
[0.8.2]: https://github.com/VissotoFlavio/asgard-codex-skill/compare/v0.8.1...v0.8.2
[0.8.1]: https://github.com/VissotoFlavio/asgard-codex-skill/compare/v0.8.0...v0.8.1
[0.8.0]: https://github.com/VissotoFlavio/asgard-codex-skill/compare/v0.7.2...v0.8.0
[0.7.2]: https://github.com/VissotoFlavio/asgard-codex-skill/compare/v0.7.1...v0.7.2
[0.7.1]: https://github.com/VissotoFlavio/asgard-codex-skill/compare/v0.7.0...v0.7.1
[0.7.0]: https://github.com/VissotoFlavio/asgard-codex-skill/compare/v0.6.0...v0.7.0
