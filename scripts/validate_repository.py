#!/usr/bin/env python3
"""Validate public Asgard artifacts without third-party dependencies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins" / "asgard"
MANIFEST = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
SKILL = PLUGIN_ROOT / "skills" / "asgard" / "SKILL.md"

# SemVer 2.0.0: numeric core identifiers cannot have leading zeroes; numeric
# prerelease identifiers cannot either. Empty prerelease/build identifiers fail.
SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*))*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def is_semver(value: Any) -> bool:
    return isinstance(value, str) and SEMVER.fullmatch(value) is not None


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"missing required file: {path.relative_to(ROOT)}") from exc
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid UTF-8 JSON in {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"JSON root must be an object: {path.relative_to(ROOT)}")
    return value


def contained_path(base: Path, value: Any, *, kind: str) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"path must be a non-empty string, got {value!r}")
    if "\\" in value:
        raise ValueError(f"path must use forward slashes: {value}")
    relative = PurePosixPath(value)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"absolute or traversal path is forbidden: {value}")
    resolved_base = base.resolve()
    resolved = base.joinpath(*relative.parts).resolve()
    if not resolved.is_relative_to(resolved_base):
        raise ValueError(f"path escapes its allowed root: {value}")
    if kind == "file" and not resolved.is_file():
        raise ValueError(f"file does not exist: {value}")
    if kind == "directory" and not resolved.is_dir():
        raise ValueError(f"directory does not exist: {value}")
    return resolved


def record_path(errors: list[str], base: Path, value: Any, *, label: str, kind: str) -> None:
    try:
        contained_path(base, value, kind=kind)
    except ValueError as exc:
        errors.append(f"{label}: {exc}")


def validate_local_markdown_links(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    for target in MARKDOWN_LINK.findall(text):
        if "://" in target or target.startswith("#"):
            continue
        relative = target.split("#", 1)[0]
        try:
            contained_path(path.parent, relative, kind="file")
        except ValueError as exc:
            errors.append(f"broken local link {target!r} in {path.relative_to(ROOT)}: {exc}")
    return errors


def validate() -> str:
    errors: list[str] = []
    try:
        manifest = load_json(MANIFEST)
    except ValueError as exc:
        errors.append(str(exc))
        manifest = {}

    version = manifest.get("version")
    if not is_semver(version):
        errors.append("plugin version must comply with Semantic Versioning 2.0.0")
    for field in ("name", "description", "license", "skills"):
        if not isinstance(manifest.get(field), str) or not manifest[field].strip():
            errors.append(f"plugin manifest field {field!r} must be a non-empty string")
    if manifest.get("name") != "asgard":
        errors.append("plugin manifest name must be 'asgard'")

    record_path(errors, PLUGIN_ROOT, manifest.get("skills"), label="skills", kind="directory")
    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        errors.append("plugin interface must be an object")
        interface = {}
    for field in ("composerIcon", "logo"):
        record_path(errors, PLUGIN_ROOT, interface.get(field), label=field, kind="file")
    screenshots = interface.get("screenshots")
    if not isinstance(screenshots, list):
        errors.append("interface screenshots must be an array")
    else:
        for index, value in enumerate(screenshots):
            record_path(errors, PLUGIN_ROOT, value, label=f"screenshots[{index}]", kind="file")

    try:
        marketplace = load_json(MARKETPLACE)
        entries = marketplace.get("plugins")
        if not isinstance(entries, list):
            errors.append("marketplace plugins must be an array")
            entries = []
        asgard = next((item for item in entries if isinstance(item, dict) and item.get("name") == "asgard"), None)
        if asgard is None:
            errors.append("marketplace does not contain the asgard plugin")
        else:
            source = asgard.get("source")
            if not isinstance(source, dict):
                errors.append("marketplace asgard source must be an object")
            else:
                record_path(errors, ROOT, source.get("path"), label="marketplace source", kind="directory")
    except ValueError as exc:
        errors.append(str(exc))

    try:
        skill_text = SKILL.read_text(encoding="utf-8")
        if not skill_text.startswith("---\n"):
            errors.append("SKILL.md must start with YAML frontmatter")
        header = skill_text.split("---", 2)[1]
        if not re.search(r"(?m)^name:\s*asgard\s*$", header):
            errors.append("SKILL.md frontmatter name must be 'asgard'")
        if not re.search(r"(?m)^description:\s*\S", header):
            errors.append("SKILL.md frontmatter must include a description")
        errors.extend(validate_local_markdown_links(SKILL))
    except (FileNotFoundError, UnicodeDecodeError, IndexError) as exc:
        errors.append(f"cannot read skill definition: {exc}")

    if errors:
        raise ValueError("\n".join(f"- {error}" for error in errors))
    assert isinstance(version, str)
    return version


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--print-version", action="store_true")
    args = parser.parse_args()
    try:
        version = validate()
    except ValueError as exc:
        print(f"Repository validation failed:\n{exc}", file=sys.stderr)
        return 1
    print(version if args.print_version else f"Repository validation passed (v{version}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
