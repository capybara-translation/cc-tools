# Claude Code Skills

A collection of custom skills for Claude Code.

## Skills

| Skill | Command | Description |
|-------|---------|-------------|
| [commit-msg](./commit-msg/SKILL.md) | `/commit-msg` | Generate a commit message in Japanese from staged/unstaged changes and copy to clipboard |
| [commit-msg-en](./commit-msg-en/SKILL.md) | `/commit-msg-en` | Generate a commit message in English from staged/unstaged changes and copy to clipboard |
| [code-review](./code-review/SKILL.md) | `/code-review [branch]` | Review code changes in a separate context with structured feedback in Japanese |
| [code-review-en](./code-review-en/SKILL.md) | `/code-review-en [branch]` | Review code changes in a separate context with structured feedback in English |
| [code-review-debate](./code-review-debate/SKILL.md) | `/code-review-debate [branch]` | Iteratively review code via an adversarial discussion between independent reviewer and implementer subagents until a conclusion is reached (Japanese) |
| [code-review-debate-en](./code-review-debate-en/SKILL.md) | `/code-review-debate-en [branch]` | Iteratively review code via an adversarial discussion between independent reviewer and implementer subagents until a conclusion is reached (English) |
| [explain-changes](./explain-changes/SKILL.md) | `/explain-changes [scope]` | Explain applied code changes ordered by importance, with prose plus representative code snippets (Japanese). Scope = base branch, git range, or PR number |
| [explain-changes-en](./explain-changes-en/SKILL.md) | `/explain-changes-en [scope]` | Explain applied code changes ordered by importance, with prose plus representative code snippets (English). Scope = base branch, git range, or PR number |
| [session-id](./session-id/SKILL.md) | `/session-id` | Display the current Claude Code session ID (UUID used by `claude --resume`); useful in the desktop app, which has no status line |

## Installation

Symlink the skill directories into `~/.claude/skills/` so edits in this repo are
picked up without re-copying. Run from this `skills/` directory:

```bash
for s in commit-msg commit-msg-en \
         code-review code-review-en \
         code-review-debate code-review-debate-en \
         explain-changes explain-changes-en \
         session-id; do
  ln -sfn "$PWD/$s" ~/.claude/skills/"$s"
done
```

After (re)installing, run `/reload-skills` in Claude Code to refresh the list.

## License

[MIT](../LICENSE)
