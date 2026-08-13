#!/usr/bin/env python3
"""Increment the Asgard plugin version without creating commits or tags."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
import tempfile
from pathlib import Path
from typing import Callable


VALIDATOR_SPEC = importlib.util.spec_from_file_location(
    "asgard_validate_repository", Path(__file__).with_name("validate_repository.py")
)
if VALIDATOR_SPEC is None or VALIDATOR_SPEC.loader is None:
    raise RuntimeError("cannot load repository validator")
VALIDATOR = importlib.util.module_from_spec(VALIDATOR_SPEC)
VALIDATOR_SPEC.loader.exec_module(VALIDATOR)
MANIFEST = VALIDATOR.MANIFEST
validate = VALIDATOR.validate


STABLE_SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


def parse_stable_version(value: str) -> tuple[int, int, int]:
    match = STABLE_SEMVER.fullmatch(value)
    if match is None:
        raise ValueError(f"version must be stable SemVer (major.minor.patch): {value!r}")
    return tuple(int(part) for part in match.groups())


def next_version(current: str, target: str) -> str:
    major, minor, patch = parse_stable_version(current)
    if target == "patch":
        candidate = (major, minor, patch + 1)
    elif target == "minor":
        candidate = (major, minor + 1, 0)
    elif target == "major":
        candidate = (major + 1, 0, 0)
    else:
        candidate = parse_stable_version(target)
        if candidate <= (major, minor, patch):
            raise ValueError(f"new version must be greater than {current}: {target}")
    return ".".join(str(part) for part in candidate)


def replace_manifest_version(text: str, current: str, candidate: str) -> str:
    pattern = re.compile(r'^(\s*"version"\s*:\s*)"' + re.escape(current) + r'"(\s*,?\s*)$', re.MULTILINE)
    updated, count = pattern.subn(rf'\g<1>"{candidate}"\g<2>', text)
    if count != 1:
        raise ValueError(f"expected exactly one version field containing {current!r}, found {count}")
    return updated


def bump_manifest(
    manifest: Path,
    target: str,
    *,
    dry_run: bool = False,
    validator: Callable[[], str] | None = None,
) -> tuple[str, str]:
    original_bytes = manifest.read_bytes()
    try:
        original = original_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"plugin manifest is not valid UTF-8: {exc}") from exc
    try:
        data = json.loads(original)
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid plugin manifest JSON: {exc}") from exc
    if not isinstance(data, dict) or not isinstance(data.get("version"), str):
        raise ValueError("plugin manifest must contain a string version field")

    current = data["version"]
    candidate = next_version(current, target)
    updated = replace_manifest_version(original, current, candidate)
    if dry_run:
        return current, candidate

    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="", dir=manifest.parent, delete=False
        ) as handle:
            handle.write(updated)
            temporary = Path(handle.name)
        temporary.replace(manifest)
        if validator is not None:
            validated = validator()
            if validated != candidate:
                raise ValueError(f"repository validator returned {validated!r}, expected {candidate!r}")
    except Exception:
        manifest.write_bytes(original_bytes)
        raise
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return current, candidate


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", help="patch, minor, major, or an explicit stable SemVer")
    parser.add_argument("--dry-run", action="store_true", help="show the change without editing the manifest")
    args = parser.parse_args()
    try:
        current, candidate = bump_manifest(MANIFEST, args.target, dry_run=args.dry_run, validator=validate)
    except (OSError, ValueError) as exc:
        print(f"Version update failed: {exc}", file=sys.stderr)
        return 1
    suffix = " (dry run)" if args.dry_run else ""
    print(f"Asgard plugin version: {current} -> {candidate}{suffix}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
