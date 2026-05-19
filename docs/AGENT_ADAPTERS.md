# Agent Adapter Map

Last checked against upstream docs: 2026-05-19.

Canonical Heddle agent material lives in this repository:

- `skills/<name>/SKILL.md`
- `agents/<name>.md`
- `AGENTS.md`
- `anchors/`

Agent-specific files created by `workspace agent-adapters install` are
adapters. They should symlink to canonical files or contain only a small
pointer to them.

The installer is intentionally conservative: it creates missing files,
updates existing symlinks that point somewhere else, and skips existing
real files or directories so repo-local agent configuration is not
overwritten.

## Installed Adapters

| Agent / format | Installed path | Purpose |
|---|---|---|
| Agent Skills standard | `.agents/skills/<skill>/` | Shared project skill location used by multiple newer agents. |
| Aider | `.aider.conf.yml` | Loads `AGENTS.md` as read-only context. |
| Cline | `.cline/rules/heddle-workspace.md`, `.cline/skills/<skill>/`, `.cline/agents/<agent>.md` | Native project rules, skills, and agent definitions. |
| Claude Code | `.claude/skills/<skill>/`, `.claude/agents/<agent>.md` | Existing Claude Code discovery paths. |
| Codex | `$CODEX_HOME/skills/heddle/<skill>/` or `~/.codex/skills/heddle/<skill>/` | Global Codex skill discovery. |
| GitHub Copilot | `.github/copilot-instructions.md` | Repository-wide custom instructions, symlinked to `AGENTS.md`. |
| Cursor | `.cursor/rules/heddle-workspace.mdc` | Project rule pointer with Cursor MDC frontmatter. |
| Devin for Terminal | `.devin/skills/<skill>/` | Native project skills. |
| Gemini CLI | `GEMINI.md` | Native context file, symlinked to `AGENTS.md`. |
| Qwen Code | `QWEN.md`, `.qwen/skills/<skill>/` | Native context file and project skills. |
| Windsurf | `.windsurf/rules/heddle-workspace.md`, `.windsurf/skills/<skill>/` | Native Cascade rules and skills. |
| Zed | `.rules` | Native project rule file, symlinked to `AGENTS.md`. |

## Source Notes

- [Cursor rules](https://docs.cursor.com/en/context) live in
  `.cursor/rules` as `.mdc` files with
  frontmatter such as `description`, `globs`, and `alwaysApply`.
  Cursor also supports root `AGENTS.md` files for simpler project
  instructions.
- [Windsurf Cascade](https://docs.windsurf.com/windsurf/cascade/agents-md)
  supports `AGENTS.md`, workspace rules in
  `.windsurf/rules/*.md`, and workspace skills in
  `.windsurf/skills/<skill>/SKILL.md`.
- [Cline project configuration](https://docs.cline.bot/getting-started/config)
  uses `.cline/rules`, `.cline/skills`, and `.cline/agents`; Cline
  also recognizes `.clinerules/`,
  Cursor/Windsurf rules, and `AGENTS.md`.
- [Devin for Terminal](https://cli.devin.ai/docs/extensibility/rules)
  recommends `AGENTS.md` for rules and supports
  project skills in `.devin/skills/`, `.windsurf/skills/`, and
  `.agents/skills/`.
- [Gemini CLI](https://google-gemini.github.io/gemini-cli/docs/cli/gemini-md.html)
  loads `GEMINI.md` context files.
- [Qwen Code](https://qwenlm.github.io/qwen-code-docs/en/users/features/memory/)
  loads `QWEN.md`, reads `AGENTS.md` when present, and
  supports project skills in `.qwen/skills/`.
- [Aider](https://aider.chat/docs/config/aider_conf.html) loads
  convention files with `read:` entries in
  `.aider.conf.yml`.
- [GitHub Copilot](https://docs.github.com/en/copilot/how-tos/custom-instructions/adding-repository-custom-instructions-for-github-copilot)
  repository-wide custom instructions live at
  `.github/copilot-instructions.md`; Copilot also supports agent
  instructions through `AGENTS.md`.
- [Zed project rules](https://zed.dev/docs/ai/rules) use a root
  `.rules` file and also recognize
  compatibility names such as `AGENTS.md`, `CLAUDE.md`, and
  `GEMINI.md`.
- [Amp](https://ampcode.com/manual) reads `AGENTS.md` and supports
  native skills in `.agents/skills/`.
- [OpenCode](https://dev.opencode.ai/docs/config/) reads `AGENTS.md`,
  so no extra adapter is needed beyond the canonical workspace file.
