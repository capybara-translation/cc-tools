---
name: explain-changes
description: Explain the code changes you applied, ordered by importance, with prose plus representative code snippets and Mermaid diagrams where they help, in Japanese. Accepts an optional scope argument (base branch, git range, or PR number).
disable-model-invocation: true
---

## Context: Explanation Target

### Arguments
The user may provide an optional scope argument.
- Base branch name (e.g. `/explain-changes main`): explain `git diff <branch>...HEAD`
- Git range (e.g. `/explain-changes main...HEAD`, `abc123..def456`): explain that range
- PR number / `#N` / PR URL (e.g. `/explain-changes 14`): explain `gh pr diff <N>`
- Empty: explain uncommitted changes (`git diff HEAD`); if there are none, fall back to the current branch vs its base (`git diff <base>...HEAD`, base = merge-base with main/master)

Argument value: $ARGUMENTS

### Current branch
!`git branch --show-current 2>/dev/null`

### Recent commits (for orientation)
!`git log --oneline -15 2>/dev/null || echo "No git history"`

### Default scope: uncommitted changes (stat)
!`git diff --stat HEAD 2>/dev/null || echo "No uncommitted changes"`

### Default scope: uncommitted changes (diff)
!`git diff HEAD 2>/dev/null`

## Your Task

ユーザーがあなた（または誰か）が適用した変更の要点を理解したい。差分を**重要度順**に整理し、**散文＋代表的なコード片**で解説し、関係や流れが文章だけでは掴みにくい箇所は **Mermaid 図**で補え。raw diff をそのまま貼るのではなく、読み手が設計判断を掴めるように合成して説明する。

### 手順

0. **対象差分の確定**: 引数（$ARGUMENTS）に応じて差分を取得する。
   - ブランチ名 → `git diff <branch>...HEAD` と `git diff --stat <branch>...HEAD`
   - git レンジ（`a...b` / `a..b`）→ そのまま `git diff <range>` / `git diff --stat <range>`
   - PR 番号 / `#N` / PR URL → `gh pr diff <N>`（必要なら `gh pr diff <N> --name-only` で一覧）
   - 空 → 上記の uncommitted changes を使う。無ければ `git merge-base HEAD main || git merge-base HEAD master` で base を求め `git diff <base>...HEAD`
   差分が空なら「説明すべき変更がない」旨を伝えて終了する。

1. **全体像の把握**: diffstat と diff から変更の意図を推測する。CLAUDE.md があれば設計方針を踏まえる。

2. **重要度でグルーピング**: ファイルをパス順・diff 出現順ではなく、**重要度順の階層**に並べ替える。目安:
   - 中核ロジック・挙動の変更（その機能の「頭脳」。アルゴリズム/状態遷移/不変条件）
   - 公開インターフェース・配線（API・ルーティング・DI・シグネチャ変更）
   - 永続化・スキーマ・マイグレーション
   - フロントエンド / UI
   - テスト・ドキュメント・機械的な追従修正・整形（最後にまとめて軽く）

3. **ファイル別の解説**: 重要なものから順に、各ファイルの**変更点・追加点**と**「なぜ」**を1〜数文で述べる。新規ファイルか既存改修かを明示する。

4. **代表的なコード片を挟む**: 特に重要なファイルには、**要点の行だけ**を抜き出したコードブロックを添える。
   - 各コードブロックの直前に「このコードが示すこと」を1行で書く。
   - ファイル全体やメソッド全体を貼らない。判断の核心となる数行に絞り、周辺は `// ...` / `# ...` で省略する。
   - コメントは原文の意図が伝わる範囲で簡約してよい。
   - 機械的な churn（シグネチャ追従のテスト修正、gofmt 整形など）にはコード片を付けず、最後にまとめて1〜2文で触れる。

5. **図で補う**: 文章とコード片だけでは関係を掴みにくい箇所には、該当ファイルの解説の中に Mermaid 図を添える。
   - 付ける場面と図の種類:
     - 処理の分岐・データの流れ → `flowchart`
     - 複数モジュール・プロセス間の呼び出し順 → `sequenceDiagram`
     - 状態遷移・ライフサイクル → `stateDiagram-v2`
     - 変更前後の比較・対応関係 → 図ではなく Markdown 表
   - 付けない場面: 1ファイル内で閉じた単純な変更、機械的な追従修正。
   - 各図の直前に「この図が示すこと」を1行で書く。図は要点に絞る（目安: 解説全体で1〜3個、1図あたりノード10個前後まで）。
   - 記法の注意（崩れると図が表示されない）:
     - ` ```mermaid ` ブロックを直接書く。別のコードブロックで囲まない。
     - 日本語や記号を含むラベルは二重引用符で囲む（`A["キャッシュを確認"]`、`stateDiagram-v2` では `state "下書き" as Draft`）。
     - ノード ID は英数字にする。小文字の `end` は ID に使わない。

6. **設計の要点**: 末尾に2〜4個の箇条書きで「この変更を貫く設計の背骨」を述べる（個々のファイルではなく全体の筋）。

### ルール
- **重要度順**に並べる。パス順・アルファベット順・diff 出現順では並べない。
- コード片は**要点の行のみ**。冗長な引用や全文貼り付けは禁止。
- **すべてのコードブロックと図に「何を示すか」の1行**を添える。
- 図は差分から読み取れる事実だけを描く。推測した関係を描かない。
- raw diff をそのまま貼らない。合成して説明する。
- 推測で断定しない。差分から読み取れる事実に基づき、不明な点は不明と明示する。
- 日本語で出力する。技術用語・コード識別子・API 名は原語のまま使う。
- 簡潔に。散文は要点に絞り、詳細はコード片に語らせる。
