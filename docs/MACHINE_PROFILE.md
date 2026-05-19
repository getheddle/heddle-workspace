# Machine profile — per-machine capabilities and overrides

A workspace can be synced across several machines (work PC, home PC,
laptop, a teammate's box). Most files in the workspace are identical
across machines — that's the whole point of syncing. A small set are
*not*: which optional tools are installed, which VMs or mounts exist,
which paths point where. This doc defines how we express those
differences without polluting the synced tree.

## The rule

Per-machine state lives in **one untracked file** at the workspace
root:

```
(local-only)/machine.yaml
```

It is read by skills and agents that need to know what's available on
this machine. It is **never** committed (the `(local-only)/` carve-out
is gitignored — see [`anchors/WORKSPACE.md`](../anchors/WORKSPACE.md)).

If the file is absent, agents assume "nothing special, no extra
capabilities" and proceed in the safe-default mode.

## Schema

```yaml
# (local-only)/machine.yaml — describes THIS machine only.

machine:
  name: <short label, e.g. "work-pc", "home-pc", "macbook">
  os: <macos | linux | windows>            # informational; agents may key off this
  notes: <free text, optional>             # one line, human-only

# Capabilities the machine offers. Keys are well-known names; values are
# either bool (present / not present) or a small struct when detail is
# needed. Skills that depend on a capability MUST gracefully degrade
# when it is absent or false.
capabilities:
  hyperv: false
  docker: true
  gpu: false
  samba_lab: false
  # add more as skills start needing them; document each new key here.

# Path overrides. Use when a synced config wants to refer to a location
# that legitimately differs per machine (large datasets, VM stores,
# external mounts). Keys are stable names; values are absolute paths
# on THIS machine.
paths:
  # vm_store: /Volumes/VMs
  # dataset_root: /mnt/data/heddle
```

All three top-level keys are optional, but `machine.name` is strongly
recommended — agents print it back to the user so the human knows
which profile is active.

## Well-known capability keys

Start narrow. Add a key here only when a skill actually consumes it.

| Key | Meaning | Consumed by |
|---|---|---|
| `hyperv` | Hyper-V available for the Samba lab scenarios | `devops-troubleshooter`, lab helpers |
| `docker` | A working Docker / Podman daemon | preflight, integration tests |
| `gpu` | Local GPU usable by LLM workers | LLM worker bring-up |
| `samba_lab` | Full Samba AD lab can run here | lab scenarios |

Adding a new key: document it in this table in the same PR that
teaches a skill to read it. Skills that read an undocumented key
should treat it as `false` rather than erroring.

## How skills should consume it

- Read `(local-only)/machine.yaml` from the workspace root (detected
  per `anchors/WORKSPACE.md`).
- Missing file, missing key, or `false` value → the capability is
  unavailable. Say so out loud ("Hyper-V lab not available on this
  machine — skipping live join, running schema check only") and
  proceed with whatever subset still works.
- Never auto-write to this file. If a capability looks like it
  *should* be available but the manifest says otherwise, surface it
  and let the user edit.

## What this is NOT

- **Not an OS-portability layer.** If a script is bash-only and the
  teammate is on Windows, the right answer is "this script doesn't
  run there yet," not a synthetic capability flag that pretends it
  does. We surface differences; we do not paper over them.
- **Not a secrets store.** Secrets belong in the system keychain or
  a per-machine secrets file alongside this one in `(local-only)/`.
  `machine.yaml` is plain config the user can hand-edit.
- **Not a replacement for a setup doc.** Substantially different
  environments (a new teammate on a different OS, a fresh GPU box)
  still need their own onboarding notes. The profile records the
  outcome of that setup; it doesn't perform it.

## Bootstrapping a new machine

1. Sync the workspace as usual.
2. Run `bin/workspace machine init` (or just run `/heddle-orient` —
   it will invoke this automatically when no profile is present).
   The command writes `(local-only)/machine.yaml` with `machine.name`,
   `machine.os`, and detectable capabilities (e.g. `docker`)
   pre-filled from the local shell. It is idempotent: a second run
   on a machine that already has the file reports "already present"
   and exits 0. Use `--force` to regenerate.
3. Open the file and flip the remaining capabilities to `true` only
   after you've verified they actually work on this machine.
4. Run `/heddle-orient` again — it should echo your `machine.name`
   and capability list back to you. That confirms the file is being
   read.
5. As you discover more capabilities (or lose them), edit the file.
   Nothing else syncs or auto-detects.

## Ceiling — when to stop using this

This file works well when machines differ in *which tools are
installed* and *where things live*. It does not scale to:

- Cross-OS command differences (use OS-specific scripts in their own
  directories instead, gated by `machine.os`).
- Multi-user shared infrastructure (use a real config-management
  tool, not a workspace file).
- Anything that needs to be true *before* the workspace is cloned
  (chicken-and-egg — handle in the machine's setup doc).

When you hit one of those, write it up rather than stretching the
schema.
