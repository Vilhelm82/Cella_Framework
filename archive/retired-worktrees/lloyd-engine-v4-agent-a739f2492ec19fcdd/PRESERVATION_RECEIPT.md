# Lloyd Engine V4 auxiliary worktree preservation receipt

- Preserved: 2026-07-15 (Australia/Sydney)
- Source repository: `/home/wlloyd/Lloyd_Engine_V4`
- Removed worktree: `/home/wlloyd/Lloyd_Engine_V4/.claude/worktrees/agent-a739f2492ec19fcdd`
- Source branch: `worktree-agent-a739f2492ec19fcdd`
- Preservation tag in source repository: `preserved/worktree-agent-a739f2492ec19fcdd-20260715`
- Commit: `5118b8ca26e20d40f6d21038c763181c38c1774e`
- Parent: `587b41c0d0e3bcb278cdb4b1ab3744ffef022f0a`
- Tree: `4dd52510050b630cbc1ca7b8aa31690c0c800822`
- Subject: `c001 three_channel_kg Stage C: gauge / single-edge battery + verdicts (CL-c4 -> DEMONSTRATED, K4 silent)`
- Unique change: 11 files, 3,395 inserted lines under `results/three_channel_kg/stage_c/`

## Portable preservation artifacts

| Artifact | Purpose | Bytes | SHA-256 |
|---|---|---:|---|
| `0001-c001-three_channel_kg-Stage-C-gauge-single-edge-batt.patch` | Git-format patch preserving the commit metadata and complete delta | 247,040 | `d1328041c0c3849311053574298c8f4623ca9d82981d57b1cccc76edb06a8016` |
| `stage-c-artifacts-5118b8c.tar.gz` | Exact committed snapshot of the 11 Stage-C artifacts | 51,225 | `cd667c848e5c34edf79aba2fe631b9a19eebd41531ab24fe37674d73eb88d005` |

The patch can be restored with `git am <patch-file>` onto a repository containing the parent history. The snapshot is independent of Git history and can be extracted with `tar -xzf <snapshot-file>`.

The auxiliary checkout was clean before removal. The original branch and annotated preservation tag remain in the source repository; the two portable artifacts above survive retirement of that repository.
