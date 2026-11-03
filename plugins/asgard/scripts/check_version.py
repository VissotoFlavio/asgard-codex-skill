#!/usr/bin/env python3
"""Best-effort, once-per-day update check shared by all Asgard skills.

Only a successful claim of the persistent cooldown permits an HTTP request.
The claim is committed before networking, so failures and concurrent callers
cannot repeatedly query GitHub. This command always exits successfully.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
import sqlite3
import subprocess
import sys
import time


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
RELEASE_API = "repos/VissotoFlavio/asgard-codex-skill/releases/latest"
RELEASE_PAGE = "https://github.com/VissotoFlavio/asgard-codex-skill/releases"
COOLDOWN_SECONDS = 24 * 60 * 60
RECOVERY_LOCK_SECONDS = 60
RECOVERY_RENAME_ATTEMPTS = 10
RECOVERY_RETRY_SECONDS = 0.02
SEMVER = re.compile(
    r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
)


def parse_version(value: str) -> tuple[tuple[int, int, int], str | None]:
    """Parse SemVer, rejecting numeric prerelease identifiers with leading zeroes."""
    if not isinstance(value, str):
        raise ValueError("version must be a string")
    match = SEMVER.fullmatch(value)
    if match is None:
        raise ValueError("invalid SemVer")
    prerelease = match[4]
    if prerelease and any(
        part.isdigit() and len(part) > 1 and part.startswith("0")
        for part in prerelease.split(".")
    ):
        raise ValueError("invalid numeric prerelease identifier")
    return (int(match[1]), int(match[2]), int(match[3])), prerelease


def state_path() -> Path:
    override = os.environ.get("ASGARD_CONFIG_HOME")
    if override is not None:
        root = Path(override)
        if not override.strip() or not root.is_absolute():
            raise ValueError("ASGARD_CONFIG_HOME must be absolute")
    elif sys.platform == "win32":
        root = Path(os.environ.get("LOCALAPPDATA") or Path.home() / "AppData" / "Local") / "Asgard"
    elif sys.platform == "darwin":
        root = Path.home() / "Library" / "Application Support" / "Asgard"
    else:
        root = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config") / "asgard"
    if not root.is_absolute():
        raise ValueError("state root must be absolute")
    root = root.resolve()
    if root.is_relative_to(PLUGIN_ROOT):
        raise ValueError("state must be outside the installed plugin")
    path = (root / "version-check.sqlite3").resolve()
    if path.is_relative_to(PLUGIN_ROOT):
        raise ValueError("state must be outside the installed plugin")
    return path


def claim_attempt(path: Path, now: float) -> bool:
    """Serialize the read/claim, then release the lock before HTTP begins."""
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    connection = sqlite3.connect(path, timeout=0.25)
    try:
        connection.execute("BEGIN IMMEDIATE")
        connection.execute(
            "CREATE TABLE IF NOT EXISTS attempts (id INTEGER PRIMARY KEY CHECK (id = 1), attempted_at REAL NOT NULL)"
        )
        row = connection.execute("SELECT attempted_at FROM attempts WHERE id = 1").fetchone()
        if row is not None:
            previous = row[0]
            if is_invalid_attempt_timestamp(previous, now):
                raise ValueError("invalid attempt timestamp")
            if now - previous < COOLDOWN_SECONDS:
                return False
        connection.execute("INSERT OR REPLACE INTO attempts VALUES (1, ?)", (now,))
        connection.commit()
        return True
    finally:
        connection.close()


def is_invalid_attempt_timestamp(value: object, now: float) -> bool:
    return not isinstance(value, (int, float)) or not 0 <= value <= now


def is_corrupt_database_error(error: sqlite3.DatabaseError) -> bool:
    message = str(error).lower()
    return any(marker in message for marker in ("not a database", "malformed", "corrupt"))


def state_needs_recovery(path: Path, now: float) -> bool:
    """Confirm corruption while holding the recovery lock before replacing state."""
    if not path.exists():
        return False
    try:
        connection = sqlite3.connect(path, timeout=0.25)
        try:
            integrity = connection.execute("PRAGMA quick_check").fetchone()
            if integrity != ("ok",):
                return True
            try:
                row = connection.execute("SELECT attempted_at FROM attempts WHERE id = 1").fetchone()
            except sqlite3.OperationalError as error:
                if "no such table" in str(error).lower():
                    return False
                raise
            return row is not None and is_invalid_attempt_timestamp(row[0], now)
        finally:
            connection.close()
    except sqlite3.DatabaseError as error:
        return is_corrupt_database_error(error)


def acquire_recovery_lock(path: Path) -> int | None:
    lock = path.with_name(f"{path.name}.recovery.lock")
    for _ in range(2):
        try:
            return os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError:
            try:
                if time.time() - lock.stat().st_mtime < RECOVERY_LOCK_SECONDS:
                    return None
                lock.unlink()
            except OSError:
                return None
    return None


def recover_corrupt_state(path: Path, now: float) -> bool:
    """Quarantine a confirmed bad database once, without racing a valid replacement."""
    lock = path.with_name(f"{path.name}.recovery.lock")
    descriptor = acquire_recovery_lock(path)
    if descriptor is None:
        return False
    try:
        if not state_needs_recovery(path, now):
            return True
        suffix = f".corrupt-{time.time_ns()}-{os.getpid()}"
        for source in (path, Path(f"{path}-wal"), Path(f"{path}-shm")):
            target = source.with_name(f"{source.name}{suffix}")
            for attempt in range(RECOVERY_RENAME_ATTEMPTS):
                try:
                    os.replace(source, target)
                    break
                except FileNotFoundError:
                    break
                except OSError:
                    if attempt == RECOVERY_RENAME_ATTEMPTS - 1:
                        return False
                    time.sleep(RECOVERY_RETRY_SECONDS)
        return True
    finally:
        os.close(descriptor)
        try:
            lock.unlink()
        except FileNotFoundError:
            pass


def resolve_gh() -> str:
    """Resolve PATH explicitly, without Windows' implicit current-directory search."""
    workspace = Path.cwd().resolve()
    name = "gh.exe" if sys.platform == "win32" else "gh"
    for entry in os.environ.get("PATH", "").split(os.pathsep):
        directory = Path(entry.strip('"'))
        if not directory.is_absolute():
            continue
        candidate = (directory / name).resolve()
        if candidate.parent == workspace:
            continue
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return str(candidate)
    raise FileNotFoundError("no trusted gh executable on PATH")


