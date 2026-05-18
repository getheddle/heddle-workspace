"""Smoke tests for the manifest module."""

from __future__ import annotations

from pathlib import Path

import pytest

from heddle_workspace import manifest
from heddle_workspace.manifest import Manifest, RepoEntry


def test_round_trip(tmp_path: Path) -> None:
    m = Manifest(
        name="DemoProject",
        umbrella_remote="git@github.com:DemoOrg/workspace.git",
        description="example",
        repos=[
            RepoEntry(path="heddle", remote="git@github.com:getheddle/heddle.git"),
            RepoEntry(
                path="my-app",
                remote="git@github.com:DemoOrg/my-app.git",
                branch="develop",
                role="app",
            ),
        ],
    )
    manifest.save(tmp_path, m)
    reloaded = manifest.load(tmp_path)
    assert reloaded.name == "DemoProject"
    assert reloaded.umbrella_remote == m.umbrella_remote
    assert len(reloaded.repos) == 2
    assert reloaded.repos[1].branch == "develop"
    assert reloaded.repos[1].role == "app"


def test_load_missing(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        manifest.load(tmp_path)


def test_render_gitignore(tmp_path: Path) -> None:
    m = Manifest(
        name="Demo",
        repos=[RepoEntry(path="heddle", remote="x"), RepoEntry(path="app", remote="y")],
    )
    out = manifest.render_gitignore(m)
    assert "/(local-only)/" in out
    assert "/heddle/" in out
    assert "/app/" in out
    assert ".DS_Store" in out


def test_find(tmp_path: Path) -> None:
    m = Manifest(name="Demo", repos=[RepoEntry(path="heddle", remote="x")])
    assert m.find("heddle") is not None
    assert m.find("missing") is None


def test_default_branch(tmp_path: Path) -> None:
    """Branch defaults to `main` when omitted from the YAML."""
    yaml_text = (
        "workspace:\n"
        "  name: Demo\n"
        "repos:\n"
        "  - path: heddle\n"
        "    remote: git@github.com:getheddle/heddle.git\n"
    )
    (tmp_path / ".heddle-workspace.yaml").write_text(yaml_text)
    m = manifest.load(tmp_path)
    assert m.repos[0].branch == "main"


def test_missing_name_rejected(tmp_path: Path) -> None:
    yaml_text = "workspace: {}\nrepos: []\n"
    (tmp_path / ".heddle-workspace.yaml").write_text(yaml_text)
    with pytest.raises(ValueError, match="workspace.name"):
        manifest.load(tmp_path)
