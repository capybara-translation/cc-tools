# Claude Code Hooks

Scripts to use as Claude Code hooks.

## Scripts

| Script | Description |
|--------|-------------|
| [notify.sh](./notify.sh) | Play a sound and show a macOS desktop notification |
| [protect_sensitive_files.py](./protect_sensitive_files.py) | PreToolUse hook: block Read/Edit/Write on files matching `Read(...)` deny rules in `~/.claude/settings.json` |
| [require_issue_links.py](./require_issue_links.py) | Stop hook: make Claude rewrite GitHub issue/PR mentions that are not links |

## protect_sensitive_files.py

A `PreToolUse` hook for `Read|Edit|MultiEdit|Write`. It reads the `Read(...)` rules under `permissions.deny` in `~/.claude/settings.json` and blocks the tool (exit code 2) when `tool_input.file_path` matches one of them.

```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Read|Edit|MultiEdit|Write", "hooks": [ { "type": "command", "command": "/path/to/hooks/protect_sensitive_files.py" } ] }
    ]
  }
}
```

## require_issue_links.py

A `Stop` hook. It checks Claude's last reply for bare issue/PR references (`#123`, `owner/repo#123`, `PR 123`, `Issue #7`), ignoring code blocks, inline code, Markdown links and URLs. If any are found, it blocks the stop once and asks Claude to restate those sentences with Markdown links to the full URL. The reason includes the current repository from `git remote get-url origin` as a hint.

It blocks at most once per reply (`stop_hook_active`), so it cannot loop. The text already shown is not removed; the corrected sentences follow it.

```json
{
  "hooks": {
    "Stop": [
      { "hooks": [ { "type": "command", "command": "/path/to/hooks/require_issue_links.py" } ] }
    ]
  }
}
```

## notify.sh

Plays a system sound (`Glass.aiff`) and displays a macOS notification via `osascript`.

```bash
./notify.sh "Title" "Body message"
```

### Changing the sound

Replace the sound file path in `notify.sh` with any file under `/System/Library/Sounds/`:

- `Glass.aiff` (default)
- `Ping.aiff`
- `Pop.aiff`
- `Tink.aiff`
- `Basso.aiff`

## Installation

Add hooks to your Claude Code settings file (`~/.claude/settings.json`):

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/hooks/notify.sh 'Claude Code' 'Response complete'"
          }
        ]
      }
    ],
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/hooks/notify.sh 'Claude Code' 'Notification'"
          }
        ]
      }
    ]
  }
}
```

Replace `/path/to/` with the actual path.

## License

[MIT](../LICENSE)
