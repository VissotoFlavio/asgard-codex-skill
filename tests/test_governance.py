from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validate_repository", ROOT / "scripts" / "validate_repository.py")
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)

LEAF_SKILLS = frozenset({"brokkr", "regin", "ymir", "mimir", "tyr", "loki", "bragi", "heimdall", "forseti"})


def skill_root(name: str) -> Path:
    return ROOT / "plugins" / "asgard" / "skills" / name


def plugin_invocation(name: str) -> str:
    return f"$asgard:{name}"


def temporary_directory() -> tempfile.TemporaryDirectory[str]:
    return tempfile.TemporaryDirectory(dir=ROOT)


def write_skill(root: Path, name: str) -> Path:
    skill = root / name
    (skill / "agents").mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: A valid test skill.\n---\n\n# {name}\n",
        encoding="utf-8",
    )
    (skill / "agents" / "openai.yaml").write_text(
        "interface:\n"
        f"  display_name: \"{name}\"\n"
        "  short_description: \"A valid test skill\"\n"
        "  default_prompt: \"Use this test skill.\"\n",
        encoding="utf-8",
    )
    return skill


class SemVerTests(unittest.TestCase):
    def test_accepts_strict_semver(self) -> None:
        for value in ("0.1.0", "1.2.3-alpha.1", "1.0.0+build.5", "1.0.0-0A"):
            self.assertTrue(VALIDATOR.is_semver(value), value)

    def test_rejects_invalid_semver(self) -> None:
        for value in (None, 1, "01.2.3", "1.02.3", "1.2.03", "1.0.0-01", "1.0.0-alpha..1", "1.0.0+", "1.0"):
            self.assertFalse(VALIDATOR.is_semver(value), value)


