from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import importlib.util
import json
import os
import subprocess
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("check_version", ROOT / "plugins/asgard/scripts/check_version.py")
assert SPEC and SPEC.loader
CHECK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK)


class VersionCheckTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.state = self.root / "state" / "version-check.sqlite3"
        self.plugin = self.root / "plugin"
        (self.plugin / ".codex-plugin").mkdir(parents=True)
        self.manifest("1.2.3")
        for patcher in (
            patch.object(CHECK, "PLUGIN_ROOT", self.plugin),
            patch.object(CHECK, "state_path", return_value=self.state),
            patch.object(CHECK.time, "time", return_value=1000000),
        ):
            patcher.start()
            self.addCleanup(patcher.stop)

    def manifest(self, version: str) -> None:
        (self.plugin / ".codex-plugin/plugin.json").write_text(json.dumps({"version": version}), encoding="utf-8")

    def release(self, tag: str = "v1.3.0", **fields) -> dict:
        return {"tag_name": tag, "draft": False, "prerelease": False, **fields}

    def test_semver_and_manifest_are_authoritative(self) -> None:
        for installed, tag, expected in (
            ("1.9.0", "v1.10.0", "update_available"),
            ("2.0.0", "v1.10.0", "current"),
            ("1.3.0-beta.1", "v1.3.0", "update_available"),
            ("1.3.0+local", "1.3.0+release", "current"),
        ):
            with self.subTest(installed=installed), patch.object(CHECK, "claim_attempt", return_value=True), patch.object(
                CHECK, "fetch_release", return_value=self.release(tag)
            ):
                self.manifest(installed)
                result = CHECK.check_version()
                self.assertEqual(result["status"], expected)
                if expected == "update_available":
                    self.assertEqual(result["installed_version"], installed)
                    self.assertEqual(set(result), {"status", "installed_version", "latest_version", "release_url"})
        for invalid in ("01.2.3", "1.2", "1.2.3-beta.01", "v1.2.3", "1.2.3\n"):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                CHECK.parse_version(invalid)

    def test_attempt_cooldown_and_exact_24_hour_boundary(self) -> None:
        with patch.object(CHECK, "fetch_release", return_value=self.release()) as fetch:
            self.assertEqual(CHECK.check_version()["status"], "update_available")
            self.assertEqual(CHECK.check_version(), {"status": "cooldown"})
            with patch.object(CHECK.time, "time", return_value=1000000 + 86399):
                self.assertEqual(CHECK.check_version(), {"status": "cooldown"})
            with patch.object(CHECK.time, "time", return_value=1000000 + 86400):
                self.assertEqual(CHECK.check_version()["status"], "update_available")
            self.assertEqual(fetch.call_count, 2)

    def test_network_failure_is_throttled(self) -> None:
        with patch.object(CHECK, "fetch_release", side_effect=OSError("offline")) as fetch:
            self.assertEqual(CHECK.check_version(), {"status": "unavailable"})
            self.assertEqual(CHECK.check_version(), {"status": "cooldown"})
            fetch.assert_called_once()

    def test_corrupt_or_unwritable_state_fails_open_without_network(self) -> None:
        self.state.parent.mkdir()
        self.state.write_bytes(b"not a sqlite database")
        with patch.object(CHECK, "fetch_release") as fetch:
            self.assertEqual(CHECK.check_version(), {"status": "unavailable"})
            fetch.assert_not_called()
        with patch.object(CHECK, "claim_attempt", side_effect=PermissionError), patch.object(CHECK, "fetch_release") as fetch:
            self.assertEqual(CHECK.check_version(), {"status": "unavailable"})
            fetch.assert_not_called()

    def test_concurrent_callers_make_one_network_attempt(self) -> None:
        with patch.object(CHECK, "fetch_release", return_value=self.release()) as fetch:
            with ThreadPoolExecutor(max_workers=8) as pool:
                results = list(pool.map(lambda _: CHECK.check_version(), range(16)))
            fetch.assert_called_once()
            self.assertEqual(sum(result["status"] == "update_available" for result in results), 1)
            self.assertTrue(all(result["status"] in {"update_available", "cooldown", "unavailable"} for result in results))

    def test_rejects_non_stable_or_invalid_release(self) -> None:
        for release in (self.release(prerelease=True), self.release(draft=True), self.release("v1.3.0-beta"), {}, self.release("latest")):
            with self.subTest(release=release), patch.object(CHECK, "claim_attempt", return_value=True), patch.object(
                CHECK, "fetch_release", return_value=release
            ):
                self.assertEqual(CHECK.check_version(), {"status": "unavailable"})


