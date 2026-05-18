"""Thin wrappers around `git` invocations used by the workspace CLI."""

from __future__ import annotations

import subprocess
from pathlib import Path


class GitError(RuntimeError):
    pass


def run(
    *args: str,
    cwd: Path | None = None,
    check: bool = True,
    capture: bool = False,
) -> subprocess.CompletedProcess:
    kwargs: dict = {"cwd": cwd}
    if capture:
        kwargs["capture_output"] = True
        kwargs["text"] = True
    result = subprocess.run(["git", *args], **kwargs)
    if check and result.returncode != 0:
        out = (result.stderr or result.stdout or "") if capture else ""
        raise GitError(f"git {' '.join(args)} failed (cwd={cwd}): {out.strip()}")
    return result


def is_repo(path: Path) -> bool:
    return (path / ".git").exists()


def origin_url(repo: Path) -> str | None:
    if not is_repo(repo):
        return None
    r = run("remote", "get-url", "origin", cwd=repo, check=False, capture=True)
    if r.returncode != 0:
        return None
    return r.stdout.strip() or None


def current_branch(repo: Path) -> str | None:
    if not is_repo(repo):
        return None
    r = run("symbolic-ref", "--short", "HEAD", cwd=repo, check=False, capture=True)
    if r.returncode != 0:
        return None
    return r.stdout.strip() or None


def is_clean(repo: Path) -> bool:
    r = run("status", "--porcelain", cwd=repo, capture=True)
    return r.stdout.strip() == ""


def ahead_behind(repo: Path, branch: str) -> tuple[int, int] | None:
    """Return (ahead, behind) of local branch vs origin/<branch>, or None."""
    r = run(
        "rev-list",
        "--left-right",
        "--count",
        f"{branch}...origin/{branch}",
        cwd=repo,
        check=False,
        capture=True,
    )
    if r.returncode != 0:
        return None
    parts = r.stdout.strip().split()
    if len(parts) != 2:
        return None
    return int(parts[0]), int(parts[1])