class ContainedPathTests(unittest.TestCase):
    def test_rejects_invalid_types_and_escape(self) -> None:
        with temporary_directory() as directory:
            root = Path(directory)
            for value in (None, 7, "", "../outside", "/absolute", "folder\\file"):
                with self.assertRaises(ValueError, msg=repr(value)):
                    VALIDATOR.contained_path(root, value, kind="file")

    def test_accepts_existing_contained_file(self) -> None:
        with temporary_directory() as directory:
            root = Path(directory)
            child = root / "assets" / "logo.png"
            child.parent.mkdir()
            child.write_bytes(b"png")
            self.assertEqual(VALIDATOR.contained_path(root, "assets/logo.png", kind="file"), child.resolve())

    def test_rejects_symlink_escape_when_supported(self) -> None:
        with temporary_directory() as directory, temporary_directory() as outside:
            root = Path(directory)
            link = root / "escape"
            try:
                link.symlink_to(Path(outside), target_is_directory=True)
            except OSError:
                self.skipTest("symlink creation is unavailable")
            with self.assertRaises(ValueError):
                VALIDATOR.contained_path(root, "escape/file", kind="file")

    def test_skill_local_markdown_links_resolve(self) -> None:
        for root in VALIDATOR.discover_distributed_skills().values():
            for markdown in VALIDATOR.markdown_files(root, VALIDATOR.SKILLS_ROOT):
                self.assertEqual(
                    VALIDATOR.validate_local_markdown_links(markdown, skills_root=VALIDATOR.SKILLS_ROOT),
                    [],
                    str(markdown),
                )

    def test_distributed_skills_have_complete_direct_artifacts(self) -> None:
        skills = VALIDATOR.discover_distributed_skills()
        self.assertTrue(VALIDATOR.EXPECTED_SKILLS.issubset(skills))
        for name, root in skills.items():
            self.assertEqual(VALIDATOR.validate_distributed_skill(name, root), [], name)
            skill = (root / "SKILL.md").read_text(encoding="utf-8")
            metadata = (root / "agents" / "openai.yaml").read_text(encoding="utf-8")
            self.assertEqual(VALIDATOR.parse_skill_frontmatter(skill, name=name)["name"], name)
            self.assertEqual(
                set(VALIDATOR.parse_agent_interface(metadata, name=name)),
                {"display_name", "short_description", "default_prompt"},
            )

    def test_manifest_skills_must_resolve_to_the_canonical_publication_root(self) -> None:
        with temporary_directory() as directory:
            plugin = Path(directory) / "plugin"
            canonical = plugin / "skills"
            alternate = plugin / "other-skills"
            canonical.mkdir(parents=True)
            alternate.mkdir()

            self.assertEqual(
                VALIDATOR.resolve_published_skills_root(
                    "./skills/",
                    plugin_root=plugin,
                    canonical_skills_root=canonical,
                ),
                canonical.resolve(),
            )
            with self.assertRaises(ValueError):
                VALIDATOR.resolve_published_skills_root(
                    "./other-skills",
                    plugin_root=plugin,
                    canonical_skills_root=canonical,
                )

    def test_future_well_formed_skills_are_discovered_and_validated(self) -> None:
        with temporary_directory() as directory:
            published_root = Path(directory) / "skills"
            published_root.mkdir()
            future = write_skill(published_root, "future")

            discovered = VALIDATOR.discover_distributed_skills(published_root)
            self.assertEqual(discovered, {"future": future.resolve()})
            self.assertEqual(
                VALIDATOR.validate_distributed_skill("future", future, skills_root=published_root),
                [],
            )

    def test_rejects_symlinked_skill_directory_when_supported(self) -> None:
        with temporary_directory() as directory:
            root = Path(directory)
            published_root = root / "skills"
            outside = root / "outside"
            published_root.mkdir()
            outside.mkdir()
            link = published_root / "linked"
            try:
                link.symlink_to(outside, target_is_directory=True)
            except OSError:
                self.skipTest("symlink creation is unavailable")
            with self.assertRaises(ValueError):
                VALIDATOR.discover_distributed_skills(published_root)

    def test_rejects_malformed_frontmatter_and_agent_metadata(self) -> None:
        with self.assertRaises(ValueError):
            VALIDATOR.parse_skill_frontmatter("name: example\n", name="example")
        with self.assertRaises(ValueError):
            VALIDATOR.parse_skill_frontmatter("---\nname: example\ndescription: true\n---\n", name="example")
        with self.assertRaises(ValueError):
            VALIDATOR.parse_skill_frontmatter("---\nname:\n  nested: example\ndescription: text\n---\n", name="example")

        for metadata in (
            "interface: invalid\n",
            "interface:\n    display_name: \"Example\"\n",
            "interface:\n  display_name: true\n  short_description: \"Short\"\n  default_prompt: \"Prompt\"\n",
            "interface:\n  metadata:\n    display_name: \"Example\"\n  short_description: \"Short\"\n  default_prompt: \"Prompt\"\n",
        ):
            with self.assertRaises(ValueError, msg=metadata):
                VALIDATOR.parse_agent_interface(metadata, name="example")

    def test_required_yaml_strings_reject_comments_and_mapping_syntax(self) -> None:
        invalid_frontmatter_values = (
            "# comment",
            "Direct skill: bounded review",
            "null",
            "[]",
        )
        for value in invalid_frontmatter_values:
            frontmatter = f"---\nname: example\ndescription: {value}\n---\n"
            with self.assertRaises(ValueError, msg=frontmatter):
                VALIDATOR.parse_skill_frontmatter(frontmatter, name="example")

        invalid_interface_values = (
            "# comment",
            "Display name: review",
            "null",
            "[]",
        )
        for value in invalid_interface_values:
            metadata = (
                "interface:\n"
                f"  display_name: {value}\n"
                "  short_description: Short description\n"
                "  default_prompt: Use this skill.\n"
            )
            with self.assertRaises(ValueError, msg=metadata):
                VALIDATOR.parse_agent_interface(metadata, name="example")

        self.assertEqual(
            VALIDATOR.parse_skill_frontmatter(
                "---\nname: example\ndescription: Direct bounded review.\n---\n",
                name="example",
            )["description"],
            "Direct bounded review.",
        )
        self.assertEqual(
            VALIDATOR.parse_agent_interface(
                "interface:\n"
                "  display_name: \"Example: review\"\n"
                "  short_description: Short description\n"
                "  default_prompt: \"Use this skill: safely.\"\n",
                name="example",
            )["display_name"],
            "Example: review",
        )

    def test_required_yaml_strings_reject_all_single_quoted_syntax(self) -> None:
        single_quoted_values = (
            "'Direct bounded review'",
            "'Bob's review'",
        )
        for value in single_quoted_values:
            frontmatter = f"---\nname: example\ndescription: {value}\n---\n"
            with self.assertRaises(ValueError, msg=frontmatter):
                VALIDATOR.parse_skill_frontmatter(frontmatter, name="example")

            metadata = (
                "interface:\n"
                f"  display_name: {value}\n"
                "  short_description: Short description\n"
                "  default_prompt: Use this skill.\n"
            )
            with self.assertRaises(ValueError, msg=metadata):
                VALIDATOR.parse_agent_interface(metadata, name="example")

    def test_leaf_skills_keep_direct_handoff_contracts(self) -> None:
        terminal_states = {
            "brokkr": ("`IMPLEMENTER_COMPLETE`", "`BLOCKED`"),
            "regin": ("`IMPLEMENTER_COMPLETE`", "`BLOCKED`"),
            "ymir": ("`IMPLEMENTER_COMPLETE`", "`BLOCKED`"),
            "mimir": ("`FINDINGS_COMPLETE`", "`BLOCKED`"),
            "tyr": ("`APPROVED`", "`CHANGES_REQUIRED`", "`BLOCKED`"),
            "loki": ("`APPROVED`", "`CHANGES_REQUIRED`", "`BLOCKED`"),
            "bragi": ("`APPROVED`", "`CHANGES_REQUIRED`", "`BLOCKED`"),
            "heimdall": ("`APPROVED`", "`CHANGES_REQUIRED`", "`BLOCKED`"),
            "forseti": ("`APPROVED`", "`PENDING`", "`CHANGES_REQUIRED`", "`BLOCKED`"),
        }
        self.assertEqual(frozenset(terminal_states), LEAF_SKILLS)
        for name, states in terminal_states.items():
            skill = (skill_root(name) / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("**Direct mode:**", skill, name)
            self.assertIn("**Odin-orchestrated mode:**", skill, name)
            self.assertIn("Never automatically invoke another Asgard skill", skill, name)
            self.assertIn("recursively invoke Odin", skill, name)
            for field in ("HANDOFF_REQUIRED", "recommended_skill:", "reason:", "evidence:", "prerequisites:", "authority_required:"):
                self.assertIn(field, skill, f"{name}: {field}")
            self.assertIn("recommended_skill: $asgard:<skill>", skill, name)
            self.assertIn("authority_required: <specific protected authority, or none>", skill, name)
            self.assertIn("`HANDOFF_REQUIRED`", skill, name)
            for state in states:
                self.assertIn(state, skill, f"{name}: {state}")

    def test_leaf_artifacts_use_canonical_roots_and_retire_root_specialist_state(self) -> None:
        published_root = VALIDATOR.SKILLS_ROOT.resolve()
        for name in LEAF_SKILLS:
            root = skill_root(name)
            self.assertTrue(root.resolve().is_relative_to(published_root), name)
            self.assertEqual(VALIDATOR.validate_distributed_skill(name, root), [], name)
            for markdown in VALIDATOR.markdown_files(root, published_root):
                self.assertTrue(markdown.resolve().is_relative_to(published_root), str(markdown))

        references = VALIDATOR.SKILL_ROOT / "references"
        for retired in (
            "roles-and-packets.md",
            "database-state.md",
            "database-vps-access.md",
            "infrastructure-state.md",
        ):
            self.assertFalse((references / retired).exists(), retired)
        self.assertEqual(list((references / "agents").glob("*.md")), [])

    def test_plugin_invocation_guidance_uses_qualified_skill_names(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        manifest = (ROOT / "plugins" / "asgard" / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        catalog = (VALIDATOR.SKILL_ROOT / "references" / "roles-and-skills.md").read_text(encoding="utf-8")

        for name in VALIDATOR.EXPECTED_SKILLS:
            invocation = plugin_invocation(name)
            metadata = (skill_root(name) / "agents" / "openai.yaml").read_text(encoding="utf-8")
            prompt = VALIDATOR.parse_agent_interface(metadata, name=name)["default_prompt"]
            self.assertIn(invocation, prompt, name)
            self.assertIn(invocation, readme, name)

        self.assertIn(plugin_invocation("asgard"), manifest)
        for name in LEAF_SKILLS:
            self.assertIn(plugin_invocation(name), catalog, name)
        self.assertIn(
            "The plugin distributes 13 skills. Invoke every plugin-provided Asgard skill with the `asgard:` namespace.",
            readme,
        )
        self.assertIn("## Install an independent workflow", readme)
        self.assertIn("$eir`, `$hermod`, or `$kvasir`", readme)
        for name in ("eir", "hermod", "kvasir"):
            metadata = (skill_root(name) / "agents" / "openai.yaml").read_text(encoding="utf-8")
            prompt = VALIDATOR.parse_agent_interface(metadata, name=name)["default_prompt"]
            self.assertIn(f"${name}", prompt, name)

    def test_asgard_discipline_guidance_is_loadable(self) -> None:
        disciplines = VALIDATOR.SKILL_ROOT / "references" / "disciplines"
        expected = {"backend", "database", "frontend", "infrastructure", "security"}
        self.assertEqual({path.stem for path in disciplines.glob("*.md")}, expected)
        for discipline in expected:
            guidance = (disciplines / f"{discipline}.md").read_text(encoding="utf-8")
            self.assertTrue(guidance.strip(), discipline)
        backend = (disciplines / "backend.md").read_text(encoding="utf-8")
        self.assertIn("$dotnet-best-practices", backend)
        self.assertIn("route structural ownership to `$asgard:regin`", backend)
        database = (disciplines / "database.md").read_text(encoding="utf-8")
        for term in ("AUTHOR", "VALIDATE", "APPLY", "keys", "indexes", "expand/contract"):
            self.assertIn(term, database)
        frontend = (disciplines / "frontend.md").read_text(encoding="utf-8")
        self.assertIn("$frontend-design", frontend)
        self.assertIn("$web-design-guidelines", frontend)
        infrastructure = (disciplines / "infrastructure.md").read_text(encoding="utf-8")
        self.assertIn("`$asgard:ymir` leaf skill", infrastructure)
        self.assertIn("skill-local guidance is canonical", infrastructure)
        self.assertIn("DISCOVER -> PLAN -> APPLY -> VERIFY", infrastructure)
        self.assertIn("Remote execution evidence never constitutes final acceptance", infrastructure)
        security = (disciplines / "security.md").read_text(encoding="utf-8")
        self.assertIn("$api-security-review", security)
        self.assertIn("$web-security-review", security)
        self.assertIn("ask the user whether to install it", security)
        self.assertIn("continue with Heimdall's native review", security)
        self.assertIn("--validate-security", security)

        definition = (VALIDATOR.SKILL_ROOT / "references" / "definition-of-done.md").read_text(encoding="utf-8")
        self.assertIn("Implementing skill: $asgard:brokkr | $asgard:regin | $asgard:ymir", definition)
        self.assertIn("For deep vulnerability analysis, record `Security`", definition)

    def test_heimdall_deep_security_analysis_uses_optional_skills_with_fallback(self) -> None:
        skill = (VALIDATOR.SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        heimdall = (skill_root("heimdall") / "SKILL.md").read_text(encoding="utf-8")
        security = (skill_root("heimdall") / "references" / "security.md").read_text(encoding="utf-8")
        roles = (VALIDATOR.SKILL_ROOT / "references" / "roles-and-skills.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("references/disciplines/security.md", skill)
        self.assertIn("deep vulnerability analysis", skill)
        self.assertIn("[security guidance](references/security.md)", heimdall)
        self.assertIn("Installing a skill is optional and requires explicit user authorization", security)
        self.assertIn("API gateways, webhooks, API authentication", security)
        self.assertIn("XSS/CSRF risk, security headers, CORS", security)
        self.assertIn("deep vulnerability review", roles)
        self.assertIn("Odin asks whether to install it", readme)
        self.assertIn("records the fallback", readme)
        self.assertIn("Run it when requested, required by repository policy, or justified by material risk", readme)

    def test_regin_owns_database_structure_without_implicit_runtime_authority(self) -> None:
        skill = (VALIDATOR.SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        roles = (VALIDATOR.SKILL_ROOT / "references" / "roles-and-skills.md").read_text(encoding="utf-8")
        regin = (skill_root("regin") / "SKILL.md").read_text(encoding="utf-8")
        database = (skill_root("regin") / "references" / "database.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("references/roles-and-skills.md", skill)
        self.assertIn("references/disciplines/database.md", skill)
        self.assertIn("Database architecture and versioned evolution", roles)
        self.assertIn("# Regin", regin)
        self.assertIn("Never self-approve", regin)
        self.assertIn("one never authorizes another", regin)
        self.assertIn("clean-tree review or canonical digest of every artifact, including untracked", regin)
        self.assertIn("durable, runtime, or non-isolated database mutation", regin)
        self.assertIn("durable, runtime, or non-isolated database mutation", database)
        self.assertIn("any durable, runtime, or non-isolated database", readme)
        self.assertIn("return `HANDOFF_REQUIRED` to obtain an authorized adapter or authority", regin)
        self.assertIn("repository's authorized deploy automation executes", regin)
        self.assertNotIn("Hermod applies", regin)
        self.assertIn("cluster/server, database/catalog, schema/tenant, and effective principal/role", regin)
        self.assertIn("Missing or mismatched fields fail closed", regin)
        self.assertIn("phase-scoped least privilege", regin)
        self.assertIn("Owner/superuser or grants need justification", regin)
        self.assertIn("separate Ymir authority", regin)
        self.assertIn("After partial failure, halt mutation", regin)
        self.assertIn("new authority bound to that state", regin)
        self.assertIn("| **Regin** |", readme)
        self.assertNotIn("reginpng.png", readme.lower())


    def test_database_inventory_is_compact_persistent_and_never_apply_authority(self) -> None:
        state = (skill_root("regin") / "references" / "database-state.md").read_text(encoding="utf-8")
        regin = (skill_root("regin") / "SKILL.md").read_text(encoding="utf-8")
        database = (skill_root("regin") / "references" / "database.md").read_text(encoding="utf-8")
        definition = (VALIDATOR.SKILL_ROOT / "references" / "definition-of-done.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        for path in (
            "ASGARD_CONFIG_HOME/databases",
            "%LOCALAPPDATA%\\Asgard\\databases",
            "${XDG_CONFIG_HOME:-$HOME/.config}/asgard/databases",
            "~/Library/Application Support/Asgard/databases",
        ):
            self.assertIn(path, state)
        for section in ("`manifest`", "`summary`", "`migrations`", "`relations`", "`schemas`", "`tables`"):
            self.assertIn(section, state)
        for inventory_state in ("`VALID`", "`PARTIAL`", "`STALE`", "`DRIFTED`", "`INVALID`"):
            self.assertIn(inventory_state, state)

        self.assertIn("require separate read-only DISCOVER authority", state)
        self.assertIn("Persistence consent is separate from connection authority", state)
        self.assertIn("explicit profile-scoped consent", state)
        self.assertIn("only task-relevant objects and sections to reduce tokens", state)
        self.assertIn("migrations are desired state; inventory is observed state", state)
        self.assertIn("Never store passwords, tokens, keys, certificates, connection strings", state)
        self.assertIn("Function/view bodies default to a digest", state)
        self.assertIn("Stale or partial state may guide AUTHOR but never authorize APPLY", state)
        self.assertIn("Immediately before APPLY, query live read-only", state)
        self.assertIn("engine-aware transitive dependencies", state)
        self.assertIn("atomically publish the complete generation", state)
        self.assertIn("reject mixed, interrupted, malformed, corrupt", state)
        self.assertIn("prior authority cannot be reused", state)
        self.assertIn("schema/tenant or scoped-object namespace", state)
        self.assertIn("override must be non-empty and absolute", state)
        self.assertIn("reject repositories, installed skills", state)
        self.assertIn("On partial APPLY or VERIFY failure, halt mutation", state)
        self.assertIn("database-state.md", regin)
        self.assertIn("database-state.md", database)
        self.assertIn("profile and inventory state", definition)
        self.assertIn("compact summary and only relevant object details", readme)
        self.assertIn("never authorize `APPLY`", readme)

    def test_vps_container_database_access_separates_network_credentials_and_authority(self) -> None:
        access = (skill_root("regin") / "references" / "database-vps-access.md").read_text(encoding="utf-8")
        database_state = (skill_root("regin") / "references" / "database-state.md").read_text(encoding="utf-8")
        infrastructure_state = (skill_root("ymir") / "references" / "infrastructure-state.md").read_text(encoding="utf-8")
        database = (skill_root("regin") / "references" / "database.md").read_text(encoding="utf-8")
        infrastructure = (skill_root("ymir") / "references" / "infrastructure.md").read_text(encoding="utf-8")
        definition = (VALIDATOR.SKILL_ROOT / "references" / "definition-of-done.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("bind it only to the VPS loopback address", access)
        self.assertIn("Public or wildcard publication such as `0.0.0.0` or `::` is forbidden by default", access)
        self.assertIn("Use a local SSH forward from an exclusively bound loopback-only", access)
        self.assertIn("Require host-key verification and confirmed forward establishment", access)
        self.assertIn("Reject occupied or stale listeners", access)
        self.assertIn("verify the listener belongs to the bounded tunnel", access)
        self.assertIn("approved host-scoped SSH identity", access)
        self.assertIn("effective remote principal and access level", access)
        self.assertIn("SSH identity and database credentials are independent", access)
        for principal in ("application runtime", "read-only `DISCOVER`", "isolated `VALIDATE`", "migration `APPLY`", "emergency administration"):
            self.assertIn(principal, access)
        self.assertIn("opaque references", access)
        self.assertIn("command arguments, process environment, reports, logs, traces", access)
        self.assertIn("fail closed when only literal argv/environment delivery is available", access)
        self.assertIn("database `CREATE ROLE`, `GRANT`, `ALTER`, and `REVOKE` are Regin `APPLY` mutations", access)
        self.assertIn("Ymir never grants database authority", access)
        self.assertIn("A break-glass exception requires exact Ymir", access)
        self.assertIn("exact Regin operation authority", access)
        self.assertIn("revoke or expire access immediately afterward", access)
        self.assertIn("credential generation/version or provider change token", access)
        self.assertIn("even when the opaque reference is stable", access)
        self.assertIn("Before opening transport, Ymir verifies the expected VPS/host key", access)
        self.assertIn("After SSH authentication and confirmed forward establishment", access)
        self.assertIn("Only then may the database session be established", access)
        self.assertIn("image digest/version, network, and exact host-to-container bindings", access)
        self.assertIn("After the authenticated database session is established but before any database operation", access)
        self.assertIn("Tunnel establishment authorizes no database operation", access)
        self.assertIn("never automatically retry a mutation", access)
        self.assertIn("database-vps-access.md", database_state)
        self.assertIn("database-vps-access.md", infrastructure_state)
        self.assertIn("database-vps-access.md", database)
        self.assertIn("database-vps-access.md", infrastructure)
        self.assertIn("verified SSH/tunnel identities", definition)
        self.assertIn("loopback-only SSH local forward", readme)
        self.assertIn("Tunnel access never authorizes a database phase", readme)

    def test_infrastructure_state_contract_enforces_security_boundaries(self) -> None:
        state = (skill_root("ymir") / "references" / "infrastructure-state.md").read_text(encoding="utf-8")
        ymir = (skill_root("ymir") / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("trusted out-of-band", state)
        self.assertIn("explicitly scoped persistence consent", state)
        self.assertIn("Reject malformed, corrupt, or unsupported-schema state", state)
        self.assertIn("stale state may guide discovery but never PLAN approval or APPLY", state)
        self.assertIn("Material drift invalidates the plan and APPLY authority", state)
        self.assertIn("On partial APPLY or VERIFY failure, halt further mutation", state)
        self.assertIn("Persistence never includes secrets", state)
        self.assertIn("Provider-specific skills extend capability but grant no authority", ymir)
        self.assertIn("Dependency or skill installation requires user authorization", ymir)


class WorkflowGovernanceTests(unittest.TestCase):
    def test_technical_refinement_is_proportional_and_policy_aware(self) -> None:
        skill = (VALIDATOR.SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        definition = (VALIDATOR.SKILL_ROOT / "references" / "definition-of-done.md").read_text(encoding="utf-8")
        odin = skill
        ymir = (skill_root("ymir") / "SKILL.md").read_text(encoding="utf-8")
        forseti = (skill_root("forseti") / "SKILL.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("## Refine before material mutation", skill)
        self.assertIn("when it improves the delivery decision", skill)
        self.assertIn("Persist the refinement only when repository policy requires", skill)
        self.assertIn("Technical refinement, when useful or policy-required", definition)
        self.assertIn("repository-designated artifact", definition)
        self.assertIn("Persist the refinement only when repository policy requires", odin)
        self.assertIn("persist it only when repository policy", ymir)
        self.assertNotIn("Technical Refinement record before mutation", forseti)
        self.assertIn("## Technical refinement", readme)

    def test_intent_routing_preserves_authority_and_discovery_boundary(self) -> None:
        skill = (VALIDATOR.SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        for intent in ("DISCOVERY", "DELIVERY", "REVIEW", "INFRASTRUCTURE", "DEPLOY", "MONITOR"):
            self.assertIn(f"**{intent}:**", skill)
        self.assertIn("Ask one focused question only when ambiguity would materially change", skill)
        self.assertIn("Intent and authority are separate dimensions", skill)
        self.assertIn("Never reinterpret an intent keyword as protected-operation authority", skill)
        self.assertIn("DISCOVERY -> user approval -> prepare or create issues when separately authorized -> DELIVERY", skill)
        self.assertIn("It does not create issues, implement changes, or begin delivery", skill)

    def test_discovery_brief_and_role_ownership_are_explicit(self) -> None:
        skill = (VALIDATOR.SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        odin = skill
        mimir = (skill_root("mimir") / "SKILL.md").read_text(encoding="utf-8")
        for field in (
            "problem or desired outcome", "relevant technical evidence", "viable alternatives",
            "proposed scope and exclusions", "affected components", "risks and unknowns",
            "relative complexity", "proposed issues", "preliminary acceptance criteria",
        ):
            self.assertIn(field, skill)
        self.assertIn("For **DISCOVERY**, Odin owns product framing", odin)
        self.assertIn("Do not turn the request into product framing", mimir)
        self.assertIn("do not edit artifacts", mimir.lower())

    def test_deploy_routing_separates_application_and_infrastructure(self) -> None:
        skill = (VALIDATOR.SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        roles = (VALIDATOR.SKILL_ROOT / "references" / "roles-and-skills.md").read_text(encoding="utf-8")
        self.assertIn("coordinate promotion of an approved application revision", skill)
        self.assertIn("route infrastructure changes to Ymir", skill)
        self.assertIn("Application promotion follows the repository's authorized workflow", roles)
        self.assertIn("separately authorized activities", roles)

    def test_readme_documents_intents_without_removed_bragi_section(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("### Bragi: final-candidate code review", readme)
        for example in (
            "Use Asgard para explorar esta ideia.",
            "Use Asgard para desenvolver esta funcionalidade.",
            "Faça o discovery e pare antes de criar as issues.",
            "Faça o discovery e, se eu aprovar, prepare as issues.",
        ):
            self.assertIn(example, readme)
        self.assertIn("Intent never grants authority", readme)
        self.assertIn("Application promotion follows the repository's authorized workflow through Hermod", readme)
        self.assertIn("Complete Odin orchestration requires the Asgard plugin", readme)
        self.assertIn("Direct invocation does not start Odin orchestration", readme)
        self.assertIn("`HANDOFF_REQUIRED`", readme)

    def test_bragi_reviews_only_completed_code_quality_candidate(self) -> None:
        bragi = (skill_root("bragi") / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("after `IMPLEMENTER_COMPLETE`", bragi)
        self.assertIn("SOLID, DRY, KISS, YAGNI, and Tell, Don't Ask", bragi)
        self.assertIn("style taste alone cannot reject", bragi)
        self.assertIn("do not review intermediate files", bragi)

        skill = (VALIDATOR.SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("references/roles-and-skills.md", skill)
        gates = (VALIDATOR.SKILL_ROOT / "references" / "review-and-publication-gates.md").read_text(encoding="utf-8")
        self.assertIn("Every Brokkr completion records `BRAGI_RECOMMENDED`", gates)
        self.assertIn("does not start services or rerun broad validations", gates)

    def test_forseti_applies_repository_traceability_with_limited_metadata_repair(self) -> None:
        text = (skill_root("forseti") / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("repository or user policy", text)
        self.assertIn("policy-required issue, branch, pull-request", text)
        self.assertIn("authorized metadata repair", text)
        self.assertIn("provider-recognized closing reference", text)
        self.assertIn("provider-recognized closing-issue relationship", text)
        self.assertIn("never guess, replace, or add several references", text)
        self.assertIn("never implies technical acceptance", text)
        self.assertIn("Never infer a repository's branch, issue, label", text)

        skill = (VALIDATOR.SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("references/roles-and-skills.md", skill)
        self.assertNotIn("github-label-governance", skill)
        self.assertFalse((VALIDATOR.SKILL_ROOT / "references" / "github-label-governance.md").exists())
        self.assertIn("$asgard:hermod", skill)

    def test_github_operations_are_cli_first_with_guarded_browser_exception(self) -> None:
        skill = (VALIDATOR.SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        forseti = (skill_root("forseti") / "SKILL.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("repository's authorized tooling", skill)
        self.assertIn("send Markdown as real multiline text", skill)
        self.assertIn("literal escape sequences such as `\\n`", skill)
        self.assertIn("body-file/stdin mechanisms", skill)
        self.assertIn("Do not impose GitHub-specific tooling", skill)
        self.assertIn("authenticated `gh` CLI", forseti)
        self.assertIn("preserve Markdown with real line breaks", forseti)
        self.assertIn("does not silently fall back to an unapproved client", readme)

    def test_repository_policy_controls_branch_and_issue_conventions(self) -> None:
        skill = (VALIDATOR.SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        forseti = (skill_root("forseti") / "SKILL.md").read_text(encoding="utf-8")
        definition = (VALIDATOR.SKILL_ROOT / "references" / "definition-of-done.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("discover the repository's issue, branch", skill)
        self.assertIn("Repository-policy artifacts and edit authority", definition)
        self.assertIn("Never infer a repository's branch", forseti)
        self.assertIn("does not define the taxonomy", readme)

    def test_changelog_rules_follow_repository_policy(self) -> None:
        skill = (VALIDATOR.SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        forseti = (skill_root("forseti") / "SKILL.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")

        for text in (skill, forseti, readme):
            self.assertIn("policy", text.lower())
        self.assertIn("versioning, changelog", skill)
        self.assertIn("changelog, versioning", forseti)
        self.assertIn("does not define the taxonomy", readme)
        self.assertIn("issue #131", changelog)

    def test_context_efficiency_is_budgeted_and_non_recursive(self) -> None:
        skill = (VALIDATOR.SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        context = (VALIDATOR.SKILL_ROOT / "references" / "context-efficiency.md").read_text(encoding="utf-8")
        roles = (VALIDATOR.SKILL_ROOT / "references" / "roles-and-skills.md").read_text(encoding="utf-8")
        definition = (VALIDATOR.SKILL_ROOT / "references" / "definition-of-done.md").read_text(encoding="utf-8")
        gates = (VALIDATOR.SKILL_ROOT / "references" / "review-and-publication-gates.md").read_text(encoding="utf-8")
        odin = skill

        self.assertIn("references/context-efficiency.md", skill)
        self.assertIn("Do not mention or invoke `$asgard:asgard` in a delegated skill task", skill)
        self.assertIn("simultaneous_agents: 3", context)
        self.assertIn("correction_cycles: 1", context)
        self.assertIn("monitor_or_status: 50", context)
        self.assertIn("implementer: 150", context)
        self.assertIn("reviewer_with_findings: 250", context)
        self.assertIn("odin_final: 300", context)
        self.assertIn("APPROVED — <primary evidence>", context)
        for status in (
            "IMPLEMENTER_COMPLETE",
            "FINDINGS_COMPLETE",
            "APPROVED",
            "CHANGES_REQUIRED",
            "PENDING",
            "HANDOFF_REQUIRED",
            "BLOCKED",
        ):
            self.assertIn(status, context)
        for field in ("handoff:", "recommended_skill:", "reason:", "evidence:", "prerequisites:", "authority_required:"):
            self.assertIn(field, context)
        self.assertIn("`HANDOFF_REQUIRED` always includes every `handoff` field above", context)
        self.assertIn("incremental_reasoning_output_tokens", context)
        self.assertIn("Do not use `high` by default", context)
        self.assertIn("phase_checkpoint:", context)
        self.assertIn("Aggregate by phase and selected skill only at the final checkpoint", context)
        self.assertIn("Reference exact paths, revisions, and bounded diff commands", roles)
        self.assertIn("Execution budget:", definition)
        self.assertIn("default budget permits one grouped correction cycle", gates)
        self.assertIn("Do not mention or invoke `$asgard:asgard` in a delegated skill task", odin)

    def test_implicit_selection_excludes_ordinary_work(self) -> None:
        skill = (VALIDATOR.SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        header = skill.split("---", 2)[1]
        self.assertIn("multiple bounded activities or material risk", header)
        self.assertIn("ordinary maintenance", header)
        self.assertIn("monitoring", header.lower())

    def test_activation_contract_covers_all_intents_and_explicit_monitoring(self) -> None:
        skill = (VALIDATOR.SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        header = skill.split("---", 2)[1]
        for intent in ("discovery", "delivery", "review", "infrastructure", "deploy", "monitor"):
            self.assertIn(intent, header.lower())
        self.assertIn("Asgard is explicitly requested", header)
        self.assertIn("explicit MONITOR requests", header)
        self.assertIn("Do not select it implicitly", header)

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        when_to_use = readme.split("## When to use Asgard", 1)[1].split("## Role model", 1)[0]
        for intent in ("discovery", "delivery", "review", "infrastructure", "deploy", "monitoring"):
            self.assertIn(intent, when_to_use.lower())
        self.assertIn("Explicit monitoring remains supported", when_to_use)
        self.assertIn("Do not select it implicitly", when_to_use)

    def test_hermod_publishes_normal_and_release_pull_requests(self) -> None:
        hermod_root = ROOT / "plugins" / "asgard" / "skills" / "hermod"
        skill = (hermod_root / "SKILL.md").read_text(encoding="utf-8")
        metadata = (hermod_root / "agents" / "openai.yaml").read_text(encoding="utf-8")
        asgard = (VALIDATOR.SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("name: hermod", skill)
        self.assertIn("**OPEN_PR:**", skill)
        self.assertIn("**RELEASE_PR:**", skill)
        for term in ("authoritative issue", "develop", "release/<version>", "master", "Semantic Version", "CHANGELOG.md", "gh auth status", "gh pr create"):
            self.assertIn(term, skill)
        self.assertIn("display_name: \"Hermod\"", metadata)
        self.assertIn("$asgard:hermod", asgard)
        self.assertNotIn((VALIDATOR.SKILL_ROOT / "references" / "agents" / "hermod.md").as_posix(), asgard)

    def test_eir_validates_pull_request_acceptance_and_corrections(self) -> None:
        eir_root = ROOT / "plugins" / "asgard" / "skills" / "eir"
        skill = (eir_root / "SKILL.md").read_text(encoding="utf-8")
        metadata = (eir_root / "agents" / "openai.yaml").read_text(encoding="utf-8")
        review = (eir_root / "references" / "review.md").read_text(encoding="utf-8")

        self.assertIn("name: eir", skill)
        self.assertIn("**REVIEW:**", skill)
        self.assertNotIn("REVIEW_COMMENTS", skill)
        for term in ("gh auth status", "gh api", "COMMENT", "APPROVE", "does not implement code", "open Pull Requests"):
            self.assertIn(term, skill)
        self.assertIn('display_name: "Eir"', metadata)
        self.assertIn("Create exactly one native Pull Request review", review)
        verification = (eir_root / "references" / "verification.md").read_text(encoding="utf-8")
        self.assertIn("Eir's original findings", verification)
        self.assertIn("only an Eir-created thread", verification)
        self.assertIn("one native `APPROVE` review", verification)

    def test_brokkr_records_non_blocking_bragi_recommendation(self) -> None:
        brokkr = (skill_root("brokkr") / "SKILL.md").read_text(encoding="utf-8")
        gates = (VALIDATOR.SKILL_ROOT / "references" / "review-and-publication-gates.md").read_text(encoding="utf-8")
        self.assertIn("**ISSUE:**", brokkr)
        self.assertIn("**TASK:**", brokkr)
        self.assertIn("**CORRECT:**", brokkr)
        self.assertIn("`BRAGI_RECOMMENDED`", brokkr)
        self.assertIn("never invokes Bragi", brokkr)
        self.assertIn("It is not a gate and does not invoke Bragi automatically", gates)

    def test_release_runs_from_master_push_without_checkout(self) -> None:
        text = (ROOT / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")
        self.assertIn("\n  push:\n    branches: [master]", text)
        self.assertNotIn("pull_request_target:", text)
        self.assertNotIn("actions/checkout", text)
        self.assertIn("MERGE_SHA: ${{ github.sha }}", text)
        self.assertIn('while [[ "$object_type" == "tag" ]]', text)
        self.assertIn('gh release view "$tag"', text)
        self.assertIn("GH_REPO: ${{ github.repository }}", text)

    def test_release_treats_only_exact_404_as_missing_tag(self) -> None:
        text = (ROOT / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")
        self.assertIn('gh api --include --silent "$tag_endpoint"', text)
        self.assertIn('if [[ "$tag_status" != "404" ]]', text)
        self.assertIn('if [[ "$tag_status" == "200" ]]', text)
        self.assertIn('elif [[ "$tag_status" != "404" ]]', text)
        self.assertNotIn("2>/dev/null || true", text)

    def test_release_opens_verified_backport_after_publication(self) -> None:
        text = (ROOT / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")
        backport = text.split("\n  create-backport:", 1)[1]
        self.assertIn("create-backport:", text)
        self.assertIn("needs: release", text)
        self.assertIn("BACKPORT_TOKEN: ${{ secrets.BACKPORT_TOKEN }}", text)
        self.assertIn("contents: read", backport)
        self.assertEqual(text.count("GH_TOKEN: ${{ secrets.BACKPORT_TOKEN }}"), 1)
        self.assertIn("BACKPORT_TOKEN is required to open a PR that triggers CI.", text)
        self.assertIn('git/ref/heads/master" --jq .object.sha', backport)
        self.assertIn("gh api --paginate", backport)
        self.assertIn("state=open&base=develop&head=${owner}%3Amaster", backport)
        self.assertIn("--method POST", backport)
        self.assertIn("-f head='master'", backport)
        self.assertIn("-f base='develop'", backport)
        self.assertNotIn("git switch", backport)
        self.assertNotIn("git push", backport)
        self.assertNotIn("gh pr create", backport)

    def test_external_actions_are_commit_pinned(self) -> None:
        for path in (ROOT / ".github" / "workflows").glob("*.yml"):
            for line in path.read_text(encoding="utf-8").splitlines():
                if "uses:" in line:
                    reference = line.split("@", 1)[1].split()[0]
                    self.assertRegex(reference, r"^[0-9a-f]{40}$", str(path))

    def test_source_gate_handles_edited_events_and_explicit_base(self) -> None:
        text = (ROOT / ".github" / "workflows" / "enforce-release-source.yml").read_text(encoding="utf-8")
        self.assertIn("edited", text)
        self.assertIn("branches: [develop, master]", text)
        self.assertIn("name: develop to master only", text)
        self.assertIn("BASE_REF", text)
        self.assertIn('case "$BASE_REF" in', text)

    def test_source_gate_allows_named_prefixes_and_internal_master_to_develop(self) -> None:
        text = (ROOT / ".github" / "workflows" / "enforce-release-source.yml").read_text(encoding="utf-8")
        self.assertIn("feature/?*|fix/?*|docs/?*|chore/?*|refactor/?*|test/?*|backport/?*", text)
        self.assertIn('master)', text)
        self.assertIn("Only this repository's master branch may backport to develop.", text)
        self.assertIn('if [[ "$HEAD_REPO" != "$REPOSITORY" ]]', text)

    def test_source_gate_restricts_master_to_same_repo_release_or_hotfix(self) -> None:
        text = (ROOT / ".github" / "workflows" / "enforce-release-source.yml").read_text(encoding="utf-8")
        master_policy = text.split("master)", 1)[1]
        self.assertIn('"$HEAD_REPO" != "$REPOSITORY"', master_policy)
        self.assertIn("release/?*|hotfix/?*", master_policy)
        self.assertIn("PRs to master require a release/ or hotfix/ branch.", master_policy)
        self.assertIn("if: github.event.pull_request.base.ref == 'master'", text)

    def test_source_gate_requires_base_manifest_without_fallback(self) -> None:
        text = (ROOT / ".github" / "workflows" / "enforce-release-source.yml").read_text(encoding="utf-8")
        self.assertIn('candidate="$(read_version "$HEAD_SHA")"', text)
        self.assertIn('current="$(read_version "$BASE_SHA")"', text)
        self.assertNotIn('current="0.0.0"', text)
        self.assertNotIn("bootstrap", text.lower())
        self.assertNotIn("matching-refs", text)
        self.assertNotIn("HTTP 404", text)


if __name__ == "__main__":
    unittest.main()
