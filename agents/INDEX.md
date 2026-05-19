# Heddle Subagents Index

Canonical subagent definitions live in this directory. Claude Code can
discover them through `.claude/agents` symlinks; other agents should read
the relevant file on demand when they support delegated review or
planning roles.

| Subagent | Use |
|---|---|
| [`heddle-architect`](heddle-architect.md) | Read-only design consultant before non-trivial implementation. |
| [`heddle-invariant-guard`](heddle-invariant-guard.md) | Diff reviewer for structural invariant violations. |
| [`heddle-contract-reviewer`](heddle-contract-reviewer.md) | Cross-repo wire-protocol and schema coherence reviewer. |
| [`mkdocs-doc-reviewer`](mkdocs-doc-reviewer.md) | Read-only reviewer for MkDocs documentation changes. |
| [`pyproject-deps-reviewer`](pyproject-deps-reviewer.md) | Read-only reviewer for Python dependency and lockfile changes. |

Install adapters from a workspace root:

```bash
./heddle-workspace/bin/install-agent-adapters --workspace .
```
