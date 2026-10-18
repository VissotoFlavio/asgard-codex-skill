# Database discipline

Load for schema, migration, index, partition, or backfill work. Supplements Regin; grants no connection or mutation authority. Follow [database profile and inventory](database-state.md) for persisted state and [VPS database access](database-vps-access.md) for container access through a VPS.

## Activity contract

Define engine/version, artifacts, entities, current/desired structure, compatibility, volume, sequence, and evidence. Analyze the whole model.

Specify columns/types/nullability/defaults, PK/FK, constraints, indexes, relations, and partitions. Check integrity, query paths, referential actions, order, and compatibility. Prefer expand/contract; contract only after verified consumers/data and separate approval.

For each migration/backfill, state transactions, locks, volume, batching, idempotency, checkpoints, resumability, partial failure, verification, reversibility, and recovery. Flag lossy steps.

## Authority phases

- `AUTHOR`: edit versioned schema, migration, backfill, and verification artifacts only; never connect or run DDL/DML.
- Before `VALIDATE`/`APPLY`, require a clean-tree revision or canonical digest of every artifact, including untracked. Divergence invalidates evidence and authority.
- `VALIDATE`: execute that candidate only on an authorized isolated target with synthetic or approved sanitized data.
- `APPLY`: any durable, runtime, or non-isolated database mutation; require exact candidate/environment authority. Manual APPLY is Regin's only with a declared adapter; absence blocks. The repository's authorized deploy automation executes.
- Before execution, freshly compare expected and observed cluster/server, database/catalog, schema/tenant, and effective principal/role. Missing or mismatched fields fail closed.

Use least privilege per phase. Owner/superuser or grants need justification and separate Ymir authorization. Ymir owns infrastructure, roles, credentials, and connectivity. No phase implies sensitive-data access.

Drift invalidates plan/authority. Stop on identity ambiguity, unsafe locks, unbounded volume, or unverifiable recovery. After partial failure, halt mutation; rediscover actual migration state, checkpoints, and commits; report them; require new authority bound to observed state before continue, repair, retry, or rollback.

When integrity/compatibility, recovery behavior, or security/availability needs an independent role, return `HANDOFF_REQUIRED` recommending `$asgard:tyr`, `$asgard:loki`, or `$asgard:heimdall` respectively; never invoke it. Regin never self-approves.
