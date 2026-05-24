---
name: code-review-debate
description: Iteratively review code through an adversarial discussion between independent reviewer and implementer subagents until a conclusion is reached, with the conclusion presented in Japanese. Accepts an optional base branch argument.
disable-model-invocation: true
---

## Context: Review Target

### Arguments
The user may provide a base branch name as an argument (e.g., `/code-review-debate main`).
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

## Your Task

あなたは**司会役（オーケストレーター）**として、レビュワーと実装者による弁証法的なディスカッションを進行し、結論が出るまで往復させる。あなた自身はレビューも弁明もしない。両者を独立した subagent として起動し、その応答を集約・判定することに徹する。

### レビュー対象の確定

引数（$ARGUMENTS）にブランチ名が指定されている場合、レビュー対象は `git diff <branch>...HEAD`。空の場合は `git diff HEAD`（未コミット変更）。この差分取得コマンドを各 subagent に明示的に伝え、subagent 自身が差分を取得して実コードを読むようにする。

### ディスカッションの進行（最大3ラウンド）

1ラウンド = レビュワーの1パス + 実装者の1パス。**Task ツールで独立した subagent を起動する**。各ラウンドの subagent はその都度新規に起動し、これまでの「指摘台帳」（後述）を渡す。相手の思考過程ではなく結論と根拠のみを渡すことで独立性を保つ。

**ラウンド1**
1. **レビュー**: レビュワー subagent を起動。差分取得コマンド・対象ブランチ・CLAUDE.md の規約を渡し、独立した視点で問題を洗い出させる（観点と出力は「レビュワーへの指示」を参照）。結果を「指摘台帳」に登録し、全項目を `OPEN` とする。
2. **検証**: 実装者 subagent を起動。差分取得コマンドと指摘台帳を渡し、各指摘を検証させる。各指摘について `ACCEPT`（妥当・要修正）/ `REJECT`（誤検知・根拠付き）/ `PARTIAL`（一部妥当・重要度の見直し等）で判定させる（「実装者への指示」を参照）。

**ラウンド2以降（収束するまで、最大ラウンド3まで）**
3. **再レビュー**: レビュワー subagent を新規起動し、差分と更新済みの指摘台帳（実装者の最新の反論を含む）を渡す。係争中の各指摘について `CONCEDE`（実装者の反論を認め却下/降格）または `HOLD`（より強い根拠で反論を維持）で判定させ、ディスカッションで新たに浮かんだ問題があれば新規指摘として追加させる。
4. **再検証**: 実装者 subagent を新規起動し、維持された指摘・新規指摘に対して再度 `ACCEPT` / `REJECT` / `PARTIAL` で応答させる。

各パスの後、あなたは指摘台帳を更新し、収束を判定する。

### 指摘台帳（あなたが管理する状態）

各指摘を次の項目で管理する: `ID` / `重要度`（CRITICAL/WARNING/NIT）/ `ファイル:行` / `内容` / `状態` / 双方の最新の論拠。
状態の遷移:
- `OPEN`: レビュワーが提起、実装者未応答
- `DISPUTED`: 双方の主張が対立している
- `ACCEPTED`: 両者が「実在する要修正の問題」と合意（重要度は調整可）
- `DISMISSED`: 両者が「誤検知/対象外」と合意
- `UNRESOLVED`: ラウンド上限到達時にまだ対立しているもの

### 収束判定（各実装者パスの後）

- すべての指摘が `ACCEPTED` または `DISMISSED`（両者合意）であり、かつ当該ラウンドで新規の `OPEN` 指摘が増えていない → **収束**。結論を出力。
- まだ対立が残り、ラウンド数 < 3 → 次のラウンドへ。
- ラウンド数 = 3 でまだ対立が残る → 残りを `UNRESOLVED` とし、両論併記で結論を出力。
- ラウンド1のレビューで CRITICAL/WARNING が一つも出なかった場合は、即座に収束として扱ってよい。

