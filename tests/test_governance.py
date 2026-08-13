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


class WorkflowGovernanceTests(unittest.TestCase):
    def test_release_has_no_push_trigger_or_checkout(self) -> None:
        text = (ROOT / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")
        self.assertIn("pull_request_target:", text)
        self.assertNotIn("\n  push:", text)
        self.assertNotIn("actions/checkout", text)
        self.assertIn("head.ref == 'develop'", text)
        self.assertIn("base.ref == 'master'", text)
        self.assertIn('while [[ "$object_type" == "tag" ]]', text)
        self.assertIn('gh release view "$tag"', text)

    def test_external_actions_are_commit_pinned(self) -> None:
        for path in (ROOT / ".github" / "workflows").glob("*.yml"):
            for line in path.read_text(encoding="utf-8").splitlines():
                if "uses:" in line:
                    reference = line.split("@", 1)[1].split()[0]
                    self.assertRegex(reference, r"^[0-9a-f]{40}$", str(path))

    def test_source_gate_handles_edited_events_and_explicit_base(self) -> None:
        text = (ROOT / ".github" / "workflows" / "enforce-release-source.yml").read_text(encoding="utf-8")
        self.assertIn("edited", text)
        self.assertIn("BASE_REF", text)
        self.assertIn('"$BASE_REF" != "master"', text)

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
