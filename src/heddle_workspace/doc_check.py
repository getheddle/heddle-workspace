"""`workspace doc-check` — mechanical checks on written claims across the repos.

The mechanical layer of repo dreaming (Heddle-Platform
``roadmap/repo-dreaming.md``, *Mechanical layer: design*). It checks only what
is written unambiguously, so a failure is a real broken claim:

- **M1** — a path that starts with a known repo name (``heddle-sdk/...``) exists
  in that repo. ``heddle/<package path>`` also resolves under
  ``heddle/src/heddle/``.
- **M2** — every path pattern in a hook template's ``case`` statement matches at
  least one tracked file, so a reminder hook can't go silently dead.
- **M4** — relative Markdown links resolve, except in a ``docs/`` tree that
  MkDocs already checks with ``mkdocs build --strict``.

- **M3** — registered claims hold: each entry in a repo's ``doc-claims.yaml``
  names a text in a file and the source it must equal (see ``check_m3``).

Repos are found by their ``origin`` remote, in the root directory and its
immediate children, so the same command works in the workspace layout (where
``platform-workspace`` is the root itself) and in CI (each repo checked out
side by side). A reference into a repo that isn't checked out is counted as
unchecked, never as a failure.

With ``--repo NAME``, the check fails only on NAME's own files, and references
from the other repos *into* NAME are reported as warnings: a rename in NAME
breaks them, but the fix lives in the other repo.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

KNOWN_REPOS = (
    "heddle",
    "heddle-sdk",
    "heddle-workspace",
    "platform-workspace",
    "getheddle.github.io",
    "warp-design",
)

# Files whose claims agents and readers act on. Historical records, templates
# (which resolve where they're installed) and frozen release notes are out.
_SCOPE_NAMES = {"AGENTS.md", "CLAUDE.md", "README.md"}
_SCOPE_PREFIXES = ("skills/", "agents/", "hooks/", "docs/", "anchors/")
_EXCLUDED = re.compile(
    r"(^|/)(templates|audits|\(archive\)|\(local-only\)|releases)/"
    r"|(^|/)CHANGELOG\.md$|-feedback\.md$|(^|/)FEEDBACK-"
)
_PLACEHOLDER = re.compile(r"[<>{}*$]|X\.Y|NNNN|\.\.\.")
_FENCE = re.compile(r"^(```|~~~).*?^\1", re.MULTILINE | re.DOTALL)
_INLINE_CODE = re.compile(r"`([^`\n]+)`")
_LINK = re.compile(r"\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
_CASE = re.compile(r'case\s+\\?"?\$\w+\\?"?\s+in\s+(.*?)\)', re.DOTALL)


@dataclass(frozen=True)
class Finding:
    check: str
    repo: str
    path: str
    line: int
    message: str


@dataclass
class Report:
    failures: list[Finding] = field(default_factory=list)
    warnings: list[Finding] = field(default_factory=list)
    unchecked: int = 0
    checked: int = 0


def _git(path: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(path), *args], capture_output=True, text=True, check=False
    )
    return result.stdout if result.returncode == 0 else ""


def find_repos(root: Path) -> dict[str, Path]:
    """Map known repo names to checkouts in ``root`` or its immediate children."""
    repos: dict[str, Path] = {}
    candidates = [root, *sorted(p for p in root.iterdir() if p.is_dir())]
    for candidate in candidates:
        if not (candidate / ".git").exists():
            continue
        url = _git(candidate, "remote", "get-url", "origin").strip()
        name = url.rstrip("/").removesuffix(".git").rsplit("/", 1)[-1]
        if name in KNOWN_REPOS and name not in repos:
            repos[name] = candidate.resolve()
    return repos


def tracked_files(repo: Path) -> list[str]:
    return [line for line in _git(repo, "ls-files").splitlines() if line]


def in_scope(rel: str) -> bool:
    if _EXCLUDED.search(rel):
        return False
    return Path(rel).name in _SCOPE_NAMES or rel.startswith(_SCOPE_PREFIXES)


def _mkdocs_checked(repo: Path, rel: str) -> bool:
    return rel.startswith("docs/") and (repo / "mkdocs.yml").exists()


def _blank_fences(text: str) -> str:
    """Replace fenced code blocks with blank lines, keeping line numbers."""
    return _FENCE.sub(lambda m: "\n" * m.group(0).count("\n"), text)


def _line_of(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _clean_token(token: str) -> str:
    token = token.strip().rstrip(".,;:)")
    token = token.split("#", 1)[0]
    return re.sub(r":\d+(-\d+)?$", "", token)


def resolve_qualified(token: str, repos: dict[str, Path]) -> bool | None:
    """True/False for a repo-qualified path; None when its repo isn't present."""
    repo_name, _, rest = token.partition("/")
    repo = repos.get(repo_name)
    if repo is None:
        return None
    rest = rest.rstrip("/")
    if (repo / rest).exists():
        return True
    return repo_name == "heddle" and (repo / "src" / "heddle" / rest).exists()


