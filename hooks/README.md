# Claude Code Hooks

Shell scripts to use as Claude Code hooks for notifications and alerts.

## Scripts

| Script | Description |
|--------|-------------|
| [notify.sh](./notify.sh) | Play a sound and show a macOS desktop notification |

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
