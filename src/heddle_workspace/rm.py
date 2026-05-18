"""`workspace rm <path>` — remove a manifest entry. Working tree untouched."""

from __future__ import annotations

import argparse
from pathlib import Path

from heddle_workspace import manifest


def run(args: argparse.Namespace) -> int:
    root: Path = args.cwd.resolve()
    m = manifest.load(root)
    entry = m.find(args.path)
    if not entry:
        raise ValueError(f"no manifest entry for {args.path}")
    m.repos = [r for r in m.repos if r.path != args.path]
    manifest.save(root, m)
    (root / ".gitignore").write_text(manifest.render_gitignore(m))
    print(f"removed manifest entry: {args.path}")
    print(f"the working tree at {args.path} is untouched.")
    return 0