def qualified_tokens(text: str) -> list[tuple[str, int]]:
    """Repo-qualified path tokens in inline code and link targets, with lines."""
    body = _blank_fences(text)
    found: list[tuple[str, int]] = []
    spans = [(m.group(1), m.start()) for m in _INLINE_CODE.finditer(body)]
    spans += [(m.group(1), m.start()) for m in _LINK.finditer(body)]
    for raw, offset in spans:
        token = _clean_token(raw)
        if " " in token or "/" not in token or _PLACEHOLDER.search(token):
            continue
        head, _, rest = token.partition("/")
        if head in KNOWN_REPOS and rest.strip("/"):
            found.append((token, _line_of(body, offset)))
    return found


def relative_links(text: str) -> list[tuple[str, int]]:
    """Relative Markdown link targets, outside code, with lines."""
    body = _INLINE_CODE.sub(lambda m: " " * len(m.group(0)), _blank_fences(text))
    found: list[tuple[str, int]] = []
    for m in _LINK.finditer(body):
        target = m.group(1).split("#", 1)[0].split("?", 1)[0]
        if not target or re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target):
            continue
        if target.startswith("/") or _PLACEHOLDER.search(target):
            continue
        found.append((target, _line_of(body, m.start())))
    return found


def _within(path: Path, base: Path) -> bool:
    try:
        path.relative_to(base)
    except ValueError:
        return False
    return True


def check_m1(
    name: str, repo: Path, repos: dict[str, Path], report: Report, target: str | None
) -> None:
    for rel in tracked_files(repo):
        path = repo / rel
        if not rel.endswith(".md") or not in_scope(rel) or path.is_symlink():
            continue
        if not path.is_file():
            continue
        text = path.read_text(errors="replace")
        for token, line in qualified_tokens(text):
            ref_repo = token.partition("/")[0]
            if target is not None and name != target and ref_repo != target:
                continue
            ok = resolve_qualified(token, repos)
            if ok is None:
                report.unchecked += 1
                continue
            report.checked += 1
            if ok:
                continue
            finding = Finding("M1", name, rel, line, f"`{token}` does not exist")
            if target is None or name == target:
                report.failures.append(finding)
            else:
                report.warnings.append(finding)


def check_m4(name: str, repo: Path, repos: dict[str, Path], report: Report) -> None:
    known = list(repos.values())
    for rel in tracked_files(repo):
        path = repo / rel
        if not rel.endswith(".md") or not in_scope(rel) or path.is_symlink():
            continue
        if not path.is_file() or _mkdocs_checked(repo, rel):
            continue
        text = path.read_text(errors="replace")
        for target, line in relative_links(text):
            if target.removeprefix("./").partition("/")[0] in KNOWN_REPOS:
                # Named by repo: M1 checks it, in either layout (the umbrella's
                # siblings sit inside it locally and beside it in CI).
                continue
            resolved = (path.parent / target).resolve()
            if not _within(resolved, repo) and not any(
                _within(resolved, k) for k in known if k != repo
            ):
                report.unchecked += 1
                continue
            report.checked += 1
            if not resolved.exists():
                report.failures.append(
                    Finding("M4", name, rel, line, f"link `{target}` does not resolve")
                )


