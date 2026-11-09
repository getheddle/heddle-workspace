---
name: heddle-contract-sync
description: Verify or update the schema and fixture sync between heddle (upstream source of truth) and heddle-sdk (vendored copies). Use whenever a change touches heddle.core.envelope, heddle.core.messages, heddle.core.wire_json, schemas/v1/* (schemas or fixtures), an SDK Wire.* or Models.* codec (.NET, Swift, JVM), or NATS subject conventions — or when you suspect downstream is behind upstream.
---

# /heddle-contract-sync — keep heddle and heddle-sdk in lockstep

The wire-protocol source of truth is the `heddle` repo: the
`WireEnvelope` frame (`heddle.core.envelope`), the body models
(`heddle.core.messages`), and the strict text decoder
(`heddle.core.wire_json`, the two I-JSON rules). Schemas and the
conformance fixtures in `schemas/v1/fixtures/` flow outward via
`heddle-sdk/tools/sync_schemas.py`. Everything else is downstream. The
schemas are the interchange format; the fixtures are the behavioral
contract every SDK must pass.

This skill assumes both `heddle/` and `heddle-sdk/` are checked out as
siblings — the workspace layout. See
`heddle-workspace/anchors/WORKSPACE.md`. Run from the workspace
root or from inside either sibling; the skill changes directory as
needed. If `heddle-sdk/` is not checked out, the skill cannot run —
ask the user to clone it as a sibling.

## When to invoke

- After editing `heddle/src/heddle/core/envelope.py`,
  `messages.py` or `wire_json.py`.
- After regenerating `heddle/schemas/v1/*.schema.json` or changing a
  fixture in `heddle/schemas/v1/fixtures/`.
- After changing NATS subject names, queue group names, or contract
  envelope fields anywhere.
- Before merging a PR that touches any of the above.
- When a `heddle-sdk` test fails with a schema mismatch and you're not
  sure whether upstream is ahead or downstream forgot to sync.

## Workflow

### Step 1 — verify

From `heddle-sdk/`:

```bash
python tools/sync_schemas.py --check
```

Three outcomes:

- **OK** — vendored manifest matches upstream commit; no sync needed.
- **Behind upstream** — heddle has changed; downstream needs the update.
- **Manifest broken** — local edits to `heddle-sdk/schemas/v1/*` or the
  manifest itself. This is a violation of invariant C1. Investigate
  before syncing.

### Step 2 — sync (only if behind)

From `heddle-sdk/`, with a local heddle checkout adjacent:

```bash
python tools/sync_schemas.py --update --upstream ../heddle
```

This copies `schemas/v1/*.schema.json` and `schemas/v1/fixtures/` from
upstream, updates `schemas/manifest.json` with the upstream commit hash +
file hashes, and reports what changed. To compare against a local
upstream checkout without updating, run
`python tools/sync_schemas.py --check-upstream --upstream ../heddle`.

### Step 3 — propagate to the language codecs

Vendored schemas and fixtures update automatically. The language codecs
are written by hand and held to the fixtures by tests:

| SDK | Frame codec | Bodies |
|---|---|---|
| .NET | `dotnet/src/Heddle.Sdk/Wire.cs` | `dotnet/src/Heddle.Sdk/Models.cs` |
| Swift | `swift/Sources/HeddleActor/Wire.swift` | `swift/Sources/HeddleActor/Models.swift` |
| JVM | `jvm/core/src/main/kotlin/heddle/sdk/Wire.kt` | `jvm/core/src/main/kotlin/heddle/sdk/Models.kt` |

After a sync, run every SDK's tests; each runs all vendored fixtures:

```bash
cd heddle-sdk
dotnet test dotnet/tests/Heddle.Sdk.Tests/Heddle.Sdk.Tests.csproj
swift test --package-path swift
./jvm/gradlew -p jvm test
```

If any fails, update that SDK's codec by hand to match, then re-run.
Aim for **language parity** (invariant C6): a change in one SDK lands in
all three unless explicitly documented as language-specific.

### Step 4 — propagate subject changes (if any)

Subject names and queue-group names are not in the JSON Schema files;
they live in code. If your upstream change touched subjects:

- Update `dotnet/src/Heddle.Sdk/Subjects.cs`.
- Update `swift/Sources/HeddleActor/Subjects.swift`.
- Update the subject builders in
  `jvm/core/src/main/kotlin/heddle/sdk/Transport.kt`.
- Update `heddle-workspace/anchors/CONTRACT_MAP.md` if it's a new
  subject.
- Update `heddle/docs/ARCHITECTURE.md` NATS-subjects table.

## What to verify before committing

```bash
# in heddle-sdk:
python tools/sync_schemas.py --check        # must say OK
dotnet build dotnet/src/Heddle.Sdk/Heddle.Sdk.csproj
dotnet test dotnet/tests/Heddle.Sdk.Tests/Heddle.Sdk.Tests.csproj
swift build --package-path swift
swift test --package-path swift
swift build --package-path swift-nats
./jvm/gradlew -p jvm build
```

If the change adds a *new* subject or field, also confirm:

- `heddle/docs/foreign-actors.md` documents it (heddle side).
- An example in `heddle-sdk/examples/` exercises it, or there's a test
  in `dotnet/tests/`, `swift/Tests/` and `jvm/core/src/test/` that does.

## Output format

```
Sync check: <OK | behind | broken>
Upstream commit: <sha or "n/a">
Action taken: <none | --update run | manual edits applied>
Tests run: <list>
Result: <pass | fail with summary>
```

If anything fails, do not commit. Report to the user and ask for direction.
