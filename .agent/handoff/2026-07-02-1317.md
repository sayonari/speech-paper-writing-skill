# HANDOFF - 2026-07-02 13:16

## 使用ツール
Claude Code（Fable 5）

## 現在のタスクと進捗
- [x] プロジェクト初期構築（make_project モードA、GitHub: https://github.com/sayonari/speech-paper-writing-skill プライベート）
- [x] コーパス構築：ICASSP 2001–2026＋Interspeech 2007–2025 全proceedings（_ref/papers/ 85GB、corpus/ 63,181本・7,600万語）
- [x] NASへの書き戻し：Interspeech 2018/2020/2024/2025 をISCA Archiveから収集しNASの欠落を補完
- [x] 統計分析：全年度の語彙/n-gram/記号/文長/章立て/AI典型語（analysis/ 配下、trends_*.md で年次推移）
- [x] 「避ける表現」確定リスト（analysis/avoid_list.md、BAN/LIMIT/WATCH、実測値付き）
- [x] 「使う表現」リスト（analysis/use_list.md、機能別・会議別）
- [x] AI生成 vs 実論文の差分分析＋スキル効果検証（analysis/ai_vs_human/report.md）
- [x] グローバルスキル改訂：paper_writing（speech_style_data.md 新設＋SKILL.md 3箇所）、field_literature_survey（パイプライン・方法論追記）。バックアップは _過去のもの/skills_backup_2026-07-02/
- [ ] サブ分野精読：相槌・応答タイミング系1,117本のリスト作成済み（analysis/subfield_papers.tsv）、精読は未着手
- [ ] 初期構築後の成果物一式がまだGitにコミットされていない（初回コミットのみ）

## 試したこと・結果
- **成功**：NASコピーはSMB経由（0.1〜2.5MB/s）を捨て、SSH経由rsync（30〜40MB/s実測）に切替。NASはSynology DS1817、ホーム無効のため鍵登録不可→SSH ControlMaster（~/.ssh/cm/ ソケット、ControlPersist=8h）で認証を使い回す方式。scripts/sync_nas.sh / backup_to_nas.sh 参照
- **成功**：3層コーパス設計（コア2015–2022＝純粋な人間文体／2023以降＝LLM混入観測／飛び石＝長期トレンド）。em-dashが24年間137/M安定→2025年に両会議で約500/Mに爆発、など混入が定量観測できた
- **成功**：スキル効果検証。素のAI（人間マーカー0、em-dashあり）→スキル適用AI（人間マーカー6.88/1k≒実論文6.05、em-dash 0）
- **失敗と対策**：BANフレーズが活用形（shed some light on）ですり抜け→語幹grepセルフチェックをspeech_style_data.md §6.5に追加
- **注意**：Finderコピー由来のAppleDoubleゴミ（._*.PDF）が抽出失敗を量産→ _ref から削除済み。ICASSP 2026はNAS側にzip展開版とpdfs/の二重格納あり（同名スキップで実害なし）

## 次のセッションで最初にやること
1. `.agent/memory/MEMORY.md` と本ファイルを読む（AGENTS.md のルール通り）
2. 成果物一式（scripts/ analysis/ .spec/ 等）をGitにコミット・push する（ユーザー確認の上）
3. 次の開発サイクル候補：サブ分野精読（analysis/subfield_papers.tsv の相槌・応答タイミング216本から開始し、質的表現集を speech_style_data.md に追補）。開始時は /newplan を使う

## 注意点・ブロッカー
- **NASパスワードがチャットに貼られたため変更推奨**（ユーザーに伝達済み）。スクリプト類にパスワードは保存していない。SSH ControlMasterソケットは8時間で失効→再確立手順は scripts/sync_nas.sh 冒頭コメント参照
- corpus/ と _ref/ は .gitignore 済み（計100GB。Git管理しない）
- Interspeech 2020/2025 に各4件のダウンロード失敗（撤回論文の可能性、実害小）
- ICASSP 2025 のen-dash・引用符頻度に年固有の異常（組版変更疑い）。スキルの根拠には不採用としてある
- スキルの避けるリストは「AI語の流行が動く」ため年1回程度の再生成を推奨（scripts/build_avoid_list.py。手順は field_literature_survey/SKILL.md の追記節参照）
