# Contributing to Forest OS

Forest OS operates under the STIM Protocol v7.0010. All contributions must comply with Layer 0 governance requirements.

## Requirements for All Contributions

1. **Declare FLOPs budget** in your task manifest before beginning work
2. **Use allowed toolsets only** — no tool calls outside your declared manifest
3. **Include Loop 1 post-mortem** on task completion (actual vs declared ΔS/J)
4. **Pass MAIM security screening** for any external write operations
5. **Human attestation required** for GitHub pushes, brain writes, and external API calls

## Brain Write Protocol

All Mycelial Brain writes MUST use sequential doc-*** format:
- ✅ `doc-164`, `doc-165`, `doc-166`
- ❌ `GARDEN/path/file.md` (fails silently — content lost)

Always verify with brain_read immediately after brain_write.

## Commit Message Format

```
[agent-name] action: description — STIM v7.0010
```

Example: `[hermes] feat: add circuit breaker to kanban sync — STIM v7.0010`

## Pull Request Process

1. Open a PR with STIM manifest attached
2. Loop 1 post-mortem must be included in PR description
3. Human review required before merge to main
4. Telegram approval loop for automated merges
