# Humans Do Not Delve 🎙️📝
**音声系英語論文執筆スキル — Speech-Field English Paper-Writing Skill for LLM Agents**

ICASSP 2001–2026 と Interspeech 2007–2025 の**全proceedings（62,977本・1億6,690万語）**を統計分析し、
「音声言語情報処理分野の人間研究者が書く英語」を実測データで定義。その結果を、LLMコーディングエージェント
（Claude Code等）が参照できる**論文執筆スキル**として実装したプロジェクトです。

📄 **成果論文（このスキル自身を使って執筆・2段組4ページ）**: [`paper/main.pdf`](paper/main.pdf)
*"Humans Do Not Delve: Measuring LLM-Induced Style Drift in 25 Years of Speech Conference Papers"*

## 主な発見 / Key Findings

| 発見 | 実測値 |
|---|---|
| **人間のベースラインは驚異的に安定** | em-dash 92–149/百万語・文長24.5語・セミコロン0.03–0.05/文が**2001→2024年の24年間ほぼ不変** |
| **2024年にLLM混入が爆発** | *notably* 24→152/M、*crucial* 63→205/M、*underscoring* ×100超（両会議で再現） |
| **em-dash（—）の激増** | 24年間安定 → **2025年に ICASSP 514/M・Interspeech 489/M へ一斉に3倍化** |
| **AI語には流行がある** | *delve*・*realm*・*pivotal* は2024年ピーク→悪名が広がり急減。固定ブロックリストは陳腐化する |
| **「消えつつある人間の言い回し」が最強の識別子** | *in other words*（×0.2）・*on the other hand*（×0.3）等はAIが自発的に書かない → 「使え」と指示できる |
| **俗説のAI語には実測で否定されるものも** | *sheds light on* / *a plethora of* / *myriad* はLLM後も増えていない（単に稀な語） |
| **会議ごとに作法が違う** | ICASSP: `CONCLUSION`・`Fig. N` / Interspeech: `Conclusions`・`Figure N`・Discussion節・番号付き謝辞 |

**検証実験**: スタイル指示なしのLLMは第1文からem-dashを使い人間マーカー0。スキルを与えると
em-dash 0・人間マーカー率6.88/1k語（実論文6.05/1k語とほぼ一致）に到達。

## リポジトリ構成

```
paper/                  ショーケース論文（LaTeX + compile.sh + PDF）
scripts/                再実行可能な分析パイプライン
  download_isca.sh        ISCA ArchiveからInterspeech proceedingsを収集（レート制限付き）
  sync_nas.sh             研究室NASとの同期（SSH経由rsync）
  backup_to_nas.sh        Web収集分をNASへ書き戻し
  extract_text.sh         PDF→テキスト一括抽出（pdftotext）
  analyze_corpus.py       語彙 / n-gram / 記号 / 文長 / 章立て / AI典型語の統計
  trend_report.py         年次推移レポート生成
  build_avoid_list.py     BAN/LIMIT/WATCH自動分類（ベースライン×急増率）
  compare_style.py        AI生成テキストと実論文のスタイル指標比較
analysis/               分析結果（全45年度分）
  avoid_list.md           「避ける表現」確定リスト（全項目に実測値付き）
  use_list.md             「使う表現」リスト（機能別・会議別）
  trends_ICASSP.md        ICASSP 26年の年次推移
  trends_InterSpeech.md   Interspeech 19年の年次推移
  ai_vs_human/            AI生成 vs 実論文の差分・検証実験レポート
  subfield_papers.tsv     音声対話・相槌・応答タイミング関連1,117本のリスト
  <会議>_<年>/            年度別の生統計（unigram〜4gram, 見出し, 記号 等のCSV）
.spec/                  仕様駆動開発ドキュメント（PLAN / SPEC / TODO / KNOWLEDGE）
```

**注**: 論文PDF（`_ref/`、85GB）と抽出テキスト（`corpus/`、15GB）は著作権とサイズのため
リポジトリに含めていません。統計値（頻度集計）のみを公開しています。

## スキル本体の場所

分析結果は以下のグローバルスキルに反映済みです（このリポジトリには改訂前のバックアップを保存）：

- `~/.claude/skills/paper_writing/speech_style_data.md` — 実測データ集：BAN/LIMIT/WATCH語彙、
  人間マーカー表現、定量目標（文長・記号）、会議別作法、活用形もれ対策のgrepセルフチェック
- `~/.claude/skills/paper_writing/SKILL.md` — 英語品質チェックリスト・構造ルールに実測根拠を統合
- `~/.claude/skills/field_literature_survey/SKILL.md` — 本パイプラインの再実行手順と方法論
  （3層コーパス設計・AI差分法）を追記

## パイプラインの使い方（再生成手順）

AI語の流行は移り変わるため、年1回程度（新年度proceedings追加時）の再生成を推奨します。

```bash
# 1. 新年度の収集（例：Interspeech 2026がWeb公開されたら）
./scripts/download_isca.sh 2026

# 2. テキスト抽出
./scripts/extract_text.sh InterSpeech 2026

# 3. 年度分析 → 推移レポート → 避けるリスト更新
python3 scripts/analyze_corpus.py corpus/InterSpeech/2026 --out analysis/InterSpeech_2026 --top 500
python3 scripts/trend_report.py --conf InterSpeech --out analysis/trends_InterSpeech.md
python3 scripts/build_avoid_list.py --out analysis/avoid_list.md
```

## 方法論のポイント：3層コーパス設計

2023年以降の「人間の論文」には既にLLM支援の文章が混入しているため、文体の見本に使ってはいけません。

1. **コア層（2015–2022）** — ChatGPT以前の純粋な人間文体。全ての頻度基準の根拠
2. **混入観測層（2024–2026）** — 見本ではなく「検出器」。ここで急増した表現＝AI由来の候補
3. **歴史層（2001–2014）** — 分野の核となる定番表現と一時的流行の区別に使用

## 制限事項

- pdftotextによる抽出のため段落境界・数式は不完全（ICASSP 2025のen-dash/引用符の急増は
  組版変更の疑いがあり、スキルの根拠から除外済み）
- 検証実験は3テーマ×1モデル系列の機能テストであり、AI検出の主張ではない
- 対象は英語・国際会議2件。ジャーナルや他分野への一般化は今後の課題

## クレジット

- 企画・監督: 西村良太（豊橋技術科学大学）
- コーパス構築・分析・スキル実装・論文起草: Claude (Anthropic) — Claude Code上で実施
- Proceedingsアーカイブ: 北岡研究室 / ISCA Archive

---
*このプロジェクトは 2026-07-02 に Claude Code（Fable 5）を用いて1セッションで構築されました。*
