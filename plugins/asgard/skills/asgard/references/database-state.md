# Database profile and inventory contract

Persist profiles and inventories outside repositories and installed skills. Use `ASGARD_CONFIG_HOME/databases`; otherwise `%LOCALAPPDATA%\Asgard\databases` on Windows, `${XDG_CONFIG_HOME:-$HOME/.config}/asgard/databases` on Linux, or `~/Library/Application Support/Asgard/databases` on macOS. Resolve with native platform APIs. An override must be non-empty and absolute. Canonicalize the destination, sanitize profile IDs, and reject repositories, installed skills, shared or over-permissive directories, traversal, symlinks, and reparse points. Create atomically with private user-only permissions and verify them; failure blocks persistence.

On first use of each profile, require separate read-only DISCOVER authority bound to the exact target, identity, scope, access level/principal, and credential mechanism; absence blocks connection. Keep metadata transient. Persistence consent is separate from connection authority: disclose the resolved destination and content classes and obtain explicit profile-scoped consent before writing. Record the policy; scope or destination changes require fresh consent. Refresh only consented, verified sections.

For a containerized database on a VPS, also follow `references/database-vps-access.md`; tunnel availability and an opaque credential reference grant no database authority.

## Profile

Profiles contain no secrets. Record name, environment, engine/provider, endpoint alias, non-secret port, database/catalog, schema/tenant or scoped-object namespace, authorized scope, freshness policy, last validation, credential mechanism and opaque reference, plus an identity tuple distinguishing account/tenant, server/cluster, database, schema/tenant, region, and engine/version as applicable.

Never store passwords, tokens, keys, certificates, connection strings, secret environment values, copied credentials, row/sample values, or query logs. Obtain credentials through masked tooling or provider-native storage, never chat or agent context. Function/view bodies default to a digest; exact text requires explicit need and consent.

Keep source-repository and database evidence distinct: migrations are desired state; inventory is observed state. Never conflate them. The live database is authoritative at runtime.

## Inventory

Shard inventory into `manifest`, `summary`, `migrations`, `relations`, `schemas`, and `tables`. Load manifest and summary first, then only task-relevant objects and sections to reduce tokens. Task relevance includes engine-aware transitive dependencies such as FKs, views, triggers, policies, and functions; unknown, denied, or incomplete closure requires broader refresh and blocks APPLY.

Record schema/collector versions, identity tuple, collection time, access level, and scope. Bind every shard to one generation ID and checksum. Stage under an exclusive lock, then atomically publish the complete generation. Readers reject mixed, interrupted, malformed, corrupt, checksum-invalid, or unsupported generations as `INVALID`. Per section record freshness, provenance, completeness, unknowns, denials, and state: `VALID`, `PARTIAL`, `STALE`, `DRIFTED`, or `INVALID`.

Refresh on TTL expiry, migration/deploy, repository migration-head change, missing or partial objects, engine/version or identity change, drift, partial failure, or explicit refresh. Full rebuild is allowed only for corrupt or unsupported-schema state, through DISCOVER plus persistence consent.

## APPLY safety

Stale or partial state may guide AUTHOR but never authorize APPLY. Immediately before APPLY, query live read-only and verify identity tuple including schema/tenant, effective principal, migration head, exact candidate revision/migration set, and affected dependency closure. Unknown, denied, or incomplete dependencies block APPLY. Mismatch or material drift invalidates candidate and authority: rediscover, revise impact and recovery, and obtain fresh approval.

On partial APPLY or VERIFY failure, halt mutation, rediscover actual migration state, checkpoints, and committed effects, and update only consented, verified sections; preserve partial or unknown status elsewhere. Report the blocker. Retry, repair, rollback, or further mutation always requires new authority bound to that actual state, recovery action, exact candidate, and environment; prior authority cannot be reused.
