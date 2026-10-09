#!/usr/bin/env python3
"""Validate this skill's structure, catalog and public-distribution hygiene."""
import json
from pathlib import Path
import re
import sys
from quillume import GROUPS, load_catalog

ROOT = Path(__file__).resolve().parent.parent


def validate(root=ROOT):
    errors = []
    entry = root / "SKILL.md"
    if not entry.is_file():
        return ["Missing SKILL.md"]
    skill = entry.read_text(encoding="utf-8")
    parts = skill.split("---", 2)
    if len(parts) != 3 or parts[0].strip():
        errors.append("SKILL.md requires frontmatter")
    else:
        fields = dict(re.findall(r"^([a-z][a-z-]*):\s*(.+)$", parts[1], re.MULTILINE))
        name = fields.get("name", "")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64 or name != root.name:
            errors.append("Skill name must match its directory and use lowercase kebab-case")
        if not 1 <= len(fields.get("description", "")) <= 1024:
            errors.append("Skill description missing or too long")
        if fields.get("license") != "MIT":
            errors.append("Expected the project's MIT license declaration")
    if len(skill.splitlines()) > 500:
        errors.append("Move long guidance to references")
    for required in ["LICENSE", "README.md", "agents/openai.yaml", "references/catalog.json", "scripts/quillume.py"]:
        if not (root / required).is_file():
            errors.append("Missing " + required)
    secrets = re.compile(r"(?<![A-Za-z0-9_])(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[A-Z0-9]{16}|GOCSPX-[A-Za-z0-9_-]{12,}|sk-[A-Za-z0-9_-]{20,}|creem_[A-Za-z0-9]{12,}|re_[A-Za-z0-9_]{25,})|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")
    forbidden_dirs = {".deploy", ".secrets", ".ssh", ".venv", "node_modules", ".next", "backups", ".cache", ".pytest_cache", "logs"}
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if set(relative.parts) & {".git", ".omx", "__pycache__"}:
            continue
        if path.is_symlink():
            errors.append("Do not ship symlinks: " + str(relative)); continue
        if set(relative.parts) & forbidden_dirs:
            errors.append("Private/runtime artifact: " + str(relative)); continue
        if not path.is_file():
            continue
        if path.name.startswith((".env", "config.local.", "notes.local.", "output.local.")) or path.suffix in {".key", ".pem", ".p12", ".pfx", ".db", ".sqlite", ".sqlite3", ".log", ".bak"}:
            errors.append("Credential or database file: " + str(relative)); continue
        if path.stat().st_size > 2_000_000:
            errors.append("Unexpectedly large file: " + str(relative)); continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeError:
            errors.append("Unexpected binary file: " + str(relative)); continue
        if secrets.search(content):
            errors.append("Credential-shaped content: " + str(relative))
        if re.search(r"\[TO" + r"DO|TO" + r"DO:|/(?:Users|home)/[^/]+/|/srv/[A-Za-z0-9_-]+/", content):
            errors.append("Scaffold or private environment reference: " + str(relative))
        if path.suffix == ".md":
            for target in re.findall(r"\]\(([^)]+)\)", content):
                if "://" in target or target.startswith(("#", "mailto:")):
                    continue
                linked = (path.parent / target.split("#", 1)[0]).resolve()
                if not linked.is_relative_to(root.resolve()) or not linked.exists():
                    errors.append(f"Broken or external local link in {relative}: {target}")
    try:
        catalog = load_catalog(root / "references/catalog.json")
        for group in GROUPS.values():
            for row in catalog[group]:
                for url in row.get("sourceRefs", []):
                    if not isinstance(url, str) or not url.startswith("https://"):
                        errors.append("Invalid source reference in " + row["id"])
    except (ValueError, OSError, KeyError) as error:
        errors.append("Invalid catalog: " + str(error))
    return errors


if __name__ == "__main__":
    problems = validate()
    if problems:
        for problem in problems:
            print(problem, file=sys.stderr)
        raise SystemExit(1)
    catalog = load_catalog()
    print(json.dumps({"status": "passed", "presets": {kind: len(catalog[group]) for kind, group in GROUPS.items()},
                      "coreCombinations": len(catalog["angles"]) * len(catalog["creators"]) * len(catalog["readers"])}, indent=2))
