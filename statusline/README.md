# Claude Code Statusline Command

A shell script that displays project info, session ID, Git branch, model name, and context usage in the Claude Code statusline.

## Example Output

```
project: ~/repos/my-project  |  cwd: ~/repos/my-project  |  session: abc123...
branch: main  |  Opus  |  ctx: 8%
```

- Line 1: project directory, current working directory, and session ID
- Line 2: Git branch, model display name, and context window usage percentage

Each field is omitted when its value is not available.

## How It Works

Claude Code passes JSON (containing `workspace.current_dir`, `workspace.project_dir`, `session_id`, `model.display_name`, `context_window.used_percentage`, etc.) via stdin. This script parses it with `jq` and returns a two-line formatted string to stdout.

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
