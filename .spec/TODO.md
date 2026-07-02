# TODO - タスクリスト

## フェーズ1：データ収集（並行実行可能）
- [x] NAS→ローカルのコピーを rsync ベースに切り替え（SSH経由、30-40MB/s）
- [ ] NAS全年度同期：ICASSP 2001–2026、INTERSPEECH 2007–2023（実行中）
- [ ] Interspeech 2024 を ISCA Archive から収集（実行中）
- [ ] Interspeech 2025 を ISCA Archive から収集（2024完了後に自動実行）
- [ ] Interspeech 2018・2020 を ISCA Archive から収集（NASに無いため）
- [ ] コピー済み年度から順次 PDF→テキスト抽出（ICASSP 2020完了、他年度実行中）

## フェーズ2：統計分析（3層設計）
- [x] 分析スクリプト作成（analyze_corpus.py：語彙/n-gram/記号/文長/章立て/AI典型語）
- [x] ICASSP 2020 の分析（analysis/ICASSP_2020/report.md）
- [ ] 第1層：2015–2022 コア分析（会議別・統合）
- [ ] 第2層：2023–2026 AI混入の年次推移分析
- [ ] 第3層：2001/2005/2010 飛び石の長期トレンド分析
- [ ] ICASSP vs Interspeech の分野差比較
- [ ] セクション別定型表現の抽出（粒度は結果を見て調整）

## フェーズ3：「避けるべき表現」特定
- [x] AI典型表現候補リスト作成 → コーパス頻度と照合（analysis/avoid_list.md、BAN/LIMIT/WATCH 3段階）
- [x] AI生成 vs 実論文の差分分析（語彙レベル）（analysis/ai_vs_human/report.md）
- [x] AI生成 vs 実論文の差分分析（構成レベル：段落・修辞疑問・三点列挙・人間マーカー欠落）
- [ ] 一般学術英語との比較（余力があれば）

## フェーズ4：精読（サブ分野重み付け）
- [x] 音声対話・相槌・応答タイミング関連論文の選定（1,117本、analysis/subfield_papers.tsv）
- [ ] 選定論文の精読・質的知見の抽出（サブ分野固有の表現集）

## フェーズ5：スキルアップグレード
- [x] 既存スキル（paper_writing / field_literature_survey）のバックアップ（_過去のもの/skills_backup_2026-07-02/）
- [x] 分析結果を統合した表現集・禁止リストの作成（analysis/use_list.md + avoid_list.md）
- [x] paper_writing スキルの更新（speech_style_data.md 新設、§8チェックリスト強化、§8.6.5根拠追記、§8.6.7新設）
- [x] field_literature_survey スキルの更新（実装済みパイプライン・3層設計・AI差分法を追記）
- [ ] 実際に論文セクションを書かせて効果検証（実行中：素のAI vs スキル適用AI vs 実論文の3者比較）

## フェーズ6：残タスク
- [x] Interspeech 2018/2020 のISCA収集完了 → NASバックアップ → 抽出・分析（コア再構築・avoid_list再生成済み、基準値に変化なし）
- [ ] Interspeech 2020/2025 の失敗各4件の確認（撤回論文の可能性、実害小）
- [ ] ICASSP 2025 のen-dash・引用符異常の原因確認（組版変更疑い。スキルには不採用済み）
- [ ] サブ分野1,117本（analysis/subfield_papers.tsv）の精読による質的表現集（次の開発サイクル候補）

## 完了済み
- [x] 初期セットアップ
- [x] SPEC.md 作成