def fetch_release() -> dict:
    # Use the repository's required GitHub client and validate authentication
    # before the API call. Capture diagnostics so the primary task stays quiet.
    executable = resolve_gh()
    subprocess.run(
        [executable, "auth", "status", "--hostname", "github.com"],
        check=True, capture_output=True, timeout=5, cwd=PLUGIN_ROOT,
    )
    response = subprocess.run(
        [executable, "api", "--hostname", "github.com", RELEASE_API, "--jq", "{tag_name, draft, prerelease}"],
        check=True, capture_output=True, timeout=5, encoding="utf-8", cwd=PLUGIN_ROOT,
    )
    return json.loads(response.stdout)


def check_version() -> dict[str, str]:
    """Return only the actionable notice or a compact non-blocking status."""
    try:
        manifest = json.loads((PLUGIN_ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
        installed = manifest["version"]
        current, prerelease = parse_version(installed)
        path = state_path()
        now = time.time()
        try:
            claimed = claim_attempt(path, now)
        except ValueError:
            if not recover_corrupt_state(path, now):
                return {"status": "unavailable"}
            claimed = claim_attempt(path, now)
        except sqlite3.DatabaseError as error:
            if not is_corrupt_database_error(error) or not recover_corrupt_state(path, now):
                return {"status": "unavailable"}
            claimed = claim_attempt(path, now)
        if not claimed:
            return {"status": "cooldown"}
        release = fetch_release()
        if release.get("draft") is not False or release.get("prerelease") is not False:
            raise ValueError("not a stable release")
        tag = release["tag_name"]
        latest = tag.removeprefix("v")
        available, candidate_prerelease = parse_version(latest)
        if candidate_prerelease is not None:
            raise ValueError("not stable SemVer")
        if available > current or (available == current and prerelease is not None):
            return {
                "status": "update_available",
                "installed_version": installed,
                "latest_version": latest,
                "release_url": f"{RELEASE_PAGE}/tag/{tag}",
            }
        return {"status": "current"}
    except Exception:
        # Missing runtime prerequisites, locked/corrupt state, and network errors
        # must never prevent the skill's primary task or print noisy diagnostics.
        return {"status": "unavailable"}


if __name__ == "__main__":
    print(json.dumps(check_version(), separators=(",", ":")))
