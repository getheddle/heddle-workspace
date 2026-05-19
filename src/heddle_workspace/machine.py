"""`workspace machine init` — create an annotated per-machine profile.

Writes `(local-only)/machine.yaml` if it doesn't already exist, pre-filling
the fields that can be reliably detected from the local shell (machine name,
OS, presence of common tools). Idempotent: a second invocation reports the
existing file and exits 0, so skills can call it blindly. See
`heddle-workspace/docs/MACHINE_PROFILE.md` for the schema.
"""

from __future__ import annotations

import argparse
import platform
import shutil
import socket
from pathlib import Path

from heddle_workspace.manifest import LOCAL_ONLY_DIR

MACHINE_FILENAME = "machine.yaml"


def _detect_os() -> str:
    s = platform.system().lower()
    if s == "darwin":
        return "macos"
    if s in ("linux", "windows"):
        return s
    return s or "unknown"


def _detect_name() -> str:
    try:
        return socket.gethostname().split(".", 1)[0] or "unknown"
    except Exception:
        return "unknown"


def _has(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def render(name: str, os_name: str, docker: bool) -> str:
    docker_v = "true " if docker else "false"
    return f"""\
# (local-only)/machine.yaml — per-machine profile for THIS computer.
# Untracked; never synced across machines. Edit freely. See
# heddle-workspace/docs/MACHINE_PROFILE.md for the schema and the list
# of well-known capability keys.

machine:
  name: {name}
  os: {os_name}
  # notes: free text, one line

# Capabilities offered by this machine. Auto-detection sets only the
# obvious ones; flip the others to `true` once you've verified they work.
# Skills MUST degrade gracefully when a capability is absent or false.
capabilities:
  docker: {docker_v}     # detected: `docker` in PATH
  hyperv: false     # Windows + Hyper-V role; Samba lab depends on this
  gpu: false        # usable local GPU for LLM workers
  samba_lab: false  # full Samba AD lab can run here

# Path overrides. Uncomment and set absolute paths when a synced config
# refers to something that legitimately differs per machine.
# paths:
#   vm_store: /Volumes/VMs
#   dataset_root: /mnt/data/heddle
"""


def run(args: argparse.Namespace) -> int:
    root: Path = args.cwd.resolve()
    target = root / LOCAL_ONLY_DIR / MACHINE_FILENAME
    if target.exists() and not args.force:
        print(f"machine profile already present: {target}")
        return 0

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render(_detect_name(), _detect_os(), _has("docker")))
    verb = "rewrote" if args.force else "wrote"
    print(f"{verb} {target}")
    print("Review and adjust capabilities as needed.")
    return 0
