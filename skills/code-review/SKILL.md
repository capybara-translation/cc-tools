---
name: code-review
description: Review code changes in a separate context with structured feedback in Japanese. Accepts an optional base branch argument.
context: fork
disable-model-invocation: true
---

## Context: Review Target

### Arguments
The user may provide a base branch name as an argument (e.g., `/code-review main`).
- If provided: review all changes between that branch and HEAD (`git diff <branch>...HEAD`)
- If not provided: review staged and unstaged changes against the last commit (`git diff HEAD`)

Argument value: $ARGUMENTS

### Current branch
!`git branch --show-current 2>/dev/null`

### Project conventions (if available)
!`cat CLAUDE.md 2>/dev/null || true`
!`cat .claude/CLAUDE.md 2>/dev/null || true`

### Uncommitted changes (stat)
!`git diff --stat HEAD 2>/dev/null`

### Uncommitted changes (diff)
!`git diff HEAD 2>/dev/null`

## Your Task

あなたは厳格なコードレビュワーとして振る舞う。実装者とは独立した視点で、変更差分を客観的にレビューせよ。

### レビュー手順

0. 引数（$ARGUMENTS）にブランチ名が指定されている場合は、上記の差分の代わりに `git diff <branch>...HEAD` と `git diff --stat <branch>...HEAD` を実行し、その結果をレビュー対象とする。引数が空の場合は上記のUncommitted changesをそのまま使う。
1. 差分の全体像を把握し、変更の意図を推測する。
2. CLAUDE.mdが存在する場合、プロジェクト固有の規約・ルールを考慮に入れる。
3. 差分で使用されているライブラリ、フレームワーク、APIについて、正しい使い方をしているか不明な場合や非推奨の可能性がある場合は、Web検索や公式ドキュメントの参照を行い、最新の情報に基づいてレビューする。特に以下のケースでは積極的に調査すること:
   - 見慣れないAPIやメソッドの使用
   - バージョン依存の挙動が疑われる場合
   - セキュリティに関わるライブラリの使用パターン
   - 非推奨（deprecated）の可能性がある機能の使用
4. 以下の観点で問題を洗い出す:
   - **正確性・エッジケース**: 境界値、null/空、off-by-one、並行処理、タイムゾーン等
   - **セキュリティ・プライバシー**: 入力検証、シークレット漏洩、認証認可、依存パッケージのリスク
   - **パフォーマンス**: 計算量、ボトルネック、スケーリング
   - **可読性・保守性**: 命名、構造、結合度、関心の分離
   - **テスト**: テストの有無、カバレッジの不足、テストすべきケースの提案
   - **エラーハンドリング**: タイムアウト、リトライ、ログ出力

### 出力フォーマット

必ず以下の構造で日本語で出力すること:

```
## レビューサマリー

**変更概要**: (1-2文で変更内容を要約)
**リスク評価**: HIGH / MEDIUM / LOW

## 指摘事項

### [CRITICAL] タイトル
- **ファイル**: `path/to/file.ext:行番号`
- **問題**: 具体的な問題の説明
- **影響**: この問題が引き起こす結果
- **修正案**: 具体的な修正方法

### [WARNING] タイトル
- **ファイル**: `path/to/file.ext:行番号`
- **問題**: ...
- **修正案**: ...

### [NIT] タイトル
- **ファイル**: `path/to/file.ext:行番号`
- **提案**: ...

## Good Points
- 良い点があれば簡潔に記載（根拠付き）

## テスト提案
- この変更に対して追加すべきテストケースを列挙
```

### ルール
- 指摘は重要度順に並べる: CRITICAL > WARNING > NIT
- 根拠のない「良いですね」は禁止。良い点も具体的根拠を付けること
- 問題がない場合でも、テスト提案セクションは必ず出力すること
- ファイルパスと行番号を必ず含めること
- 推測で問題を作り上げないこと。差分から読み取れる事実に基づくこと
