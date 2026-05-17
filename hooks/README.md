# hooks/ — Heddle-family Claude Code hook templates

Claude Code hooks run shell commands in response to tool events (Edit,
Write, etc.). This directory holds **templates** you can merge into a
workspace or repo's `.claude/settings.json`. The toolkit does not
auto-install hooks — they're opt-in, because hooks run on every
matching tool call and the right set depends on what's checked out.

## What's here

### `settings.template.json`

Two hooks tuned to a Heddle workspace:

| Hook | When it fires | What it does |
|---|---|---|
| `PostToolUse` on Edit/Write/MultiEdit | After a Python file under any `heddle/src/` or `heddle/tests/` tree is edited | Runs `uv run ruff check --fix --quiet` on the file. Output is truncated to 20 lines. |
| `PreToolUse` on Edit/Write/MultiEdit | Before a file under `heddle/schemas/v1/`, `heddle-sdk/.../Models/` is edited | Emits a stderr reminder to run `/heddle-contract-sync` and consider `/cross-repo-pr`. Non-blocking. |

Both hooks exit 0 on the non-matching path so unrelated edits aren't
affected.

## Installing

Two options.

### Option A — start fresh in a target without `.claude/settings.json`

```bash
./install.sh --hooks <target>
```

This copies `settings.template.json` to `<target>/.claude/settings.json`
**only if no settings file exists yet**. It will not overwrite. Re-run
without `--hooks` to add toolkit symlinks separately.

### Option B — merge into an existing `settings.json`

`install.sh` deliberately does not merge JSON (too fragile). Copy the
`hooks:` block from `settings.template.json` into your existing
`settings.json` by hand. If your file already has a `hooks:` key, merge
arrays rather than replacing.

## Tuning

The matchers in the template assume a workspace layout where `heddle/`
and `heddle-sdk/` are immediate children of the workspace root. If
your layout differs (e.g. heddle is a submodule), edit the `case`
patterns in the hook commands.

If you find a hook noisy in practice, change `PostToolUse` to
`SessionEnd` for the ruff hook so it only runs at session boundaries.

## What this template is NOT

- Not a substitute for `/heddle-preflight`. Hooks are fast feedback;
  preflight is the comprehensive pre-commit check.
- Not a place to put repo-secret-bearing commands. Anything in
  `settings.json` is committed (or symlinked) and visible to anyone
  with read access.
