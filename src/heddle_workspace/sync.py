"""`workspace sync` — clone missing manifest entries; fetch the rest."""

from __future__ import annotations

import argparse
from pathlib import Path

from heddle_workspace import git, manifest


def run(args: argparse.Namespace) -> int:
    root: Path = args.cwd.resolve()
    m = manifest.load(root)
    cloned = 0
    fetched = 0
    skipped = 0

    for repo in m.repos:
        target = root / repo.path
        if not target.exists():
            print(f"clone  {repo.path}  ←  {repo.remote}")
            git.run(
                "clone",
                "--branch",
                repo.branch,
                repo.remote,
                str(target),
                cwd=root,
            )
            cloned += 1
            continue

        if not git.is_repo(target):
            print(f"skip   {repo.path}  (exists but not a git repo)")
            skipped += 1
            continue

        if args.fetch:
            print(f"fetch  {repo.path}")
            git.run("fetch", "origin", cwd=target, check=False)
            fetched += 1
        else:
            skipped += 1

    print()
    print(f"sync complete: {cloned} cloned, {fetched} fetched, {skipped} skipped")
    return 0