def hook_patterns(text: str) -> list[str]:
    """Path patterns from shell ``case`` statements in a hook template's commands."""
    data = json.loads(text)
    commands: list[str] = []

    def walk(node: object) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                if key == "command" and isinstance(value, str):
                    commands.append(value)
                else:
                    walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(data)
    patterns: list[str] = []
    for command in commands:
        for m in _CASE.finditer(command):
            patterns += [p.strip() for p in m.group(1).split("|") if p.strip()]
    return patterns


def check_m2(name: str, repo: Path, repos: dict[str, Path], report: Report) -> None:
    corpus: list[str] | None = None
    for rel in tracked_files(repo):
        if not (rel.startswith("hooks/") and rel.endswith(".json")):
            continue
        text = (repo / rel).read_text(errors="replace")
        for pattern in hook_patterns(text):
            if corpus is None:
                corpus = [
                    f"/{repo_name}/{f}"
                    for repo_name, path in repos.items()
                    for f in tracked_files(path)
                ]
            if any(fnmatch.fnmatchcase(p, pattern) for p in corpus):
                report.checked += 1
                continue
            mentioned = [r for r in KNOWN_REPOS if f"{r}/" in pattern]
            if mentioned and not all(r in repos for r in mentioned):
                report.unchecked += 1
                continue
            report.checked += 1
            line = _line_of(text, max(text.find(pattern.lstrip("*")), 0))
            report.failures.append(
                Finding(
                    "M2",
                    name,
                    rel,
                    line,
                    f"hook pattern `{pattern}` matches no tracked file",
                )
            )


CLAIMS_FILE = "doc-claims.yaml"
_TAG = re.compile(r"refs/tags/(v(\d+)\.(\d+)\.(\d+))$")


class ClaimError(Exception):
    """A claim or its source can't be read: a broken claim, reported as M3."""


class Unavailable(Exception):
    """The claim's source lives in a repo that isn't checked out."""


def _claim_path(spec: str, repo: Path, repos: dict[str, Path]) -> Path:
    head, _, rest = spec.partition("/")
    if head in KNOWN_REPOS and rest:
        if head not in repos:
            raise Unavailable(head)
        return repos[head] / rest
    return repo / spec


def _read(spec: str, repo: Path, repos: dict[str, Path]) -> str:
    path = _claim_path(spec, repo, repos)
    if not path.is_file():
        raise ClaimError(f"`{spec}` does not exist")
    return path.read_text(errors="replace")


def _latest_tag(repo_name: str, repos: dict[str, Path]) -> str:
    if repo_name not in repos:
        raise Unavailable(repo_name)
    out = _git(repos[repo_name], "ls-remote", "--tags", "origin", "v*")
    tags = [m for line in out.splitlines() if (m := _TAG.search(line))]
    if not tags:
        raise ClaimError(f"no v<major>.<minor>.<patch> tags found for {repo_name}")
    best = max(tags, key=lambda m: tuple(int(g) for g in m.groups()[1:]))
    return best.group(1)


def claim_source(source: dict[str, Any], repo: Path, repos: dict[str, Path]) -> str:
    """The value a claim must equal, read from its source."""
    if "value" in source:
        return str(source["value"])
    if "toml" in source:
        import tomllib

        data: Any = tomllib.loads(_read(source["toml"], repo, repos))
        for key in str(source["key"]).split("."):
            if not isinstance(data, dict) or key not in data:
                raise ClaimError(f"`{source['key']}` not in `{source['toml']}`")
            data = data[key]
        return str(data)
    if "json_count" in source:
        data = json.loads(_read(source["json_count"], repo, repos))
        for key in str(source.get("key", "")).split(".") if source.get("key") else []:
            data = data[key]
        return str(len(data))
    if "line_count" in source:
        pattern = re.compile(source["pattern"], re.MULTILINE)
        return str(len(pattern.findall(_read(source["line_count"], repo, repos))))
    if "latest_tag" in source:
        return _latest_tag(source["latest_tag"], repos)
    raise ClaimError(f"unknown source {sorted(source)}")