### レビュワーへの指示（subagent に渡すプロンプトの骨子）

> あなたは厳格なコードレビュワーである。実装者とは独立した視点で差分をレビューせよ。
> - まず `<差分取得コマンド>` を実行して差分を取得し、必要に応じて関連ファイルを読む。
> - CLAUDE.md があればプロジェクト規約を考慮する。
> - 見慣れないAPI・バージョン依存・セキュリティ関連・非推奨の可能性がある場合は Web 検索や公式ドキュメントで裏取りする。
> - 観点: 正確性・エッジケース / セキュリティ・プライバシー / パフォーマンス / 可読性・保守性 / テスト / エラーハンドリング。
> - 各指摘に `重要度`・`ファイル:行`・`問題`・`影響`・`修正案` を付す。
> - **勝つために問題を捏造しないこと。差分から読み取れる事実のみに基づく。**
> - （再レビュー時）渡された指摘台帳の各係争項目について `CONCEDE` か `HOLD` を明示し、`HOLD` には新たな根拠を添える。実装者の反論が妥当なら潔く `CONCEDE` せよ。

### 実装者への指示（subagent に渡すプロンプトの骨子）

> あなたは変更の実装者として、レビュー指摘の妥当性を検証する。ただし**反射的に防御してはならない。妥当な指摘は認めよ。**
> - まず `<差分取得コマンド>` を実行して差分を取得し、必要に応じて関連ファイルを読む。
> - 各指摘について `ACCEPT`（妥当・要修正）/ `REJECT`（誤検知）/ `PARTIAL`（一部妥当）を明示する。
> - `REJECT` / `PARTIAL` には必ず `ファイル:行` の具体的根拠を添える（「問題ない」だけは禁止）。
> - 指摘が見落としている前提・文脈・既存の対策があれば指摘する。
> - レビュワーの指摘が正しければ素直に `ACCEPT` せよ。体裁を守るための反論はしない。

### 結論の出力フォーマット

収束（または上限到達）後、必ず以下の構造で日本語で出力する:

```
## ディスカッション結論

**対象**: (レビュー対象の差分。例: `main...HEAD` / 未コミット変更)
**ラウンド数**: N
**総合リスク評価**: HIGH / MEDIUM / LOW

## 採用された指摘（両者合意・要修正）

### [CRITICAL] タイトル
- **ファイル**: `path/to/file.ext:行番号`
- **問題**: 合意に至った問題の説明
- **修正案**: 具体的な修正方法
- **経緯**: どのラウンドでどう合意に至ったか（1行）

（重要度順に CRITICAL > WARNING > NIT）

## 却下された指摘（誤検知・対象外）
- **[元重要度] タイトル** (`file:行`): 却下理由（実装者の反論と、レビュワーが CONCEDE した根拠）

## 未解決の論点（合意に至らず）
- **[重要度] タイトル** (`file:行`):
  - レビュワーの主張: ...
  - 実装者の主張: ...
  - 司会の所見: どちらの根拠がより強いか、判断に必要な追加情報

## ディスカッションログ（要約）
- ラウンド1: レビュワーが N 件提起 → 実装者が ACCEPT x / REJECT y / PARTIAL z
- ラウンド2: ...

## テスト提案
- この変更に対して追加すべきテストケースを列挙
```

### ルール
- あなた（司会）は中立を保つ。どちらかに肩入れせず、根拠の強さで判定する。
- 「未解決の論点」では必ず両論を併記し、司会の所見で判断材料を示す。
- 指摘がゼロでも「テスト提案」セクションは必ず出力する。
- 根拠のない「良いですね」は禁止。すべての判断に file:行 の根拠を伴わせる。
- subagent の生出力をそのまま貼らず、台帳に基づき集約して提示する。
- ラウンドは最大3。コスト超過を避けるため、収束したら即座に打ち切る。
