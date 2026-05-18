"""`workspace link <remote>` — link a divergent local workspace to an umbrella."""

from __future__ import annotations

import argparse
from pathlib import Path

from heddle_workspace import git


def run(args: argparse.Namespace) -> int:
    root: Path = args.cwd.resolve()
    if not git.is_repo(root):
        raise RuntimeError(
            f"{root} is not a git repo. Run `workspace init` first to commit "
            "your current loose-file state, then `workspace link` to merge."
        )

    existing = git.origin_url(root)
    if existing:
        if existing == args.remote:
            print(f"origin already set to {existing}; proceeding to fetch.")
        else:
            raise RuntimeError(
                f"origin already set to {existing}; cannot link to {args.remote}. "
                "Resolve manually (`git remote set-url` or `git remote add`)."
            )
    else:
        git.run("remote", "add", "origin", args.remote, cwd=root)
        print(f"added origin: {args.remote}")

    git.run("fetch", "origin", cwd=root)
    print(f"fetched origin/{args.branch}")

    # Merge unrelated histories. This is the step that may produce conflicts;
    # we intentionally do not auto-resolve them. The operator gets the merge
    # state and resolves with normal git tools.
    r = git.run(
        "merge",
        "--allow-unrelated-histories",
        f"origin/{args.branch}",
        cwd=root,
        check=False,
        capture=True,
    )
    if r.returncode == 0:
        print(r.stdout.strip() or "merge succeeded.")
        _print_post_link()
        return 0

    print(r.stdout)
    print(r.stderr)
    print()
    print("Merge stopped — conflicts to resolve. See:")
    print(
        "  docs/WORKSPACE_SYNC_DESIGN.md → 'Phase 2.5 — Resolve conflicts' "
        "in heddle-workspace, for the three conflict categories "
        "(loose files, manifest, divergent child-repo work)."
    )
    print("After resolving, `git add` the files, `git commit`, then `workspace sync`.")
    return 1


def _print_post_link() -> None:
    print()
    print("Next steps:")
    print("  workspace sync     # clone any manifest entry not yet present locally")
    print("  workspace status   # verify clean")
    print("  git push origin main  # publish the merged umbrella")
