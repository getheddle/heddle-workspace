"""Read and write `.heddle-workspace.yaml`.

The manifest is the authoritative declaration of which child repos belong
in a workspace and where to clone them from. Schema is intentionally
minimal — `path / remote / branch` per repo, no SHA pinning by default.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

MANIFEST_FILENAME = ".heddle-workspace.yaml"
LOCAL_ONLY_DIR = "(local-only)"


@dataclass
class RepoEntry:
    path: str
    remote: str
    branch: str = "main"
    pin: str | None = None
    role: str | None = None

    def to_dict(self) -> dict:
        out: dict = {"path": self.path, "remote": self.remote, "branch": self.branch}
        if self.pin:
            out["pin"] = self.pin
        if self.role:
            out["role"] = self.role
        return out

    @classmethod
    def from_dict(cls, data: dict) -> RepoEntry:
        return cls(
            path=data["path"],
            remote=data["remote"],
            branch=data.get("branch", "main"),
            pin=data.get("pin"),
            role=data.get("role"),
        )


@dataclass
class Manifest:
    name: str
    umbrella_remote: str | None = None
    description: str | None = None
    repos: list[RepoEntry] = field(default_factory=list)

    def to_dict(self) -> dict:
        ws: dict = {"name": self.name}
        if self.description:
            ws["description"] = self.description
        if self.umbrella_remote:
            ws["umbrella_remote"] = self.umbrella_remote
        return {
            "workspace": ws,
            "repos": [r.to_dict() for r in self.repos],
        }

    @classmethod
    def from_dict(cls, data: dict) -> Manifest:
        ws = data.get("workspace") or {}
        if "name" not in ws:
            raise ValueError("manifest missing required field: workspace.name")
        return cls(
            name=ws["name"],
            umbrella_remote=ws.get("umbrella_remote"),
            description=ws.get("description"),
            repos=[RepoEntry.from_dict(r) for r in data.get("repos") or []],
        )

    def find(self, path: str) -> RepoEntry | None:
        for r in self.repos:
            if r.path == path:
                return r
        return None


def manifest_path(workspace_root: Path) -> Path:
    return workspace_root / MANIFEST_FILENAME


def load(workspace_root: Path) -> Manifest:
    p = manifest_path(workspace_root)
    if not p.exists():
        raise FileNotFoundError(f"no manifest at {p}")
    data = yaml.safe_load(p.read_text()) or {}
    return Manifest.from_dict(data)


def save(workspace_root: Path, manifest: Manifest) -> Path:
    p = manifest_path(workspace_root)
    header = (
        "# .heddle-workspace.yaml — source of truth for which child repos\n"
        "# belong in this workspace. Edit by hand or via `workspace add/rm`.\n"
        "# See heddle-workspace/docs/WORKSPACE_SYNC_DESIGN.md for full spec.\n\n"
    )
    body = yaml.safe_dump(
        manifest.to_dict(),
        sort_keys=False,
        default_flow_style=False,
        indent=2,
    )
    p.write_text(header + body)
    return p


def render_gitignore(manifest: Manifest) -> str:
    """Produce the .gitignore content for an umbrella tracking this manifest."""
    lines = [
        "# Carve-out: anything local-only is untracked, full stop.",
        f"/{LOCAL_ONLY_DIR}/",
        "",
        "# Each manifest entry is its own git repo; the umbrella never tracks",
        "# their content. Listed explicitly so a stray `git add -A` does the",
        "# right thing even if the directory is empty.",
    ]
    for r in manifest.repos:
        lines.append(f"/{r.path}/")
    lines.extend(
        [
            "",
            "# Machine noise",
            ".DS_Store",
            "",
        ]
    )
    return "\n".join(lines)
