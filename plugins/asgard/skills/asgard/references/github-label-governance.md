# GitHub classification labels

Classify every authoritative issue and eligible pull request on two independent axes. Labels are cumulative: classification never forces a cross-boundary activity into only one category.

## Nature

Require at least one repository-defined nature label describing what the work is, such as `bug`, `enhancement`, `documentation`, or `release`. Repositories may define additional nature labels. A status, priority, team, or automation label does not satisfy this requirement.

## Discipline

Apply every discipline materially affected by the work. A database activity always requires `database`; this includes schema design or evolution, tables, columns, data types, primary or foreign keys, constraints, indexes, relationships, partitions, migrations, persisted-data backfills, or database compatibility. Database classification may coexist with `backend`, `frontend`, `infrastructure`, or another repository-defined discipline.

The authoritative issue and its eligible pull request must carry the same required nature and discipline classification. Operational labels may differ. If the repository is missing a required label, label creation is an external mutation and requires explicit authority; otherwise stop before issue or pull-request creation. Missing, incomplete, or inconsistent classification is `CHANGES_REQUIRED` and blocks governance approval.

When preparing an issue or pull request, record the selected nature and disciplines with a short rationale. Re-evaluate them when scope changes; adding a database concern later requires `database` on both artifacts before approval.
