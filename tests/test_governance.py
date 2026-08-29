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


class SemVerTests(unittest.TestCase):
    def test_accepts_strict_semver(self) -> None:
        for value in ("0.1.0", "1.2.3-alpha.1", "1.0.0+build.5", "1.0.0-0A"):
            self.assertTrue(VALIDATOR.is_semver(value), value)

    def test_rejects_invalid_semver(self) -> None:
        for value in (None, 1, "01.2.3", "1.02.3", "1.2.03", "1.0.0-01", "1.0.0-alpha..1", "1.0.0+", "1.0"):
            self.assertFalse(VALIDATOR.is_semver(value), value)


class ContainedPathTests(unittest.TestCase):
    def test_rejects_invalid_types_and_escape(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for value in (None, 7, "", "../outside", "/absolute", "folder\\file"):
                with self.assertRaises(ValueError, msg=repr(value)):
                    VALIDATOR.contained_path(root, value, kind="file")

    def test_accepts_existing_contained_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            child = root / "assets" / "logo.png"
            child.parent.mkdir()
            child.write_bytes(b"png")
            self.assertEqual(VALIDATOR.contained_path(root, "assets/logo.png", kind="file"), child.resolve())

    def test_rejects_symlink_escape_when_supported(self) -> None:
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as outside:
            root = Path(directory)
            link = root / "escape"
            try:
                link.symlink_to(Path(outside), target_is_directory=True)
            except OSError:
                self.skipTest("symlink creation is unavailable")
            with self.assertRaises(ValueError):
                VALIDATOR.contained_path(root, "escape/file", kind="file")

    def test_skill_local_markdown_links_resolve(self) -> None:
        for markdown in VALIDATOR.SKILL_ROOT.rglob("*.md"):
            self.assertEqual(VALIDATOR.validate_local_markdown_links(markdown), [], str(markdown))

    def test_specialist_packets_are_independently_loadable(self) -> None:
        agents = VALIDATOR.SKILL_ROOT / "references" / "agents"
        expected = {"odin", "brokkr", "sindri", "ymir", "mimir", "tyr", "loki", "heimdall", "hermod"}
        self.assertEqual({path.stem for path in agents.glob("*.md")}, expected)
        for role in expected:
            packet = (agents / f"{role}.md").read_text(encoding="utf-8")
            self.assertLess(len(packet), 2_500, role)

    def test_discipline_packets_are_independently_loadable(self) -> None:
        disciplines = VALIDATOR.SKILL_ROOT / "references" / "disciplines"
        expected = {"backend", "frontend", "infrastructure"}
        self.assertEqual({path.stem for path in disciplines.glob("*.md")}, expected)
        for discipline in expected:
            packet = (disciplines / f"{discipline}.md").read_text(encoding="utf-8")
            self.assertLess(len(packet), 2_500, discipline)
        backend = (disciplines / "backend.md").read_text(encoding="utf-8")
        self.assertIn("$dotnet-best-practices", backend)
        frontend = (disciplines / "frontend.md").read_text(encoding="utf-8")
        self.assertIn("$frontend-design", frontend)
        self.assertIn("$web-design-guidelines", frontend)
        infrastructure = (disciplines / "infrastructure.md").read_text(encoding="utf-8")
        self.assertIn("DISCOVER -> PLAN -> APPLY -> VERIFY", infrastructure)
        self.assertIn("infrastructure-state.md", infrastructure)
        self.assertIn("Material drift invalidates the plan and authority", infrastructure)
        self.assertIn("absent, unverifiable, or mismatched identity fails closed", infrastructure)
        self.assertIn("rollback and retries require exact authority", infrastructure)

        definition = (VALIDATOR.SKILL_ROOT / "references" / "definition-of-done.md").read_text(encoding="utf-8")
        self.assertIn("Implementer: Brokkr | Sindri | Ymir", definition)

    def test_infrastructure_state_contract_enforces_security_boundaries(self) -> None:
        state = (VALIDATOR.SKILL_ROOT / "references" / "infrastructure-state.md").read_text(encoding="utf-8")
        ymir = (VALIDATOR.SKILL_ROOT / "references" / "agents" / "ymir.md").read_text(encoding="utf-8")
        self.assertIn("trusted out-of-band", state)
        self.assertIn("explicitly scoped persistence consent", state)
        self.assertIn("Reject malformed, corrupt, or unsupported-schema state", state)
        self.assertIn("stale state may guide discovery but never PLAN approval or APPLY", state)
        self.assertIn("Material drift invalidates the plan and APPLY authority", state)
        self.assertIn("On partial APPLY or VERIFY failure, halt further mutation", state)
        self.assertIn("Persistence never includes secrets", state)
        self.assertIn("Provider-specific skills extend capability but grant no authority", ymir)
        self.assertIn("dependency or skill installation requires user authorization", ymir)


class WorkflowGovernanceTests(unittest.TestCase):
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
