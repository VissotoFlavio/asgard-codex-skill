# Backend discipline

Load this packet for an activity that owns server-side application behavior, APIs, services, persistence, integrations, or background processing. It supplements Brokkr or Sindri; it does not replace the implementer's role packet or create shared ownership.

## .NET capability

When the owned production or test artifacts are .NET or C#, require `$dotnet-best-practices` in the activity contract and confirm that it is available before dispatch. The implementer must use that skill before making implementation decisions and apply the guidance relevant to the affected solution and project.

Repository instructions, target-framework constraints, and established solution conventions take precedence over generic skill recommendations. Do not introduce a test framework, package, namespace scheme, architectural pattern, localization system, Semantic Kernel, or other dependency merely because the skill mentions it. Record any material conflict and the chosen project-compatible interpretation.

For mixed-stack activities, apply the skill only to the .NET-owned artifacts and keep validation scoped to the affected projects. Prefer the smallest relevant build and test commands; do not expand to the full solution without a concrete cross-project risk or repository requirement.

## Backend invariants

Put only affected invariants in the DoD. Consider public contracts, authorization, validation, persistence, transactions, idempotency, concurrency, retries, partial failures, observability, and compatibility when the activity can change them. Route material contract or consistency risk to Tyr, adversarial behavior to Loki, and security or availability risk to Heimdall.

Database migrations, infrastructure changes, deployment, and new dependencies remain unauthorized unless the user explicitly grants that authority.
