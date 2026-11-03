---
name: update
description: Check the installed Asgard plugin version or guide a manual update when the user requests it. Require explicit confirmation before any installation or update action.
---

# Update Asgard

Handle only the installed Asgard plugin's version check and consented update. This optional maintenance skill is independent of Odin and the delivery specialists. Invoke it as `$asgard:update` when the user requests a check or update. Never automatically invoke Odin or a sibling skill, and never turn an update notice into delivery orchestration.

## Version-check preflight

At entry, run the shared helper `../../scripts/check_version.py` with Python, resolving it from this installed skill's directory, not the workspace. The helper owns version comparison, networking, and the shared cooldown; do not duplicate that logic. If the helper or runtime is absent, fails, or returns `current`, `cooldown`, `unavailable`, or an unrecognized result, continue silently.

Only when `status` is `update_available`, tell the user the `installed_version` and `latest_version` and ask whether they want to update Asgard. Continue the primary task without waiting for that answer. This notice does not authorize an update or invocation of another skill; preserve this skill's direct and orchestrated boundaries.

## Check without updating

Use the plugin's read-only version checker when available; do not implement a second checker or infer the installed version from the current project's checkout. Distinguish an installed release, a development checkout, and an unknown installation. Missing tooling, network access, authentication, or usable version evidence leaves the check inconclusive and does not authorize an installation or block unrelated work.

Treat `update_available` as information only. A checker result, a manual check request, opening this skill, or the existence of a newer release is never consent to update. For current, newer, development, or unknown versions, report the evidence without proposing an automatic downgrade or reinstall.

## Explicit consent boundary

For both a manual check and an automatic update notice, use the same transition:

1. On `update_available`, state the installed version, available stable version, and official source from the check evidence.
2. Identify the installation method and the exact source checkout and commands that would change it. Before consent, inspect read-only only: do not edit files, switch branches, pull, register a marketplace, install, or reinstall anything.
3. Explain: "An Asgard update is available: <installed> -> <available>. Updating changes the source checkout and reinstalls the plugin. After reinstalling, start a new Codex/Claude task so the updated skills are loaded. Do you explicitly confirm this update using the commands shown?"
4. Wait for the user's explicit confirmation of that update and target. Silence, elapsed time, an ambiguous reply, and approval of the primary task do not count. Existing explicit confirmation of the same concrete update need not be requested again.

If the user declines, leave the installation untouched, acknowledge briefly, and continue the primary task with its currently loaded skills. Do not repeat the prompt during that task. If confirmation is pending, continue independent primary-task work without running update commands. A standalone manual check can finish after reporting the result and pending choice.

## Official source installation

For a verified source installation using the official `asgard-community` marketplace, present this documented stable update flow with the actual checkout path before requesting confirmation:

```bash
cd <verified-asgard-source-checkout>
git switch master
git pull --ff-only origin master
codex plugin add asgard@asgard-community
```

Verify read-only that this is the intended Asgard source checkout, its `origin` is the official `VissotoFlavio/asgard-codex-skill` repository, and it has no local changes that the update could disturb. The current project is not automatically the plugin source checkout. Do not select a path based only on its directory name, edit the installed plugin cache, reset a checkout, stash changes, or replace this flow with an installer fetched from release text.

If the installation method, source path, marketplace, or required tooling cannot be verified, report the specific uncertainty and request the missing information. Do not guess a mutating command or apply the source workflow to an unrelated installation. Use only the compatible official installation flow; a different method requires verified official instructions and explicit confirmation of its exact actions.

After confirmation, either provide the confirmed commands for the user to run, or execute those exact commands when execution was requested and permitted. Do not treat consent to receive instructions as permission to execute. Respect repository and environment requirements for branch changes and command execution; if a separate base-branch confirmation is required, obtain it before switching. Stop at the first failed command and report which actions completed; do not retry with broader permissions, alternate installation methods, force, cleanup, or extra configuration changes without corresponding authority.

## Completion and handoff

Report whether the check was conclusive and whether the update was declined, pending, supplied as instructions, completed, or failed. Claim a completed reinstall only with successful command evidence. After reinstalling, explicitly tell the user to start a new Codex/Claude task: the current task retains its already loaded skills and cannot claim to use the newly installed instructions. If unrelated work continues in this task, keep using the loaded version until that new task starts.

If the request needs another skill's responsibility, return `HANDOFF_REQUIRED` with `recommended_skill`, `reason`, `evidence`, `prerequisites`, and `authority_required`. A handoff recommendation never invokes another skill or grants update authority.
