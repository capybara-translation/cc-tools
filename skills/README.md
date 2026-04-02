# Claude Code Skills

A collection of custom skills for Claude Code.

## Skills

| Skill | Command | Description |
|-------|---------|-------------|
| [commit-msg](./commit-msg/SKILL.md) | `/commit-msg` | Generate a commit message in Japanese from staged/unstaged changes and copy to clipboard |
| [commit-msg-en](./commit-msg-en/SKILL.md) | `/commit-msg-en` | Generate a commit message in English from staged/unstaged changes and copy to clipboard |
| [code-review](./code-review/SKILL.md) | `/code-review [branch]` | Review code changes in a separate context with structured feedback in Japanese |
| [code-review-en](./code-review-en/SKILL.md) | `/code-review-en [branch]` | Review code changes in a separate context with structured feedback in English |

## Installation

Copy skill directories to `~/.claude/skills/`:

```bash
cp -r commit-msg ~/.claude/skills/
cp -r commit-msg-en ~/.claude/skills/
cp -r code-review ~/.claude/skills/
cp -r code-review-en ~/.claude/skills/
```

## License

[MIT](../LICENSE)
