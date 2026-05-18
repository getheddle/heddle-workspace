"""`workspace doctor` — verify remote reachability and .gitignore coverage."""

from __future__ import annotations

import argparse
from pathlib import Path

from heddle_workspace import git, manifest


def run(args: argparse.Namespace) -> int:
    root: Path = args.cwd.resolve()
    m = manifest.load(root)
    problems: list[str] = []

    # Remote reachability — ls-remote with --exit-code is the cheap check.
    for repo in m.repos:
        r = git.run(
            "ls-remote", "--exit-code", "--heads", repo.remote, repo.branch,
            check=False, capture=True,
        )
        if r.returncode != 0:
            problems.append(
                f"  unreachable: {repo.path}  ←  {repo.remote} ({repo.branch})"
            )
        else:
            print(f"  ok   {repo.path}")

    # .gitignore coverage
    gitignore = root / ".gitignore"
    expected = manifest.render_gitignore(m)
    actual = gitignore.read_text() if gitignore.exists() else ""
    if actual.strip() != expected.strip():
        problems.append(
            "  .gitignore drift: contents differ from manifest-derived render."
        )

    print()
    if problems:
        print("doctor: PROBLEMS")
        for p in problems:
            print(p)
        return 1
    print("doctor: clean.")
    return 0
