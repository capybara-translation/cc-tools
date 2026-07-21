---
name: commit-msg
description: Generate a commit message from staged/unstaged changes since the last commit and copy it to the clipboard.
disable-model-invocation: true
---

## Context: Current Git Changes

### Recent commit history (for style reference)
!`git log --oneline -10 2>/dev/null || echo "No git history found"`

### Staged changes
!`git diff --cached --stat 2>/dev/null || echo "No staged changes"`

### Unstaged changes
!`git diff --stat 2>/dev/null || echo "No unstaged changes"`

### Detailed diff (staged + unstaged)
!`git diff HEAD 2>/dev/null || git diff 2>/dev/null || echo "No changes detected"`

## Your Task

0. コミット履歴に「No git history found」と表示されている場合、gitリポジトリが未初期化または初回コミット前の状態である。この場合は `git init && git add .` を実行し、`git diff --cached --stat` と `git diff --cached` で差分を再取得してから次のステップに進む。
1. 上記のdiffと直近のコミット履歴を分析し、プロジェクトのコミットメッセージのスタイルを把握する。
2. 以下のルールに従い、簡潔で構造化されたコミットメッセージを生成する:
   - Conventional Commits形式を使用: `type(scope): 説明`
   - Types: feat, fix, refactor, docs, test, chore, style, perf, ci, build
   - **説明部分は必ず日本語で記述すること**（例: `feat(auth): ログイン画面にOAuth認証を追加`）
   - ライブラリ名、API名、技術用語など英語が自然なものはそのまま英語で可だが、文の主体は日本語とする
   - サブジェクト行は72文字以内に収める
   - 必要に応じて空行の後にbodyを箇条書きで追加し「なぜ」を説明する
   - **サブジェクト行および各箇条書き項目は1行で記述すること**（途中で改行を入れない。改行はサブジェクトとbodyの区切り、および各箇条書き項目の区切りのみに使う）
   - 既存のコミット履歴のスタイルがあればそれに合わせる
   - **「Co-Authored-By」行は絶対に含めないこと**
3. コミットメッセージをコードブロックで提示する。
4. **クリップボードにコピーする**。UTF-8 + LF を保持したまま GUI クリップボードへ入れること。以下の 2 手順で行う:
   1. メッセージを一時ファイルへ**そのままのバイト列 (LF 改行)** で書き出す。Write ツールが使えるならそれで書き出すのが最も確実。シェルのみで行う場合は変数展開・エスケープを避けるため quoted heredoc を使う (末尾に改行が 1 つ付くが git が除去するため無害):
      ```sh
      cat > "${TMPDIR:-/tmp}/claude-commit-msg.txt" <<'COMMIT_MSG_EOF'
      <コミットメッセージ本文をそのまま>
      COMMIT_MSG_EOF
      ```
   2. その一時ファイルを UTF-8 として読み、GUI クリップボードへセットする (CLI 版・デスクトップ版の両方で動作する):
      ```sh
      osascript -e 'set the clipboard to (read POSIX file "'"${TMPDIR:-/tmp}/claude-commit-msg.txt"'" as «class utf8»)'
      ```
   - **`pbcopy` と `do shell script "cat …"` は使わないこと**。デスクトップ版 Claude Code は Bash が GUI(Aqua) セッションから切り離されているため `pbcopy` は GUI クリップボードに届かず、`osascript` の `do shell script` は改行を LF→CR に変換してサブジェクト/body の `\n\n` 境界を壊す (GUI Git クライアントの Title/Description 自動分割が失敗する)。
   - 改行はサブジェクトと body の区切り (空行) および各箇条書き項目の区切りのみとし、センテンスや箇条書き項目の途中では改行しないこと。
5. クリップボードにコピー済みであることをユーザーに伝える。

変更が検出されない場合は、コミットする変更がないことをユーザーに伝える。