class StatePathTests(unittest.TestCase):
    def test_override_persists_across_plugin_versions(self) -> None:
        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, {"ASGARD_CONFIG_HOME": directory}):
            self.assertEqual(CHECK.state_path(), Path(directory).resolve() / "version-check.sqlite3")

    def test_rejects_relative_empty_and_plugin_local_override(self) -> None:
        for override in ("", "relative/path", str(CHECK.PLUGIN_ROOT / "state")):
            with self.subTest(override=override), patch.dict(os.environ, {"ASGARD_CONFIG_HOME": override}), self.assertRaises(ValueError):
                CHECK.state_path()


class ReleaseClientTests(unittest.TestCase):
    def test_checks_authentication_then_queries_official_latest_release(self) -> None:
        response = subprocess.CompletedProcess([], 0, '{"tag_name":"v1.2.3","draft":false,"prerelease":false}')
        executable = str(Path(tempfile.gettempdir()).resolve() / "trusted-gh.exe")
        with patch.object(CHECK, "resolve_gh", return_value=executable), patch.object(CHECK.subprocess, "run", return_value=response) as run:
            self.assertEqual(CHECK.fetch_release()["tag_name"], "v1.2.3")
            self.assertEqual(run.call_args_list[0].args[0], [executable, "auth", "status", "--hostname", "github.com"])
            self.assertEqual(run.call_args_list[1].args[0], [
                executable, "api", "--hostname", "github.com", "repos/VissotoFlavio/asgard-codex-skill/releases/latest", "--jq", "{tag_name, draft, prerelease}"
            ])
            for call in run.call_args_list:
                self.assertEqual(call.kwargs["timeout"], 5)
                self.assertTrue(call.kwargs["capture_output"])
                self.assertEqual(call.kwargs["cwd"], CHECK.PLUGIN_ROOT)

    def test_authentication_failure_prevents_api_request(self) -> None:
        with patch.object(CHECK, "resolve_gh", return_value=str(ROOT / "trusted-gh.exe")), patch.object(
            CHECK.subprocess, "run", side_effect=subprocess.CalledProcessError(1, "gh")
        ) as run:
            with self.assertRaises(subprocess.CalledProcessError):
                CHECK.fetch_release()
            run.assert_called_once()

    def test_fake_gh_in_cwd_and_relative_path_are_never_selected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory).resolve()
            (workspace / "gh.exe").write_bytes(b"fake executable")
            with patch.object(CHECK.sys, "platform", "win32"), patch.object(
                CHECK.Path, "cwd", return_value=workspace
            ), patch.dict(os.environ, {"PATH": os.pathsep.join(("", ".", "relative/bin", str(workspace)))}), patch.object(
                CHECK.subprocess, "run"
            ) as run:
                with self.assertRaises(FileNotFoundError):
                    CHECK.fetch_release()
                run.assert_not_called()

    def test_absolute_path_installation_is_selected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            executable = Path(directory).resolve() / "gh.exe"
            executable.write_bytes(b"test executable")
            with patch.object(CHECK.sys, "platform", "win32"), patch.dict(
                os.environ, {"PATH": str(executable.parent)}
            ), patch.object(CHECK.os, "access", return_value=True):
                self.assertEqual(CHECK.resolve_gh(), str(executable))


if __name__ == "__main__":
    unittest.main()
