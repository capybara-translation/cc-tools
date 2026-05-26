# Claude Code Statusline Command

A shell script that displays project info, session ID, working directory, Git branch, model name, reasoning effort, context usage, rate-limit usage, and the current open PR in the Claude Code statusline.

## Example Output

```
project: ~/repos/my-project
session: abc123...
cwd: ~/repos/my-project
branch: main
model: Opus 4.7  |  effort: high  |  ctx: 8%  |  5h: 42%  |  7d: 12%
PR #123 (approved)
```

- Lines 1-4: project directory, session ID, current working directory, and Git branch — each on its own line
- Line 5: model display name, reasoning effort level, context-window usage %, and rate-limit usage % for the 5-hour and 7-day windows
- Line 6 (conditional): open PR number and review state, only when a PR is associated with the current branch

Each field is omitted when its value is not available. Notable conditional fields:

- `effort` — hidden for models that do not support the reasoning-effort parameter
- `5h` / `7d` — provided only for Claude.ai Pro/Max sessions, and only after the first API response
- `PR #...` — present only when an open PR exists for the current branch

## How It Works

Claude Code passes JSON (containing `workspace.current_dir`, `workspace.project_dir`, `session_id`, `model.display_name`, `effort.level`, `context_window.used_percentage`, `rate_limits.five_hour.used_percentage`, `rate_limits.seven_day.used_percentage`, `pr.number`, `pr.review_state`, etc.) via stdin. This script parses it with `jq` and returns a formatted multi-line string to stdout.

## Prerequisites

- `jq`
- `git`

## Installation

Add the following to your Claude Code settings file (e.g., `~/.claude/settings.json`).

```json
{
  "statusLine": {
    "type": "command",
    "command": "/path/to/statusline-command.sh"
  }
}
```

Replace `/path/to/` with the actual path.

## License

[MIT](../LICENSE)
