#!/usr/bin/env python3
"""Check portable configuration and internal links; never calls a model or API."""

from pathlib import Path
import re
import sys
import tomllib


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "templates/project"


def check_bundle():
    errors = []
    config = tomllib.loads((PROJECT / ".codex/config.toml").read_text())
    agents = config["agents"]
    if config["model"] != "gpt-6-astra" or not agents["enabled"]:
        errors.append("Project defaults must enable Astra orchestration.")
    if (agents["default_subagent_model"], agents["default_subagent_reasoning_effort"]) != (
        "gpt-6-luna", "medium"
    ):
        errors.append("Routine defaults must be Luna medium.")
    if not isinstance(agents["max_concurrent_threads_per_session"], int) or agents[
        "max_concurrent_threads_per_session"
    ] < 1:
        errors.append("The child-agent limit must be a positive integer.")

    roles = {"explorer", "worker", "tester", "researcher", "reviewer"}
    files = list((PROJECT / ".codex/agents").glob("*.toml"))
    if {p.stem for p in files} != roles:
        errors.append("The bundle must provide the five documented roles.")
    for path in files:
        role = tomllib.loads(path.read_text())
        for field in ("name", "description", "developer_instructions"):
            if not isinstance(role.get(field), str) or not role[field].strip():
                errors.append(f"{path.name}: missing {field}")
        if role.get("name") != path.stem:
            errors.append(f"{path.name}: role name differs from filename")
        reviewer = path.stem == "reviewer"
        expected = ("gpt-6-astra", "low") if reviewer else ("gpt-6-luna", "medium")
        if (role.get("model"), role.get("model_reasoning_effort")) != expected:
            errors.append(f"{path.name}: unexpected model or effort")
        sandbox = "workspace-write" if path.stem in {"worker", "tester"} else "read-only"
        if role.get("sandbox_mode") != sandbox:
            errors.append(f"{path.name}: unexpected sandbox default")

    skill = PROJECT / ".agents/skills/astra-orchestrator/SKILL.md"
    content = skill.read_text()
    header = re.match(r"\A---\n(.*?)\n---\n", content, re.S)
    if not header or not re.search(r"^name: astra-orchestrator$", header[1], re.M):
        errors.append("Skill name/frontmatter is invalid.")
    if not header or not re.search(r"^description: \S", header[1], re.M):
        errors.append("Skill description is missing.")

    private_patterns = (
        r"(?:" + "/" + r"Users/|/" + r"home/)[^/\s]+/"
        r"|[A-Za-z]:\\Users\\[^\\\s]+\\"
        r"|sk-[A-Za-z0-9_-]{16,}|ghp_[A-Za-z0-9]{16,}"
        r"|github_pat_[A-Za-z0-9_]{16,}|-----BEGIN [A-Z ]*PRIVATE KEY-----"
    )
    for path in ROOT.rglob("*"):
        if {".git", "__pycache__", ".pytest_cache"}.intersection(path.relative_to(ROOT).parts):
            continue
        if path.is_symlink():
            errors.append(f"{path.relative_to(ROOT)}: unexpected symlink in public bundle")
            continue
        if not path.is_file():
            continue
        raw = path.read_bytes()
        if b"\0" in raw:
            continue
        try:
            content = raw.decode("utf-8")
        except UnicodeDecodeError:
            continue
        # JSON and source literals may escape Windows separators twice.
        privacy_text = content.replace("\\\\", "\\")
        if re.search(private_patterns, privacy_text):
            errors.append(f"{path.relative_to(ROOT)}: potential private path or credential")
        if path.suffix != ".md":
            continue
        for target in re.findall(r"\[[^\]]*\]\(([^\s)]+)\)", content):
            if "://" in target or target.startswith("#"):
                continue
            resolved = (path.parent / target.split("#", 1)[0]).resolve()
            if not resolved.is_relative_to(ROOT) or not resolved.exists():
                errors.append(f"{path.relative_to(ROOT)}: broken/outside link {target}")
    return errors


if __name__ == "__main__":
    try:
        problems = check_bundle()
    except (KeyError, OSError, tomllib.TOMLDecodeError) as error:
        problems = [str(error)]
    for problem in problems:
        print(f"FAIL: {problem}")
    if problems:
        sys.exit(1)
    print("PASS: config, five roles, Skill frontmatter and local Markdown links")
    print("PASS: finite privacy-pattern scan of UTF-8 text (not a comprehensive secret audit)")
    print("Static validation only; target-client loading and runtime routing are unverified.")
