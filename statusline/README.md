# Claude Code Statusline Command

Claude Code のステータスライン（画面下部）に、現在の作業ディレクトリ・プロジェクトディレクトリ・Git ブランチ名を表示するシェルスクリプトです。

## 表示例

```
cwd: ~/repos/my-project  |  project: ~/repos/my-project  |  branch: main
```

Git リポジトリ外では branch 部分が省略されます。

## 仕組み

Claude Code は標準入力に JSON（`workspace.current_dir`, `workspace.project_dir` など）を渡します。このスクリプトはそれを `jq` で解析し、整形した文字列を `stdout` に返します。

## 前提条件

- `jq`
- `git`

## インストール

1. スクリプトに実行権限を付与します。

```bash
chmod +x statusline-command.sh
```

2. Claude Code の設定ファイル（`~/.claude/settings.json` など）に以下を追加します。

```json
{
  "statusline": {
    "command": "/path/to/statusline-command.sh"
  }
}
```

`/path/to/` は実際のパスに置き換えてください。

## License

[MIT](../LICENSE)
