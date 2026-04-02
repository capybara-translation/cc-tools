# Claude Code Statusline Command

A shell script that displays the current working directory, project directory, and Git branch name in the Claude Code statusline.

## Example Output

```
cwd: ~/repos/my-project  |  project: ~/repos/my-project  |  branch: main
```

The branch section is omitted outside of a Git repository.

## How It Works

Claude Code passes JSON (containing `workspace.current_dir`, `workspace.project_dir`, etc.) via stdin. This script parses it with `jq` and returns a formatted string to stdout.

## Prerequisites

- `jq`
- `git`

## Installation

Add the following to your Claude Code settings file (e.g., `~/.claude/settings.json`).

```json
{
  "statusline": {
    "command": "/path/to/statusline-command.sh"
  }
}
```

Replace `/path/to/` with the actual path.

## License

[MIT](../LICENSE)
