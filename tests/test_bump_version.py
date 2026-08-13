from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("bump_version", ROOT / "scripts" / "bump_version.py")
assert SPEC and SPEC.loader
BUMP = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUMP)


class VersionCalculationTests(unittest.TestCase):
    def test_increments_patch_minor_and_major(self) -> None:
        self.assertEqual(BUMP.next_version("1.2.3", "patch"), "1.2.4")
        self.assertEqual(BUMP.next_version("1.2.3", "minor"), "1.3.0")
        self.assertEqual(BUMP.next_version("1.2.3", "major"), "2.0.0")

    def test_accepts_only_greater_stable_explicit_version(self) -> None:
        self.assertEqual(BUMP.next_version("1.2.3", "2.0.0"), "2.0.0")
        for target in ("1.2.3", "1.2.2", "1.3.0-beta.1", "01.3.0", "latest"):
            with self.assertRaises(ValueError, msg=target):
                BUMP.next_version("1.2.3", target)


class ManifestUpdateTests(unittest.TestCase):
    def make_manifest(self, directory: str, version: str = "1.2.3") -> Path:
        path = Path(directory) / "plugin.json"
        path.write_text('{\n  "name": "asgard",\n  "version": "' + version + '"\n}\n', encoding="utf-8")
        return path

    def test_updates_only_the_version_field(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manifest = self.make_manifest(directory)
            before = manifest.read_text(encoding="utf-8")
            current, candidate = BUMP.bump_manifest(manifest, "minor")
            self.assertEqual((current, candidate), ("1.2.3", "1.3.0"))
            self.assertEqual(manifest.read_text(encoding="utf-8"), before.replace("1.2.3", "1.3.0"))

    def test_dry_run_does_not_edit_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manifest = self.make_manifest(directory)
            before = manifest.read_bytes()
            self.assertEqual(BUMP.bump_manifest(manifest, "patch", dry_run=True), ("1.2.3", "1.2.4"))
            self.assertEqual(manifest.read_bytes(), before)

    def test_restores_manifest_when_validation_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manifest = self.make_manifest(directory)
            before = manifest.read_bytes()

            def reject() -> str:
                raise ValueError("invalid repository")

            with self.assertRaisesRegex(ValueError, "invalid repository"):
                BUMP.bump_manifest(manifest, "patch", validator=reject)
            self.assertEqual(manifest.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