def check_m3(name: str, repo: Path, repos: dict[str, Path], report: Report) -> None:
    """Check ``doc-claims.yaml`` at the repo root.

    Each claim has an ``id``, a ``file``, a ``pattern`` (a regex whose first
    matched group, or whole match, is the claimed text; every match must agree) and an
    ``equals`` source: ``value``, ``toml`` + ``key``, ``json_count`` (+ ``key``),
    ``line_count`` + ``pattern``, or ``latest_tag`` (a repo name). File paths
    are repo-relative, or repo-qualified to read another checked-out repo. A
    pattern that no longer matches is itself a failure, so claims can't rot.
    """
    claims_path = repo / CLAIMS_FILE
    if not claims_path.is_file():
        return
    text = claims_path.read_text()
    try:
        claims = (yaml.safe_load(text) or {}).get("claims", [])
    except yaml.YAMLError as exc:
        report.failures.append(
            Finding("M3", name, CLAIMS_FILE, 1, f"unreadable: {exc}")
        )
        return
    for claim in claims:
        cid = claim.get("id", "?")
        line = _line_of(text, max(text.find(f"id: {cid}"), 0))
        try:
            expected = claim_source(claim["equals"], repo, repos)
            body = _read(claim["file"], repo, repos)
            matches = [
                next((g for g in m.groups() if g is not None), m.group(0))
                for m in re.finditer(claim["pattern"], body)
            ]
        except Unavailable:
            report.unchecked += 1
            continue
        except (
            ClaimError,
            KeyError,
            re.error,
            json.JSONDecodeError,
            ValueError,
        ) as exc:
            report.failures.append(
                Finding("M3", name, CLAIMS_FILE, line, f"{cid}: {exc}")
            )
            continue
        report.checked += 1
        if not matches:
            report.failures.append(
                Finding(
                    "M3",
                    name,
                    CLAIMS_FILE,
                    line,
                    f"{cid}: pattern no longer matches `{claim['file']}`",
                )
            )
        elif any(m != expected for m in matches):
            found = ", ".join(sorted(set(matches)))
            report.failures.append(
                Finding(
                    "M3",
                    name,
                    CLAIMS_FILE,
                    line,
                    f"{cid}: `{claim['file']}` says {found}, source says {expected}",
                )
            )


def run_checks(root: Path, target: str | None = None) -> Report:
    repos = find_repos(root)
    if target is not None and target not in repos:
        raise ValueError(f"repo {target!r} not found under {root}")
    report = Report()
    for name, repo in sorted(repos.items()):
        check_m1(name, repo, repos, report, target)
        if target is None or name == target:
            check_m2(name, repo, repos, report)
            check_m3(name, repo, repos, report)
            check_m4(name, repo, repos, report)
    return report


def _format(finding: Finding, style: str, level: str, location: str) -> str:
    if style == "github":
        return (
            f"::{level} file={location},line={finding.line},"
            f"title={finding.check}::{finding.repo}: {finding.message}"
        )
    return f"{finding.repo}/{finding.path}:{finding.line}: {finding.check} {finding.message}"


def _location(finding: Finding, repos: dict[str, Path], root: Path) -> str:
    """The finding's path relative to ``root``, as workflow annotations expect."""
    path = repos[finding.repo] / finding.path
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return finding.path


def run(args: argparse.Namespace) -> int:
    root = Path(args.cwd).resolve()
    report = run_checks(root, args.repo)
    repos = find_repos(root)
    for level, findings in (("error", report.failures), ("warning", report.warnings)):
        for finding in findings:
            location = _location(finding, repos, root)
            print(_format(finding, args.format, level, location))
    print(
        f"doc-check: {report.checked} checked, {len(report.failures)} failed, "
        f"{len(report.warnings)} warnings, {report.unchecked} unchecked "
        "(repo not checked out)"
    )
    return 1 if report.failures else 0
