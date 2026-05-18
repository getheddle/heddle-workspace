"""Interactive wizard for `workspace init`.

Falls back to plain `input()` if `questionary` isn't importable for any reason
(e.g. running with --non-interactive shouldn't reach here at all, but the
fallback keeps the tool usable in odd terminals).
"""

from __future__ import annotations

from pathlib import Path

from heddle_workspace.manifest import RepoEntry

try:
    import questionary  # type: ignore[import-not-found]

    _HAS_QUESTIONARY = True
except ImportError:  # pragma: no cover — only on stripped installs
    _HAS_QUESTIONARY = False


def run_init_wizard(
    root: Path,
    detected: list[tuple[Path, str, str]],
    default_name: str,
    default_project_org: str | None,
) -> tuple[str, str | None, str | None, list[RepoEntry]]:
    """Walk the user through bootstrapping a workspace umbrella.

    Returns (name, description, umbrella_remote, repos).
    """
    print(f"Bootstrapping a Heddle workspace at: {root}")
    print(f"Detected {len(detected)} child git repo(s) with remotes.")
    print()

    name = _ask_text(
        "Workspace name (also the GitHub repo name for the umbrella):",
        default=default_name,
    )
    description = _ask_text("One-line description (optional):", default="")
    description = description.strip() or None

    project_org = _ask_text(
        "GitHub org/user that will host the umbrella (e.g. IranTransitionProject):",
        default=default_project_org or "",
    ).strip()
    if project_org:
        umbrella_remote = f"git@github.com:{project_org}/{name}.git"
        print(f"  → umbrella will live at: {umbrella_remote}")
    else:
        umbrella_remote = None
        print("  → no umbrella remote configured; you can add one later with `git remote add`.")
    print()

    # Pick which detected repos to include in the manifest.
    if not detected:
        print("No child repos detected at the workspace root. The manifest will be empty;")
        print("use `workspace add <path>` later for each repo you want tracked.")
        return name, description, umbrella_remote, []

    print("Which of the detected child repos should the manifest track?")
    print("(Anything you exclude can be re-added later or moved into (local-only)/.)")
    choices = [
        {
            "name": f"{p.name:30}  ←  {r}  ({b})",
            "value": idx,
            "checked": True,
        }
        for idx, (p, r, b) in enumerate(detected)
    ]
    selected = _ask_checkbox("Select repos to include:", choices)
    repos = [
        RepoEntry(path=detected[i][0].name, remote=detected[i][1], branch=detected[i][2])
        for i in selected
    ]
    print(f"  → {len(repos)} repo(s) will be in the manifest.")
    print()

    return name, description, umbrella_remote, repos


def _ask_text(prompt: str, default: str = "") -> str:
    if _HAS_QUESTIONARY:
        ans = questionary.text(prompt, default=default).ask()
        if ans is None:
            raise KeyboardInterrupt
        return ans
    suffix = f" [{default}]" if default else ""
    raw = input(f"{prompt}{suffix} ").strip()
    return raw or default


def _ask_checkbox(prompt: str, choices: list[dict]) -> list[int]:
    if _HAS_QUESTIONARY:
        items = [
            questionary.Choice(c["name"], value=c["value"], checked=c["checked"])
            for c in choices
        ]
        ans = questionary.checkbox(prompt, choices=items).ask()
        if ans is None:
            raise KeyboardInterrupt
        return ans
    print(prompt)
    for c in choices:
        print(f"  [{'x' if c['checked'] else ' '}] {c['value']}: {c['name']}")
    raw = input(
        "Enter comma-separated indexes to INCLUDE (default: all): "
    ).strip()
    if not raw:
        return [c["value"] for c in choices]
    try:
        return [int(x.strip()) for x in raw.split(",") if x.strip()]
    except ValueError as e:
        raise ValueError("expected comma-separated integers") from e
