# Role Routing Index

Use this index only when role selection is unclear. The main skill links directly to each role packet so unused roles do not enter context.

| Need | Role | Packet |
|---|---|---|
| Orchestration and final acceptance | Odin | [agents/odin.md](agents/odin.md) |
| Bounded implementation with established architecture | Brokkr | [agents/brokkr.md](agents/brokkr.md) |
| Inseparable architectural implementation | Sindri | [agents/sindri.md](agents/sindri.md) |
| Infrastructure discovery, planning, execution, and verification | Ymir | [agents/ymir.md](agents/ymir.md) |
| Read-only uncertainty reduction | Mimir | [agents/mimir.md](agents/mimir.md) |
| Rules, contracts, compatibility, or consistency review | Tyr | [agents/tyr.md](agents/tyr.md) |
| Adversarial behavior and edge-case review | Loki | [agents/loki.md](agents/loki.md) |
| Security, privacy, isolation, abuse, or availability review | Heimdall | [agents/heimdall.md](agents/heimdall.md) |
| Approved version-control and release promotion | Hermod | [agents/hermod.md](agents/hermod.md) |

Odin is the primary agent. It owns the graph, DoDs, routing, integration, evidence review, correction decisions, and final acceptance.

## Shared packet contract

Send only the selected role packet plus:

- the activity objective, DoD, rejection conditions, and primary failure mode;
- relevant paths or the exact candidate diff/revision;
- applicable repository rules and explicit exclusions;
- the applicable discipline packet and explicitly required skills;
- stable dependency state and focused validation commands;
- authority boundaries for edits and external mutations.

Do not attach the full conversation when this task-local contract is sufficient. Agent output should contain only decisions or findings, changed artifacts when applicable, validation evidence, deviations, unresolved risks, and blockers. Omit repeated instructions and empty fields.
