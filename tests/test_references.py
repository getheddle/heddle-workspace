"""Tests for `heddle_workspace.references` — Hooman Method projection sync."""

from __future__ import annotations

import subprocess
from pathlib import Path

from heddle_workspace import references


def _make_fixture_source(base: Path) -> Path:
    """A minimal hooman-method-shaped tree: general docs + the skill."""
    source = base / "source"
    (source / "design-stance" / "universal").mkdir(parents=True)
    (source / "skills" / "hooman-assistant" / "references").mkdir(parents=True)
    (source / "hooman-contract.md").write_text("contract v1\n")
    (source / "hooman-notes.md").write_text("notes v1\n")
    (source / "design-stance" / "universal" / "design-stance-universal.md").write_text(
        "stance v1\n"
    )
    (source / "skills" / "hooman-assistant" / "SKILL.md").write_text("skill v1\n")
    (source / "skills" / "hooman-assistant" / "references" / "workspace.md").write_text(
        "workspace rules v1\n"
    )
    (source / ".DS_Store").write_text("junk")
    return source


def test_sync_projection_populates_all_three_targets(tmp_path: Path) -> None:
    source = _make_fixture_source(tmp_path)
    root = tmp_path / "toolkit"
    global_dir = tmp_path / "global"

    data = references.sync_projection(
        root, source, tag="v-test", global_skill_dir=global_dir
    )

    assert (root / "references" / "hooman-contract.md").read_text() == "contract v1\n"
    assert (root / "references" / "skills").exists() is False  # skill excluded here
    assert (root / "skills" / "hooman-assistant" / "SKILL.md").read_text() == "skill v1\n"
    assert (global_dir / "SKILL.md").read_text() == "skill v1\n"
    assert not (root / "references" / ".DS_Store").exists()

    assert data["source"]["tag"] == "v-test"
    assert set(data["targets"]) == {"references", "skill", "global_skill"}
    assert "UPSTREAM" not in data["targets"]["references"]["files"]
    assert (root / "references" / "UPSTREAM").exists()


def test_sync_projection_records_global_path_home_relative(tmp_path: Path, monkeypatch) -> None:
    """A committed manifest must never bake in a machine-specific absolute
    home path (e.g. `/Users/<name>/...`) — it's meaningless and leaks
    local FS layout on every other checkout."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    source = _make_fixture_source(tmp_path)
    root = tmp_path / "toolkit"
    global_dir = tmp_path / ".claude" / "skills" / "hooman-assistant"

    data = references.sync_projection(
        root, source, tag="v-test", global_skill_dir=global_dir
    )

    assert data["targets"]["global_skill"]["path"] == "~/.claude/skills/hooman-assistant"


def test_sync_projection_skip_global(tmp_path: Path) -> None:
    source = _make_fixture_source(tmp_path)
    root = tmp_path / "toolkit"
    global_dir = tmp_path / "global"

    data = references.sync_projection(
        root, source, tag="v-test", global_skill_dir=global_dir, sync_global=False
    )

    assert not global_dir.exists()
    assert "global_skill" not in data["targets"]


def test_sync_projection_removes_stale_files(tmp_path: Path) -> None:
    source = _make_fixture_source(tmp_path)
    root = tmp_path / "toolkit"
    global_dir = tmp_path / "global"
    references.sync_projection(root, source, tag="v-test", global_skill_dir=global_dir)

    (source / "hooman-notes.md").unlink()
    references.sync_projection(root, source, tag="v-test", global_skill_dir=global_dir)

    assert not (root / "references" / "hooman-notes.md").exists()


def test_check_is_clean_immediately_after_sync(tmp_path: Path) -> None:
    source = _make_fixture_source(tmp_path)
    root = tmp_path / "toolkit"
    global_dir = tmp_path / "global"
    references.sync_projection(root, source, tag="v-test", global_skill_dir=global_dir)

    assert references.check(root, global_skill_dir=global_dir) == []


def test_check_reports_missing_manifest(tmp_path: Path) -> None:
    root = tmp_path / "toolkit"
    root.mkdir()

    problems = references.check(root, global_skill_dir=tmp_path / "global")

    assert len(problems) == 1
    assert "no references manifest" in problems[0]


def test_check_detects_drift_per_target(tmp_path: Path) -> None:
    source = _make_fixture_source(tmp_path)
    root = tmp_path / "toolkit"
    global_dir = tmp_path / "global"
    references.sync_projection(root, source, tag="v-test", global_skill_dir=global_dir)

    (root / "references" / "hooman-contract.md").write_text("hand-edited!\n")
    (root / "skills" / "hooman-assistant" / "SKILL.md").write_text("hand-edited!\n")
    (global_dir / "SKILL.md").write_text("hand-edited!\n")

    problems = references.check(root, global_skill_dir=global_dir)

    assert any("references: drifted" in p and "hooman-contract.md" in p for p in problems)
    assert any("skill: drifted" in p and "SKILL.md" in p for p in problems)
    assert any("global_skill: drifted" in p and "SKILL.md" in p for p in problems)


def test_check_skips_missing_global_copy_without_complaint(tmp_path: Path) -> None:
    source = _make_fixture_source(tmp_path)
    root = tmp_path / "toolkit"
    global_dir = tmp_path / "global"
    references.sync_projection(root, source, tag="v-test", global_skill_dir=global_dir)

    # Simulate a machine that never had the D7 global copy installed.
    for p in sorted(global_dir.rglob("*"), reverse=True):
        p.unlink() if p.is_file() else p.rmdir()
    global_dir.rmdir()

    assert references.check(root, global_skill_dir=global_dir) == []


def test_update_pins_the_tagged_tree_not_the_working_copy(tmp_path: Path) -> None:
    """`update()` must resolve the pinned tag via `git archive`, not whatever
    the upstream checkout's working tree currently has checked out — the
    real hooman-method clone on the reference machine was a commit ahead of
    its own latest tag when this was written."""
    upstream = tmp_path / "upstream"
    _make_fixture_source(tmp_path).rename(upstream)
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=upstream, check=True)
    subprocess.run(["git", "add", "-A"], cwd=upstream, check=True)
    subprocess.run(
        ["git", "-c", "user.email=t@example.com", "-c", "user.name=t", "commit", "-q", "-m", "v-test"],
        cwd=upstream,
        check=True,
    )
    subprocess.run(["git", "tag", "v-test"], cwd=upstream, check=True)
    # Move past the tag: the local clone's working tree is no longer what
    # was tagged.
    (upstream / "hooman-contract.md").write_text("contract v2 (post-tag)\n")
    subprocess.run(["git", "add", "-A"], cwd=upstream, check=True)
    subprocess.run(
        ["git", "-c", "user.email=t@example.com", "-c", "user.name=t", "commit", "-q", "-m", "post-tag drift"],
        cwd=upstream,
        check=True,
    )

    root = tmp_path / "toolkit"
    data = references.update(
        root, upstream, tag="v-test", global_skill_dir=tmp_path / "global"
    )

    assert data["source"]["tag"] == "v-test"
    assert (root / "references" / "hooman-contract.md").read_text() == "contract v1\n"
