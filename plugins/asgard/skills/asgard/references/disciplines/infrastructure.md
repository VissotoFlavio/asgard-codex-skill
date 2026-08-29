# Infrastructure discipline

Load this packet for work on hosts, cloud resources, networks, OS services, container platforms, runtime configuration, or infrastructure access. It supplements Ymir and grants no authority.

## Profile and inventory contract

Use `references/infrastructure-state.md` for profiles and inventories. Remote read-only discovery does not authorize durable local writes. Profiles locate a destination and reference external credentials; inventories are observed metadata snapshots. Neither may contain secrets.

Before dispatch, record provider, required tools and skills, availability, expected identity, access level, and whether APPLY may be requested. Provider skills are capabilities, not permission sources.

For SSH/Linux, confirm first-use identity out of band, prefer SSH agent/config, and discover only authorized metadata. Detect OS, architecture, systemd, Docker/Compose, relevant services, and bounded workloads. Never disable host-key checking, scan arbitrary filesystems, read secret files, or capture environment values.

For AWS, only detect AWS CLI, profile/SSO, expected account/role/region, adapter, and required skills. Do not install or operate without user authority and suitable capability. Other providers fail closed likewise.

## Infrastructure invariants

Follow `DISCOVER -> PLAN -> APPLY -> VERIFY`. Before APPLY, revalidate identity and affected state; absent, unverifiable, or mismatched identity fails closed. Material drift invalidates the plan and authority, requiring a regenerated plan, impact, recovery path, and fresh approval. Stale, corrupt, malformed, or unsupported state cannot authorize APPLY. On partial APPLY or failed VERIFY, halt mutation, rediscover and report actual state; rollback and retries require exact authority. Credentials, migrations, deployment, destructive actions, firewall or privilege changes, restarts, infrastructure mutation, persistence, and dependency installation remain protected unless explicitly authorized.

Route material contracts and state consistency to Tyr, behavioral and recovery failure modes to Loki, and identity, secrets, privilege, exposure, or availability to independent Heimdall review. Remote execution evidence never constitutes final acceptance.
