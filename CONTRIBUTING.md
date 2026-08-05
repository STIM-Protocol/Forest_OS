# Contributing to Forest OS

Forest OS operates under the STIM Protocol v7.0011. All contributions must comply with Layer 0 governance requirements.

## Requirements for All Contributions

1. **Declare FLOPs budget** in your task manifest before beginning work
2. **Use allowed toolsets only** — no tool calls outside your declared manifest
3. **Include Loop 1 post-mortem** on task completion (actual vs declared delta-S/J)
4. **Pass MAIM security screening** for any external write operations
5. **Human attestation required** for GitHub pushes, brain writes, and external API calls

## Brain Write Protocol

All Mycelial Brain writes MUST use sequential doc-*** format:
- Correct: `doc-164`, `doc-165`, `doc-166`
- Incorrect: `FOREST/path/file.md` (fails silently — content lost)

Always verify with brain_read immediately after brain_write.

## Style Guide (Stop Slop)

- No em dashes — use hyphens, colons, or restructure
- No passive voice
- No filler adverbs
- Direct, dense prose
- Cite sources inline

## Commit Message Format

```
[agent-name] action: description — STIM v7.0011
```

Example: `[hermes] feat: add circuit breaker to kanban sync — STIM v7.0011`

## Pull Request Process

1. Open a PR with STIM manifest attached
2. Loop 1 post-mortem must be included in PR description
3. Human review required before merge to main
4. Telegram approval loop for automated merges
