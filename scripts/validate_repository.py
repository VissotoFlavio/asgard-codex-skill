#!/usr/bin/env python3
"""Validate public Asgard artifacts without third-party dependencies."""

from __future__ import annotations

import argparse
import json
import re
import stat
import sys
from pathlib import Path, PurePosixPath
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins" / "asgard"
MANIFEST = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
SKILLS_ROOT = PLUGIN_ROOT / "skills"
SKILL = SKILLS_ROOT / "asgard" / "SKILL.md"
SKILL_ROOT = SKILL.parent

EXPECTED_SKILLS = frozenset(
    {
        "asgard",
        "bragi",
        "brokkr",
        "eir",
        "forseti",
        "heimdall",
        "hermod",
        "kvasir",
        "loki",
        "mimir",
        "regin",
        "sindri",
        "tyr",
        "ymir",
    }
)

# SemVer 2.0.0: numeric core identifiers cannot have leading zeroes; numeric
# prerelease identifiers cannot either. Empty prerelease/build identifiers fail.
SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*))*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
SAFE_PLAIN_YAML_STRING = re.compile(r"^[A-Za-z][A-Za-z0-9 $'(),.;!?/+-]*$")
YAML_NUMBER = re.compile(
    r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?"
    r"|0[xX][0-9A-Fa-f_]+|0[oO][0-7_]+|0[bB][01_]+"
)


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


def is_link_or_reparse_point(path: Path) -> bool:
    try:
        attributes = path.lstat().st_file_attributes
    except (AttributeError, FileNotFoundError, OSError):
        attributes = 0
    return path.is_symlink() or bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0))


def published_path(path: Path, skills_root: Path, *, kind: str) -> Path:
    try:
        relative = path.relative_to(skills_root)
    except ValueError as exc:
        raise ValueError(f"path is outside the published skills root: {path}") from exc
    ancestor = skills_root
    if is_link_or_reparse_point(ancestor):
        raise ValueError(f"symbolic links and reparse points are forbidden: {ancestor}")
    for part in relative.parts:
        ancestor /= part
        if is_link_or_reparse_point(ancestor):
            raise ValueError(f"symbolic links and reparse points are forbidden: {ancestor}")
    resolved_root = skills_root.resolve()
    resolved = path.resolve()
    if not resolved.is_relative_to(resolved_root):
        raise ValueError(f"path escapes the published skills root: {path}")
    if kind == "file" and not resolved.is_file():
        raise ValueError(f"file does not exist: {path}")
    if kind == "directory" and not resolved.is_dir():
        raise ValueError(f"directory does not exist: {path}")
    return resolved


def record_path(errors: list[str], base: Path, value: Any, *, label: str, kind: str) -> None:
    try:
        contained_path(base, value, kind=kind)
    except ValueError as exc:
        errors.append(f"{label}: {exc}")


def validate_local_markdown_links(path: Path, *, skills_root: Path | None = None) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    for target in MARKDOWN_LINK.findall(text):
        if "://" in target or target.startswith("#"):
            continue
        relative = target.split("#", 1)[0]
        try:
            target_path = contained_path(path.parent, relative, kind="file")
            if skills_root is not None:
                published_path(target_path, skills_root, kind="file")
        except ValueError as exc:
            errors.append(f"broken local link {target!r} in {path.relative_to(ROOT)}: {exc}")
    return errors


def resolve_published_skills_root(
    value: Any,
    *,
    plugin_root: Path = PLUGIN_ROOT,
    canonical_skills_root: Path = SKILLS_ROOT,
) -> Path:
    published_root = contained_path(plugin_root, value, kind="directory")
    canonical_root = canonical_skills_root.resolve()
    if published_root != canonical_root:
        raise ValueError("plugin manifest skills must resolve to plugins/asgard/skills")
    if is_link_or_reparse_point(canonical_skills_root):
        raise ValueError("published skills root must not be a symbolic link or reparse point")
    return canonical_root


def discover_distributed_skills(skills_root: Path = SKILLS_ROOT) -> dict[str, Path]:
    if not skills_root.is_dir():
        raise ValueError(f"missing skills directory: {skills_root.relative_to(ROOT)}")
    if is_link_or_reparse_point(skills_root):
        raise ValueError("published skills root must not be a symbolic link or reparse point")

    discovered: dict[str, Path] = {}
    for path in skills_root.iterdir():
        if not path.is_dir():
            continue
        discovered[path.name] = published_path(path, skills_root, kind="directory")
    return discovered


def markdown_files(skill_root: Path, skills_root: Path) -> list[Path]:
    files: list[Path] = []
    directories = [skill_root]
    while directories:
        directory = directories.pop()
        published_path(directory, skills_root, kind="directory")
        for path in directory.iterdir():
            if is_link_or_reparse_point(path):
                raise ValueError(f"symbolic links and reparse points are forbidden: {path}")
            if path.is_dir():
                directories.append(path)
            elif path.is_file() and path.suffix == ".md":
                files.append(published_path(path, skills_root, kind="file"))
    return files


