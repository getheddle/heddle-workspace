"""Copy-sync the Hooman Method global-tier docs into this repo.

Models `heddle-sdk/tools/sync_schemas.py`'s copy + sha256 manifest
pattern, extended to three destinations from one pinned source:

- ``references/`` — the method's general docs (contract, notes, design
  stances, coding conventions). Read-only projection; never hand-edited.
- ``skills/hooman-assistant/`` — the assistant skill, fanned out to every
  coding agent via the existing `agent_adapters` symlink path.
- an optional global copy (default ``~/.claude/skills/hooman-assistant``,
  D7) for Claude Code sessions started outside any Heddle-family
  workspace.

``references/UPSTREAM`` is the single manifest covering all three: source
repository, pinned tag, refresh date, refresh instruction, and a sha256
per file per target. `workspace doctor` reads it to detect drift.

The source tree is always resolved via `git archive <tag>`, not the
upstream checkout's current working tree — the pinned tag is the
contract, regardless of what commit the local clone happens to have
checked out.
"""

from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import hashlib
import os
import subprocess
import tarfile
import tempfile
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_TAG = "v0.8.1"
UPSTREAM_REPO_URL = "https://github.com/hooman/hooman-method"
GLOBAL_SKILL_DIR_ENV = "HOOMAN_ASSISTANT_GLOBAL_DIR"
UPSTREAM_REPO_ENV = "HOOMAN_METHOD_REPO"

SKIP_NAMES = {".git", ".DS_Store", ".gitignore"}
REFERENCES_SKIP_NAMES = SKIP_NAMES | {".claude", "skills"}


def default_global_skill_dir() -> Path:
    return Path(
        os.environ.get(GLOBAL_SKILL_DIR_ENV, "~/.claude/skills/hooman-assistant")
    ).expanduser()


def _default_upstream() -> Path | None:
    value = os.environ.get(UPSTREAM_REPO_ENV)
    return Path(value) if value else None


def _display_path(path: Path) -> str:
    """Render `path` `~`-relative when under the home dir, for a
    manifest that's committed to a shared repo — an absolute
    `/Users/<name>/...` path would be machine-specific and wrong on
    every other checkout."""
    try:
        return f"~/{path.relative_to(Path.home())}"
    except ValueError:
        return str(path)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _tree_files(root: Path, *, skip_names: set[str]) -> list[Path]:
    if not root.exists():
        return []
    return sorted(
        p
        for p in root.rglob("*")
        if p.is_file()
        and not any(part in skip_names for part in p.relative_to(root).parts)
    )


def _relative_hashes(
    root: Path, *, skip_names: set[str], preserve: set[str] = frozenset()
) -> dict[str, str]:
    return {
        str(p.relative_to(root)): _sha256(p)
        for p in _tree_files(root, skip_names=skip_names)
        if str(p.relative_to(root)) not in preserve
    }


def _mirror_tree(
    source: Path, dest: Path, *, skip_names: set[str], preserve: set[str] = frozenset()
) -> None:
    """Copy every file under `source` into `dest`, removing stale files.

    Files whose relative path is in `preserve` are never touched by the
    stale-removal pass (used to protect `UPSTREAM` itself when `dest` is
    `references/`).
    """
    dest.mkdir(parents=True, exist_ok=True)
    wanted = _tree_files(source, skip_names=skip_names)
    wanted_relpaths = {str(p.relative_to(source)) for p in wanted}

    for src_path in wanted:
        rel = src_path.relative_to(source)
        dst_path = dest / rel
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        dst_path.write_bytes(src_path.read_bytes())

    for dst_path in _tree_files(dest, skip_names=skip_names):
        rel = str(dst_path.relative_to(dest))
        if rel in preserve or rel in wanted_relpaths:
            continue
        dst_path.unlink()


