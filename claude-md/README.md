# Claude Code Global Memory

The global `CLAUDE.md` (user-level memory) that Claude Code loads for every
project, version-controlled here.

## Files

| File | Installed as | Description |
|------|--------------|-------------|
| [CLAUDE.global.md](./CLAUDE.global.md) | `~/.claude/CLAUDE.md` | Global instructions applied to all projects |

### Why `CLAUDE.global.md` and not `CLAUDE.md`?

A file literally named `CLAUDE.md` inside this repository would be picked up by
Claude Code as *project* memory whenever files in this directory are read, so the
same instructions would be loaded twice. The `.global` suffix avoids that and
makes the scope obvious to anyone browsing the repo. The symlink renames it at
install time, so Claude Code still sees `~/.claude/CLAUDE.md`.

## Installation

Symlink it into `~/.claude/` so edits in this repo take effect without copying.
Run from this `claude-md/` directory:

```bash
ln -sfn "$PWD/CLAUDE.global.md" ~/.claude/CLAUDE.md
```

If `~/.claude/CLAUDE.md` already exists as a regular file, back it up first —
`ln -sfn` overwrites it without warning:

```bash
cp -p ~/.claude/CLAUDE.md ~/.claude/CLAUDE.md.bak
```

Verify the link, then start a new Claude Code session (memory is read at session
start, so a running session keeps the old content):

```bash
ls -l ~/.claude/CLAUDE.md
```

## Notes

- The file is loaded for **every** project on this machine. Keep it free of
  project-specific rules and of anything secret — this repository is shared.
- Project-specific instructions belong in that project's own `CLAUDE.md`, not
  here.

## License

[MIT](../LICENSE)
