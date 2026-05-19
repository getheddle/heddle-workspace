"""Install thin discovery adapters for coding agents.

The canonical Heddle agent material lives in this repository:

- ``skills/<name>/SKILL.md`` for progressive-disclosure workflows.
- ``agents/<name>.md`` for subagent definitions.

Agent-specific directories should be symlink adapters back to those
canonical files, not copies.
"""

from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class LinkResult:
    action: str
    path: Path
    detail: str


def toolkit_root() -> Path:
    return Path(__file__).resolve().parents[2]


def default_codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME", "~/.codex")).expanduser()


def install(
    workspace_root: Path,
    *,
    install_agents_standard: bool = True,
    install_aider: bool = True,
    install_cline: bool = True,
    install_claude: bool = True,
    install_codex: bool = True,
    install_copilot: bool = True,
    install_cursor: bool = True,
    install_devin: bool = True,
    install_gemini: bool = True,
    install_qwen: bool = True,
    install_windsurf: bool = True,
    install_zed: bool = True,
    codex_home: Path | None = None,
) -> list[LinkResult]:
    """Install adapter symlinks for the requested agents."""
    root = workspace_root.resolve()
    if not root.is_dir():
        raise FileNotFoundError(f"workspace root not found: {root}")
    src_root = toolkit_root()
    results: list[LinkResult] = []

    if install_agents_standard:
        results.extend(_install_agents_standard(root, src_root))
    if install_aider:
        results.extend(_install_aider(root))
    if install_cline:
        results.extend(_install_cline(root, src_root))
    if install_claude:
        results.extend(_install_claude(root, src_root))
    if install_codex:
        results.extend(_install_codex(codex_home or default_codex_home(), src_root))
    if install_copilot:
        results.extend(_install_copilot(root))
    if install_cursor:
        results.extend(_install_cursor(root))
    if install_devin:
        results.extend(_install_devin(root, src_root))
    if install_gemini:
        results.extend(_install_gemini(root))
    if install_qwen:
        results.extend(_install_qwen(root, src_root))
    if install_windsurf:
        results.extend(_install_windsurf(root, src_root))
    if install_zed:
        results.extend(_install_zed(root))
    return results


def _install_agents_standard(workspace_root: Path, src_root: Path) -> list[LinkResult]:
    results: list[LinkResult] = []
    for skill in _skills(src_root):
        results.append(_link(skill, workspace_root / ".agents" / "skills" / skill.name))
    return results


def _install_aider(workspace_root: Path) -> list[LinkResult]:
    return [
        _write_if_missing(
            workspace_root / ".aider.conf.yml",
            "# Heddle agent adapter for aider.\n"
            "# Keep canonical instructions in AGENTS.md; aider loads this as\n"
            "# read-only context when it starts.\n"
            "read:\n"
            "  - AGENTS.md\n",
        )
    ]


def _install_cline(workspace_root: Path, src_root: Path) -> list[LinkResult]:
    results: list[LinkResult] = []
    for skill in _skills(src_root):
        results.append(_link(skill, workspace_root / ".cline" / "skills" / skill.name))
    for agent in _agents(src_root):
        results.append(_link(agent, workspace_root / ".cline" / "agents" / agent.name))
    results.append(
        _write_if_missing(
            workspace_root / ".cline" / "rules" / "heddle-workspace.md",
            _plain_rule_content("Cline"),
        )
    )
    return results


def _install_claude(workspace_root: Path, src_root: Path) -> list[LinkResult]:
    results: list[LinkResult] = []
    skills_dst = workspace_root / ".claude" / "skills"
    agents_dst = workspace_root / ".claude" / "agents"

    for skill in _skills(src_root):
        results.append(_link(skill, skills_dst / skill.name))
    for agent in _agents(src_root):
        results.append(_link(agent, agents_dst / agent.name))
    return results


def _install_codex(codex_home: Path, src_root: Path) -> list[LinkResult]:
    results: list[LinkResult] = []
    skills_dst = codex_home.expanduser() / "skills" / "heddle"

    for skill in _skills(src_root):
        results.append(_link(skill, skills_dst / skill.name))
    return results


def _install_copilot(workspace_root: Path) -> list[LinkResult]:
    return [
        _link(
            workspace_root / "AGENTS.md",
            workspace_root / ".github" / "copilot-instructions.md",
        )
    ]


def _install_cursor(workspace_root: Path) -> list[LinkResult]:
    return [
        _write_if_missing(
            workspace_root / ".cursor" / "rules" / "heddle-workspace.mdc",
            "---\n"
            "description: Heddle workspace orientation and skill discovery map\n"
            "globs:\n"
            "alwaysApply: true\n"
            "---\n\n"
            f"{_plain_rule_content('Cursor')}",
        )
    ]


def _install_devin(workspace_root: Path, src_root: Path) -> list[LinkResult]:
    results: list[LinkResult] = []
    for skill in _skills(src_root):
        results.append(_link(skill, workspace_root / ".devin" / "skills" / skill.name))
    return results


def _install_gemini(workspace_root: Path) -> list[LinkResult]:
    return [_link(workspace_root / "AGENTS.md", workspace_root / "GEMINI.md")]