@contextlib.contextmanager
def _extracted_tag(upstream: Path, tag: str) -> Iterator[Path]:
    """Extract the tree at `tag` from `upstream` into a temp directory.

    Uses `git archive` so the pin is the tag's committed content, not
    whatever the upstream checkout's working tree currently has checked
    out (it may be ahead or behind the pinned tag).
    """
    if not upstream.is_dir():
        raise SystemExit(f"upstream hooman-method checkout not found: {upstream}")
    with tempfile.TemporaryDirectory(prefix="hooman-method-") as tmp:
        tmp_path = Path(tmp)
        try:
            proc = subprocess.run(
                ["git", "-C", str(upstream), "archive", "--format=tar", tag],
                check=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError as exc:
            stderr = exc.stderr.decode(errors="replace") if exc.stderr else ""
            raise SystemExit(
                f"git archive {tag} failed against {upstream}: {stderr.strip()}"
            ) from exc
        archive_path = tmp_path / "archive.tar"
        archive_path.write_bytes(proc.stdout)
        extract_dir = tmp_path / "tree"
        extract_dir.mkdir()
        # No `filter=` kwarg: keeps this py3.11-compatible (added in 3.12).
        # Source is our own trusted local clone, not attacker-controlled.
        with tarfile.open(archive_path) as tar:
            tar.extractall(extract_dir)
        yield extract_dir


def sync_projection(
    root: Path,
    source: Path,
    *,
    tag: str,
    global_skill_dir: Path | None = None,
    sync_global: bool = True,
) -> dict[str, Any]:
    """Mirror an already-extracted hooman-method tree into all sync targets.

    `source` is a plain directory (no git involved) — the extracted tag
    tree in production, a fixture directory in tests.
    """
    references_dir = root / "references"
    skill_dir = root / "skills" / "hooman-assistant"
    upstream_skill = source / "skills" / "hooman-assistant"
    if not upstream_skill.is_dir():
        raise SystemExit(f"source missing skills/hooman-assistant: {upstream_skill}")

    targets: dict[str, Any] = {}

    _mirror_tree(source, references_dir, skip_names=REFERENCES_SKIP_NAMES, preserve={"UPSTREAM"})
    targets["references"] = {
        "path": "references",
        "files": _relative_hashes(
            references_dir, skip_names=REFERENCES_SKIP_NAMES, preserve={"UPSTREAM"}
        ),
    }

    _mirror_tree(upstream_skill, skill_dir, skip_names=SKIP_NAMES)
    targets["skill"] = {
        "path": "skills/hooman-assistant",
        "files": _relative_hashes(skill_dir, skip_names=SKIP_NAMES),
    }

    if sync_global:
        gdir = (global_skill_dir or default_global_skill_dir()).expanduser()
        _mirror_tree(upstream_skill, gdir, skip_names=SKIP_NAMES)
        targets["global_skill"] = {
            "path": _display_path(gdir),
            "files": _relative_hashes(gdir, skip_names=SKIP_NAMES),
        }

    data: dict[str, Any] = {
        "source": {
            "repository": UPSTREAM_REPO_URL,
            "tag": tag,
            "refreshed": dt.date.today().isoformat(),
        },
        "refresh_instruction": (
            "uv run workspace references update --upstream "
            "<path-to-local-hooman-method-clone>"
        ),
        "hash_algorithm": "sha256",
        "targets": targets,
    }
    _write_manifest(references_dir, data)
    return data


def update(
    root: Path,
    upstream: Path,
    *,
    tag: str = DEFAULT_TAG,
    global_skill_dir: Path | None = None,
    sync_global: bool = True,
) -> dict[str, Any]:
    with _extracted_tag(upstream, tag) as source:
        return sync_projection(
            root,
            source,
            tag=tag,
            global_skill_dir=global_skill_dir,
            sync_global=sync_global,
        )


def _write_manifest(references_dir: Path, data: dict[str, Any]) -> None:
    references_dir.mkdir(parents=True, exist_ok=True)
    header = (
        "# references/UPSTREAM — Hooman Method projection manifest.\n"
        "# Read-only projection (DT3): never hand-edit. Regenerate via:\n"
        "#   workspace references update --upstream <path-to-hooman-method-clone>\n\n"
    )
    body = yaml.safe_dump(data, sort_keys=False, default_flow_style=False, indent=2)
    (references_dir / "UPSTREAM").write_text(header + body)


def _load_manifest(references_dir: Path) -> dict[str, Any]:
    path = references_dir / "UPSTREAM"
    return yaml.safe_load(path.read_text()) or {}


def check(root: Path, *, global_skill_dir: Path | None = None) -> list[str]:
    """Return drift problems across all three sync targets; empty = clean.

    The global copy is skipped without complaint when absent — D7 keeps
    it an optional, per-machine artifact, not a required one.
    """
    references_dir = root / "references"
    manifest_path = references_dir / "UPSTREAM"
    if not manifest_path.exists():
        return [
            f"no references manifest at {manifest_path} — run: "
            "workspace references update --upstream <path-to-hooman-method-clone>"
        ]

    data = _load_manifest(references_dir)
    targets = data.get("targets") or {}
    problems: list[str] = []

    dirs: dict[str, tuple[Path, set[str], set[str]]] = {
        "references": (references_dir, REFERENCES_SKIP_NAMES, {"UPSTREAM"}),
        "skill": (root / "skills" / "hooman-assistant", SKIP_NAMES, set()),
        "global_skill": (
            (global_skill_dir or default_global_skill_dir()).expanduser(),
            SKIP_NAMES,
            set(),
        ),
    }

    for name, (dir_path, skip_names, preserve) in dirs.items():
        recorded = (targets.get(name) or {}).get("files")
        if recorded is None:
            continue  # not part of this sync (e.g. --no-global at update time)
        if not dir_path.exists():
            if name == "global_skill":
                continue  # optional per machine (D7); absence alone isn't drift
            problems.append(f"{name}: missing sync target directory: {dir_path}")
            continue
        actual = _relative_hashes(dir_path, skip_names=skip_names, preserve=preserve)
        missing = sorted(set(recorded) - set(actual))
        extra = sorted(set(actual) - set(recorded))
        changed = sorted(
            rel for rel in set(recorded) & set(actual) if recorded[rel] != actual[rel]
        )
        if missing:
            problems.append(f"{name}: missing files vs. pinned manifest: {', '.join(missing)}")
        if extra:
            problems.append(f"{name}: extra/unpinned files: {', '.join(extra)}")
        if changed:
            problems.append(f"{name}: drifted from pinned manifest: {', '.join(changed)}")

    return problems


def run(args: argparse.Namespace) -> int:
    if args.references_command == "update":
        upstream = args.upstream or _default_upstream()
        if upstream is None:
            raise SystemExit(
                "references update: pass --upstream <path> or set "
                f"${UPSTREAM_REPO_ENV}"
            )
        data = update(
            ROOT,
            upstream.resolve(),
            tag=args.tag,
            global_skill_dir=args.global_skills_dir,
            sync_global=not args.no_global,
        )
        print(f"synced hooman-method {data['source']['tag']} from {upstream.resolve()}")
        for name, info in data["targets"].items():
            print(f"  {name:13} {info['path']}  ({len(info['files'])} files)")
        print(f"wrote {(ROOT / 'references' / 'UPSTREAM').relative_to(ROOT)}")
        return 0

    if args.references_command == "check":
        problems = check(ROOT, global_skill_dir=args.global_skills_dir)
        if problems:
            print("references: PROBLEMS")
            for p in problems:
                print(f"  {p}")
            return 1
        print("references: in sync")
        return 0

    raise ValueError(f"unknown references command: {args.references_command}")
