# Infrastructure discipline

Load this guidance for work on hosts, cloud resources, networks, OS services, container platforms, runtime configuration, or infrastructure access. It supplements the `$asgard:ymir` leaf skill and grants no authority.

## Canonical operational guidance

Route infrastructure work to `$asgard:ymir`; its skill-local guidance is canonical for profiles, inventories, VPS container database access, credentials, identity, drift, and partial-failure controls. This root guidance grants no authority and does not duplicate those operational policies.

Before dispatch, record provider, required tools and skills, availability, expected identity, access level, and whether `APPLY` may be requested. Provider skills are capabilities, not permission sources.

For SSH/Linux, require first-use identity confirmation out of band and define only the authorized discovery boundary: OS, architecture, systemd, Docker/Compose, relevant services, and bounded workloads. `$asgard:ymir` applies its canonical transport and secret-handling controls.

For AWS, record AWS CLI, profile/SSO, expected account/role/region, adapter, and required skills. Do not install or operate without user authority and suitable capability. Other providers fail closed likewise.

## Infrastructure invariants

Require `$asgard:ymir` to follow its canonical `DISCOVER -> PLAN -> APPLY -> VERIFY` model. The task-local contract must state the exact authority, expected impact, recovery, verification, and protected operations; the root guidance does not restate or grant operational controls.

Select `$asgard:tyr` for material contracts or state consistency, `$asgard:loki` for behavioral or recovery failure modes, and `$asgard:heimdall` for identity, secrets, privilege, exposure, or availability review when their independent boundary is justified. Odin selects these leaf skills. Remote execution evidence never constitutes final acceptance.