def parse_yaml_scalar(value: str, *, location: str) -> Any:
    """Parse the small YAML scalar subset used by shipped skill metadata.

    Unquoted strings deliberately use a conservative ASCII subset with no YAML
    comment or mapping syntax. JSON-style double quotes are the only supported
    quoted form; rejecting YAML single quotes avoids a partial escape grammar.
    This keeps fields required to be strings from being interpreted as another
    YAML type.
    """
    if not value or value.startswith(("[", "{", "|", ">", "&", "*", "!", "@")):
        raise ValueError(f"{location} must be a scalar value")
    if value.startswith('"'):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{location} has an invalid quoted string") from exc
        if not isinstance(parsed, str):
            raise ValueError(f"{location} must be a string")
        return parsed
    if value.startswith("'"):
        raise ValueError(f"{location} must use JSON-style double quotes, not YAML single quotes")

    scalar = value.rstrip()
    if not scalar or scalar.startswith("#") or ":" in scalar or " #" in scalar:
        raise ValueError(f"{location} must use a quoted string for YAML syntax or comments")
    normalized = scalar.casefold()
    if normalized in {"null", "~"}:
        return None
    if normalized in {"true", "false", "yes", "no", "on", "off"}:
        return normalized in {"true", "yes", "on"}
    if normalized in {".inf", "+.inf", "-.inf", ".nan"}:
        return float(scalar)
    if YAML_NUMBER.fullmatch(scalar):
        return float(scalar) if any(marker in scalar.casefold() for marker in (".", "e")) else int(scalar, 0)
    if not SAFE_PLAIN_YAML_STRING.fullmatch(scalar):
        raise ValueError(f"{location} must use a quoted string outside the safe YAML scalar subset")
    return scalar


def parse_yaml_mapping(text: str, *, location: str) -> dict[str, Any]:
    root: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(-2, root)]
    for line_number, line in enumerate(text.splitlines(), start=1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if "\t" in line:
            raise ValueError(f"{location}:{line_number} must use spaces for indentation")
        indent = len(line) - len(line.lstrip(" "))
        if indent % 2:
            raise ValueError(f"{location}:{line_number} has invalid indentation")
        content = line[indent:]
        match = re.fullmatch(r"([A-Za-z][A-Za-z0-9_-]*):(?: +(.*))?", content)
        if match is None:
            raise ValueError(f"{location}:{line_number} must be a mapping entry")
        while indent <= stack[-1][0]:
            stack.pop()
        if indent != stack[-1][0] + 2:
            raise ValueError(f"{location}:{line_number} has invalid nesting")
        mapping = stack[-1][1]
        key, raw_value = match.groups()
        if key in mapping:
            raise ValueError(f"{location}:{line_number} duplicates {key!r}")
        if raw_value is None:
            nested: dict[str, Any] = {}
            mapping[key] = nested
            stack.append((indent, nested))
        else:
            mapping[key] = parse_yaml_scalar(raw_value, location=f"{location}:{line_number}")
    return root


def parse_skill_frontmatter(text: str, *, name: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError(f"{name} SKILL.md must start with YAML frontmatter")
    try:
        closing = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError(f"{name} SKILL.md must close YAML frontmatter") from exc
    header = parse_yaml_mapping("\n".join(lines[1:closing]), location=f"{name} SKILL.md frontmatter")
    frontmatter_name = header.get("name")
    description = header.get("description")
    if not isinstance(frontmatter_name, str) or frontmatter_name != name:
        raise ValueError(f"{name} SKILL.md frontmatter name must be {name!r}")
    if not isinstance(description, str) or not description.strip():
        raise ValueError(f"{name} SKILL.md frontmatter must include a description")
    return {"name": frontmatter_name, "description": description}


def parse_agent_interface(text: str, *, name: str) -> dict[str, str]:
    metadata = parse_yaml_mapping(text, location=f"{name} agents/openai.yaml")
    interface = metadata.get("interface")
    if not isinstance(interface, dict):
        raise ValueError(f"{name} agents/openai.yaml must include an interface mapping")
    required = ("display_name", "short_description", "default_prompt")
    result: dict[str, str] = {}
    for field in required:
        value = interface.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} agents/openai.yaml interface {field} must be a non-empty string")
        result[field] = value
    return result


def validate_distributed_skill(name: str, skill_root: Path, *, skills_root: Path = SKILLS_ROOT) -> list[str]:
    errors: list[str] = []

    try:
        skill_root = published_path(skill_root, skills_root, kind="directory")
        definition = published_path(skill_root / "SKILL.md", skills_root, kind="file")
        skill_text = definition.read_text(encoding="utf-8")
        parse_skill_frontmatter(skill_text, name=name)
        for markdown in markdown_files(skill_root, skills_root):
            errors.extend(validate_local_markdown_links(markdown, skills_root=skills_root))
    except (FileNotFoundError, UnicodeDecodeError, OSError, ValueError) as exc:
        errors.append(f"cannot validate {name} skill definition: {exc}")

    try:
        metadata = published_path(skill_root / "agents" / "openai.yaml", skills_root, kind="file")
        metadata_text = metadata.read_text(encoding="utf-8")
        parse_agent_interface(metadata_text, name=name)
    except (FileNotFoundError, UnicodeDecodeError, OSError, ValueError) as exc:
        errors.append(f"cannot validate {name} agent metadata: {exc}")

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

    try:
        published_skills_root = resolve_published_skills_root(manifest.get("skills"))
    except ValueError as exc:
        errors.append(f"skills: {exc}")
        published_skills_root = SKILLS_ROOT.resolve()
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
        distributed_skills = discover_distributed_skills(published_skills_root)
        discovered_names = frozenset(distributed_skills)
        missing_skills = EXPECTED_SKILLS - discovered_names
        if missing_skills:
            errors.append(f"missing expected distributed skills: {', '.join(sorted(missing_skills))}")
        for name, skill_root in sorted(distributed_skills.items()):
            errors.extend(validate_distributed_skill(name, skill_root, skills_root=published_skills_root))
    except ValueError as exc:
        errors.append(str(exc))

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