def _install_qwen(workspace_root: Path, src_root: Path) -> list[LinkResult]:
    results = [_link(workspace_root / "AGENTS.md", workspace_root / "QWEN.md")]
    for skill in _skills(src_root):
        results.append(_link(skill, workspace_root / ".qwen" / "skills" / skill.name))
    return results


def _install_windsurf(workspace_root: Path, src_root: Path) -> list[LinkResult]:
    results: list[LinkResult] = []
    for skill in _skills(src_root):
        results.append(
            _link(skill, workspace_root / ".windsurf" / "skills" / skill.name)
        )
    results.append(
        _write_if_missing(
            workspace_root / ".windsurf" / "rules" / "heddle-workspace.md",
            "---\n"
            "description: Heddle workspace orientation and skill discovery map\n"
            "trigger: always_on\n"
            "---\n\n"
            f"{_plain_rule_content('Windsurf')}",
        )
    )
    return results


def _install_zed(workspace_root: Path) -> list[LinkResult]:
    return [_link(workspace_root / "AGENTS.md", workspace_root / ".rules")]


def _skills(src_root: Path) -> list[Path]:
    skills_dir = src_root / "skills"
    if not skills_dir.exists():
        return []
    return sorted(
        p for p in skills_dir.iterdir() if p.is_dir() and (p / "SKILL.md").exists()
    )


def _agents(src_root: Path) -> list[Path]:
    agents_dir = src_root / "agents"
    if not agents_dir.exists():
        return []
    return sorted(p for p in agents_dir.glob("*.md") if p.name.lower() != "index.md")


def _link(src: Path, dst: Path) -> LinkResult:
    if not src.exists():
        return LinkResult("skipped", dst, f"source missing: {src}")

    dst.parent.mkdir(parents=True, exist_ok=True)
    target = os.path.relpath(src, dst.parent)

    if dst.is_symlink():
        current = os.readlink(dst)
        if current == target:
            return LinkResult("ok", dst, target)
        dst.unlink()
        dst.symlink_to(target, target_is_directory=src.is_dir())
        return LinkResult("updated", dst, target)

    if dst.exists():
        return LinkResult("skipped", dst, "exists and is not a symlink")

    dst.symlink_to(target, target_is_directory=src.is_dir())
    return LinkResult("linked", dst, target)


def _write_if_missing(dst: Path, content: str) -> LinkResult:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() or dst.is_symlink():
        if dst.is_file() and not dst.is_symlink() and dst.read_text() == content:
            return LinkResult("ok", dst, "already up to date")
        return LinkResult("skipped", dst, "exists")
    dst.write_text(content)
    return LinkResult("wrote", dst, "adapter pointer")


def _plain_rule_content(agent_name: str) -> str:
    return (
        f"# Heddle Workspace for {agent_name}\n\n"
        "Use `AGENTS.md` as the canonical workspace instructions. Do not copy\n"
        "or restate the skill and subagent bodies here.\n\n"
        "When a task needs a reusable workflow, inspect\n"
        "`heddle-workspace/skills/INDEX.md` and then open only the relevant\n"
        "`SKILL.md`. When a task needs a specialized review or planning role,\n"
        "inspect `heddle-workspace/agents/INDEX.md`.\n"
    )


def run(args: argparse.Namespace) -> int:
    if args.agent_adapters_command != "install":
        raise ValueError(
            f"unknown agent-adapters command: {args.agent_adapters_command}"
        )
    enabled = [
        args.agents_standard,
        args.aider,
        args.cline,
        args.claude,
        args.codex,
        args.copilot,
        args.cursor,
        args.devin,
        args.gemini,
        args.qwen,
        args.windsurf,
        args.zed,
    ]
    if not any(enabled):
        raise ValueError("nothing to install: all adapters were disabled")

    results = install(
        args.cwd,
        install_agents_standard=args.agents_standard,
        install_aider=args.aider,
        install_cline=args.cline,
        install_claude=args.claude,
        install_codex=args.codex,
        install_copilot=args.copilot,
        install_cursor=args.cursor,
        install_devin=args.devin,
        install_gemini=args.gemini,
        install_qwen=args.qwen,
        install_windsurf=args.windsurf,
        install_zed=args.zed,
        codex_home=args.codex_home,
    )

    print("Installing Heddle agent adapters")
    print(f"  workspace: {args.cwd.resolve()}")
    if args.codex:
        print(f"  codex home: {(args.codex_home or default_codex_home()).expanduser()}")
    print()
    for r in results:
        print(f"{r.action:8} {r.path} -> {r.detail}")
    if args.codex:
        print()
        print("Restart Codex so it rescans available skills.")
    if args.claude:
        print("Restart Claude Code so it rescans .claude/.")
    project_enabled = [
        args.agents_standard,
        args.aider,
        args.cline,
        args.copilot,
        args.cursor,
        args.devin,
        args.gemini,
        args.qwen,
        args.windsurf,
        args.zed,
    ]
    if any(project_enabled):
        print("Reload other coding agents so they rescan project rules and skills.")
    return 0
