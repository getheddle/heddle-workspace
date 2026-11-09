"""Tests for `heddle_workspace.doc_check` — mechanical checks on written claims."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from heddle_workspace import doc_check


def _repo(
    root: Path, name: str, files: dict[str, str], *, as_root: bool = False
) -> Path:
    """A git repo whose origin names a known repo, with ``files`` staged."""
    path = root if as_root else root / name
    path.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    subprocess.run(
        [
            "git",
            "-C",
            str(path),
            "remote",
            "add",
            "origin",
            f"https://github.com/getheddle/{name}.git",
        ],
        check=True,
    )
    for rel, text in files.items():
        target = path / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)
    subprocess.run(["git", "-C", str(path), "add", "-A"], check=True)
    return path


def _messages(report: doc_check.Report) -> list[str]:
    return [
        f"{f.check} {f.repo}/{f.path}:{f.line} {f.message}" for f in report.failures
    ]


def test_find_repos_by_origin_in_both_layouts(tmp_path: Path) -> None:
    _repo(tmp_path, "platform-workspace", {"AGENTS.md": "x\n"}, as_root=True)
    _repo(tmp_path, "heddle", {"README.md": "x\n"})
    _repo(tmp_path, "not-ours", {"README.md": "x\n"})
    repos = doc_check.find_repos(tmp_path)
    assert set(repos) == {"platform-workspace", "heddle"}
    assert repos["platform-workspace"] == tmp_path.resolve()


def test_m1_flags_missing_repo_qualified_path(tmp_path: Path) -> None:
    _repo(tmp_path, "heddle-sdk", {"swift/Sources/HeddleActor/Wire.swift": "//\n"})
    _repo(
        tmp_path,
        "heddle-workspace",
        {
            "skills/sync/SKILL.md": (
                "Edit `heddle-sdk/swift/Sources/HeddleActor/Wire.swift`.\n"
                "Not `heddle-sdk/swift/Sources/HeddleActor/Models/`.\n"
            ),
        },
    )
    report = doc_check.run_checks(tmp_path)
    expected = (
        "M1 heddle-workspace/skills/sync/SKILL.md:2 "
        "`heddle-sdk/swift/Sources/HeddleActor/Models/` does not exist"
    )
    assert _messages(report) == [expected]


def test_m1_package_fallback_placeholders_and_suffixes(tmp_path: Path) -> None:
    _repo(tmp_path, "heddle", {"src/heddle/core/envelope.py": "#\n"})
    _repo(
        tmp_path,
        "heddle-workspace",
        {
            "AGENTS.md": (
                "`heddle/core/envelope.py` resolves under src/heddle.\n"
                "`heddle/src/heddle/core/envelope.py:12` keeps its line suffix.\n"
                "`heddle-sdk/<lang>/Models.cs` is a placeholder.\n"
                "`heddle/core/*.py` is a pattern.\n"
                "`heddle/` alone names the repo.\n"
            ),
        },
    )
    report = doc_check.run_checks(tmp_path)
    assert report.failures == []
    assert report.checked == 2


def test_m1_counts_absent_repo_as_unchecked(tmp_path: Path) -> None:
    _repo(
        tmp_path,
        "heddle-workspace",
        {
            "README.md": "See `warp-design/decisions/0001-x.md`.\n",
        },
    )
    report = doc_check.run_checks(tmp_path)
    assert report.failures == []
    assert report.unchecked == 1


def test_scope_skips_history_templates_and_fences(tmp_path: Path) -> None:
    missing = "`heddle/src/heddle/gone.py`"
    _repo(tmp_path, "heddle", {"pyproject.toml": "x\n"})
    _repo(
        tmp_path,
        "heddle-workspace",
        {
            "CHANGELOG.md": f"Removed {missing}.\n",
            "templates/workspace-init/AGENTS.md": f"{missing}\n",
            "docs/releases/v1.md": f"{missing}\n",
            "notes/scratch.md": f"{missing}\n",
            "docs/GUIDE.md": f"```text\n{missing}\n```\n",
        },
    )
    assert doc_check.run_checks(tmp_path).failures == []


def test_m4_relative_links(tmp_path: Path) -> None:
    _repo(
        tmp_path,
        "heddle-workspace",
        {
            "docs/GUIDE.md": (
                "[ok](../README.md#top) [web](https://example.com) [x](#here)\n"
                "[broken](MISSING.md) `[code](ignored.md)`\n"
            ),
            "README.md": "x\n",
        },
    )
    report = doc_check.run_checks(tmp_path)
    assert _messages(report) == [
        "M4 heddle-workspace/docs/GUIDE.md:2 link `MISSING.md` does not resolve"
    ]


def test_m4_skips_docs_checked_by_mkdocs(tmp_path: Path) -> None:
    _repo(
        tmp_path,
        "heddle",
        {
            "mkdocs.yml": "site_name: x\n",
            "docs/index.md": "[broken](MISSING.md)\n",
        },
    )
    assert doc_check.run_checks(tmp_path).failures == []


def test_m2_hook_patterns_must_match_a_tracked_file(tmp_path: Path) -> None:
    command = (
        'bash -lc \'case "$f" in *heddle/schemas/v1/*|'
        "*heddle-sdk/dotnet/src/*/Models/*) echo note ;; esac'"
    )
    template = {"hooks": {"PreToolUse": [{"hooks": [{"command": command}]}]}}
    _repo(tmp_path, "heddle", {"schemas/v1/task.schema.json": "{}\n"})
    _repo(tmp_path, "heddle-sdk", {"dotnet/src/Heddle.Sdk/Wire.cs": "//\n"})
    _repo(
        tmp_path,
        "heddle-workspace",
        {
            "hooks/settings.template.json": json.dumps(template, indent=2),
        },
    )
    report = doc_check.run_checks(tmp_path)
    assert [f.check for f in report.failures] == ["M2"]
    assert "*heddle-sdk/dotnet/src/*/Models/*" in report.failures[0].message


def test_target_repo_fails_own_files_and_warns_on_references_into_it(
    tmp_path: Path,
) -> None:
    _repo(
        tmp_path,
        "heddle",
        {
            "src/heddle/core/envelope.py": "#\n",
            "README.md": "`heddle/src/heddle/core/renamed.py`\n",
        },
    )
    _repo(
        tmp_path,
        "heddle-workspace",
        {
            "AGENTS.md": "`heddle/src/heddle/core/gone.py` and `heddle-sdk/x/y.cs`\n",
        },
    )
    report = doc_check.run_checks(tmp_path, target="heddle")
    assert [(f.check, f.repo) for f in report.failures] == [("M1", "heddle")]
    assert [(f.check, f.repo) for f in report.warnings] == [("M1", "heddle-workspace")]


def test_cli_exit_codes_and_github_format(tmp_path: Path, capsys) -> None:
    from heddle_workspace.cli import main

    _repo(tmp_path, "heddle-workspace", {"README.md": "[x](MISSING.md)\n"})
    assert main(["-C", str(tmp_path), "doc-check", "--format", "github"]) == 1
    out = capsys.readouterr().out
    assert "::error file=heddle-workspace/README.md,line=1,title=M4::" in out

    (tmp_path / "heddle-workspace" / "MISSING.md").write_text("x\n")
    subprocess.run(
        ["git", "-C", str(tmp_path / "heddle-workspace"), "add", "-A"], check=True
    )
    assert main(["-C", str(tmp_path), "doc-check"]) == 0


def test_links_named_by_repo_are_checked_once_by_m1(
    tmp_path: Path,
) -> None:
    _repo(
        tmp_path,
        "platform-workspace",
        {
            "AGENTS.md": "[toolkit](heddle-workspace/) [doc](heddle-workspace/docs/A.md)\n"
            "[gone](heddle-workspace/docs/GONE.md)\n",
        },
    )
    _repo(tmp_path, "heddle-workspace", {"docs/A.md": "x\n"})
    report = doc_check.run_checks(tmp_path, target="platform-workspace")
    assert [(f.check, f.message) for f in report.failures] == [
        ("M1", "`heddle-workspace/docs/GONE.md` does not exist")
    ]
