# Infrastructure profile and inventory contract

Keep persistent infrastructure state outside the installed skill and repository unless the repository explicitly defines a safe project-local mapping. Resolve the state root from `ASGARD_CONFIG_HOME` when explicitly configured; otherwise use `%LOCALAPPDATA%\Asgard\infrastructure` on Windows, `${XDG_CONFIG_HOME:-$HOME/.config}/asgard/infrastructure` on Linux, and `~/Library/Application Support/Asgard/infrastructure` on macOS. Use restrictive permissions and separate `profiles` from `inventories`. Never write state into the installed skill, where an update could replace it.

DISCOVER is remote read-only and initially collects metadata transiently. Before a durable local write, disclose the exact destination and content class and obtain explicitly scoped persistence consent. Record that policy in the profile. Later verified refreshes may update only the approved profile state under that policy; changed scope or destination requires fresh consent. Persistence never includes secrets.

## Profile

A profile may contain a stable name, environment classification, transport/provider, host alias or provider profile, port and user when non-secret, expected host fingerprint or account identity, region, credential mechanism type and opaque reference, authorized scope, and last validation time.

It must not contain passwords, passphrases, private keys, access keys, session tokens, certificate private material, secret environment values, or copied credential files. Collect secrets only through a masked local tool or provider-native login that writes directly to SSH agent/config, OS keyring, SSO, or provider credential storage; chat and agent context must never carry the value.

First use requires identity confirmation through a trusted out-of-band channel. Identity absent, unverifiable, or mismatched fails closed. Validate it on every connection and immediately before APPLY; a mismatch stops work and requires explicit reauthorization, never an automatic profile rewrite.

## Inventory

An inventory is a timestamped, bounded snapshot with schema and collector versions, profile identity, collection time, provenance, access level, scope, completeness, and unknown or denied sections. It may record operating-system identity, architecture, capabilities, service names and versions, Docker/Compose projects, container/image identifiers, health, published ports, networks, volumes, and secret names when necessary. Never record secret contents or environment-variable values.

Prefer trusted labels and Compose metadata when grouping containers into applications. Mark inference confidence and persist user-confirmed grouping. Do not recursively scan filesystems or inspect unrelated workloads merely to make the snapshot appear complete.

Reject malformed, corrupt, or unsupported-schema state and rebuild it only through discovery plus persistence consent. Inventory is stale when its recorded freshness policy has expired or affected objects were not revalidated; stale state may guide discovery but never PLAN approval or APPLY. Remote state is authoritative.

Refresh volatile state when relevant and re-read every affected object immediately before mutation. Material drift invalidates the plan and APPLY authority: regenerate plan, impact, verification and recovery, then obtain fresh approval. Never silently overwrite drift.

On partial APPLY or VERIFY failure, halt further mutation, rediscover actual partial state, truthfully update only consented inventory sections, and report the blocker. Rollback is a separate mutation allowed only by prior exact authority or fresh authority. Retry only bounded, authorized operations; otherwise remain blocked. After success, persist only verified sections with timestamps and provenance.
