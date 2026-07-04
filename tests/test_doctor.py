"""Tests for the `workspace doctor` Hooman Method references-pin check."""

from __future__ import annotations

import argparse
from pathlib import Path

from heddle_workspace import agent_adapters, doctor, manifest, references


def _init_manifest(root: Path) -> None:
    m = manifest.Manifest(name="ws", umbrella_remote=None, description=None, repos=[])
    manifest.save(root, m)
    (root / ".gitignore").write_text(manifest.render_gitignore(m))


def _synced_toolkit(base: Path) -> Path:
    source = base / "source"
    (source / "skills" / "hooman-assistant" / "references").mkdir(parents=True)
    (source / "hooman-contract.md").write_text("contract v1\n")
    (source / "skills" / "hooman-assistant" / "SKILL.md").write_text("skill v1\n")

    toolkit = base / "toolkit"
    references.sync_projection(
        toolkit, source, tag="v-test", global_skill_dir=base / "global"
    )
    return toolkit


def test_doctor_clean_when_references_in_sync(tmp_path, monkeypatch, capsys) -> None:
    toolkit = _synced_toolkit(tmp_path)
    monkeypatch.setattr(agent_adapters, "toolkit_root", lambda: toolkit)
    monkeypatch.setattr(references, "default_global_skill_dir", lambda: tmp_path / "global")

    root = tmp_path / "workspace"
    root.mkdir()
    _init_manifest(root)

    exit_code = doctor.run(argparse.Namespace(cwd=root))

    assert exit_code == 0
    assert "ok   references/ (Hooman Method projection)" in capsys.readouterr().out


def test_doctor_flags_references_drift(tmp_path, monkeypatch, capsys) -> None:
    toolkit = _synced_toolkit(tmp_path)
    monkeypatch.setattr(agent_adapters, "toolkit_root", lambda: toolkit)
    monkeypatch.setattr(references, "default_global_skill_dir", lambda: tmp_path / "global")
    (toolkit / "references" / "hooman-contract.md").write_text("hand-edited!\n")

    root = tmp_path / "workspace"
    root.mkdir()
    _init_manifest(root)

    exit_code = doctor.run(argparse.Namespace(cwd=root))

    out = capsys.readouterr().out
    assert exit_code == 1
    assert "references: references: drifted" in out
    assert "hooman-contract.md" in out
