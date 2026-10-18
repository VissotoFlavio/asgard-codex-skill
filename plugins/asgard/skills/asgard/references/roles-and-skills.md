# Odin routing catalog

Use this catalog to select a direct skill or an Odin-orchestrated activity. Every skill is directly invokable and stays within its own boundary. Odin alone chooses and sequences skills in a governed delivery; a direct skill never invokes Odin or a sibling automatically.

| Need | Direct skill | Boundary |
|---|---|---|
| Implementation-ready technical refinement | `$asgard:kvasir` | Refine one defined issue or delivery demand without implementing it. |
| Read-only uncertainty reduction | `$asgard:mimir` | One stated technical uncertainty. |
| Application implementation or a designated Pull Request correction | `$asgard:brokkr` | One authoritative issue with explicit task context or exact correction scope; stops at the ready candidate. |
| Database architecture and versioned evolution | `$asgard:regin` | One database-structure activity under explicit AUTHOR, VALIDATE, or APPLY authority. |
| Infrastructure discovery, planning, execution, and verification | `$asgard:ymir` | One infrastructure activity under explicit DISCOVER, PLAN, APPLY, or VERIFY authority. |
| Rules, contracts, compatibility, or consistency review | `$asgard:tyr` | One exact candidate and supplied DoD. |
| Adversarial behavior and edge-case review | `$asgard:loki` | One exact candidate's credible behavioral risks. |
| Human readability, maintainability, and code quality review | `$asgard:bragi` | One completed immutable candidate. |
| Security, privacy, isolation, abuse, availability, or deep vulnerability review | `$asgard:heimdall` | One exact candidate and bounded attack surface. |
| Required issue, pull-request, and delivery traceability | `$asgard:forseti` | Read-only traceability, except its narrow authorized closing-reference repair. |
| Pull Request publication | `$asgard:hermod` | Open one authorized normal or release Pull Request from a ready candidate. |
| Pull Request acceptance validation | `$asgard:eir` | Review or verify one ready Pull Request against its issue and acceptance criteria. |

Odin remains the sole orchestrator and delivery owner. Canonical intent does not itself select a mutation or grant authority. Odin owns discovery and decision-making; Mimir may supply only read-only evidence for a stated technical uncertainty. Application promotion follows the repository's authorized workflow through Hermod when Pull Request publication is authorized, while infrastructure discovery or mutation routes to Ymir. A deploy request that includes both becomes coordinated, separately authorized activities.

## Shared dispatch contract

Send each selected skill a task-local contract containing:

- the activity objective, DoD, rejection conditions, and primary failure mode;
- relevant paths or the exact candidate diff/revision;
- applicable repository rules and explicit exclusions;
- the applicable discipline guidance and explicitly required skills;
- stable dependency state and focused validation commands; and
- authority boundaries for edits and external mutations.

Do not mention or invoke `$asgard:asgard` in a specialist task; its policy has already been applied by Odin. Do not attach the full conversation when this task-local contract is sufficient. Use a fresh context without inherited history when available.

Reference exact paths, revisions, and bounded diff commands rather than attaching full diffs. Reference validation artifacts rather than pasting successful logs. Include a short sanitized excerpt only when a failure cannot be understood without it.

Skill output should stay within the activity's report budget and contain only decisions or findings, changed artifacts when applicable, validation evidence, deviations, unresolved risks, and blockers. Omit repeated instructions, role guidance, successful command output, and empty fields.
