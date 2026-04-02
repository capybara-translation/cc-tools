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
   - 既存のコミット履歴のスタイルがあればそれに合わせる
   - **「Co-Authored-By」行は絶対に含めないこと**
3. コミットメッセージをコードブロックで提示する。
4. **即座にクリップボードにコピーする**: `printf '%s' "<message>" | pbcopy` を実行する。
5. クリップボードにコピー済みであることをユーザーに伝える。

変更が検出されない場合は、コミットする変更がないことをユーザーに伝える。
