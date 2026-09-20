# Database discipline

Load for schema, migration, index, partitioning, or backfill work. Supplements Regin; grants no connection or mutation authority.

## Activity contract

Define engine/version, artifacts, entities/relations, current/desired structure, compatibility, volume/traffic, sequence, and evidence. Analyze the whole model.

Specify columns/types/nullability/defaults, PK/FK/unique/check constraints, indexes, relations, and partitions. Check integrity, query paths, write amplification, referential actions, naming, order, and compatibility. Prefer expand/contract; contract only after verified consumers/data and separate approval.

For each migration/backfill, state transactions, locks, volume, batching, throttling, idempotency, checkpoints, resumability, partial failure, verification, reversibility, and recovery. Down migrations do not prove safe rollback; flag lossy steps.

## Authority phases

- `AUTHOR`: edit versioned schema, migration, backfill, and verification artifacts only; never connect or run DDL/DML.
- Before `VALIDATE`/`APPLY`, require an immutable candidate: clean-tree review or canonical digest of every artifact, including untracked. Divergence invalidates validation, approval, and authority.
- `VALIDATE`: execute that candidate only on an authorized isolated target with synthetic or approved sanitized data.
- `APPLY`: any durable, runtime, or non-isolated database mutation, shared or not; require exact candidate/environment authority. Standalone/manual APPLY is Regin's only with a declared adapter/capability; absence blocks. In deploy, repository deploy automation executes; Hermod promotes/monitors only.
- Before execution, freshly compare expected and observed cluster/server, database/catalog, schema/tenant, and effective principal/role. Missing or mismatched fields fail closed.

Use least privilege per phase. Owner/superuser or grants need justification and separate Ymir authorization. Ymir owns infrastructure, roles, credentials, and connectivity. No phase implies sensitive-data access.

Drift invalidates plan/authority. Stop on identity ambiguity, unsafe locks, unbounded volume, or unverifiable recovery. After partial failure, halt mutation; rediscover actual migration state, checkpoints, and commits; report them; require new authority bound to observed state before continue, repair, retry, or rollback.

Route integrity/compatibility to Tyr, recovery to Loki, and security/availability to Heimdall. Regin never self-approves.
