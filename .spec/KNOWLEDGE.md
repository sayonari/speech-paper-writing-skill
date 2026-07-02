# KNOWLEDGE - ドメイン知識・調査結果

## 業務・ドメイン知識
- 対象コーパス：ICASSP 2020–2026（NAS）、Interspeech 2020–2023（NAS、ただし2020は索引のみでPDFなし）、Interspeech 2024–2025（ISCA ArchiveのみのWeb配布）
- Interspeech 2020 の論文PDFはNASに存在しない → ISCA Archive（interspeech_2020）から取得する
- ユーザーの重点サブ分野：音声対話システム・相槌（backchannel）・応答タイミング（turn-taking / response timing）

## 調査・リサーチ結果
- ISCA Archive の構造：`https://www.isca-archive.org/interspeech_<year>/index.html` に論文ページ（`<key>_interspeech.html`）へのリンクがあり、PDFは同名の `.pdf`。Interspeech 2024は1065本
- NASのフォルダ名は `INTERSPEECH`、ローカルは `InterSpeech` と表記が異なる（sync_nas.shでマッピング）
- InterspeechのNAS内PDFは大文字拡張子 `.PDF` が混在（IS2021/ 等のサブフォルダ内）→ 検索は case-insensitive（-iname）必須

## 技術的な知見
- **研究室NAS転送速度（2026-07-02計測）**：SMBマウント経由 0.1〜2.5MB/s に対し、SSH経由rsync（サーバ側read）は **7.2MB/s** と圧倒的に速い。小ファイル多数のProceedingsコピーはSSH rsync一択
- NASはSynology（DS1817）。共有の実パスは `/volume1/Kitaoka_lab/`。rsync 3.1.2 がサーバ側に存在
- NASのユーザーホームが無効（/var/services/homes が無い）ため**SSH公開鍵認証は登録不可**。代わりに SSH ControlMaster（`-o ControlPersist=8h` + `~/.ssh/cm/` ソケット）で一度の認証を使い回す
- Synologyの `@eaDir`（サムネイル用）はrsyncで除外すること
- 長時間ジョブは `caffeinate -i` でスリープ防止

## 分析から得た主要知見（2026-07-02）
- **LLM混入は2024年から人間の論文に定量観測される**：AI典型語がICASSP/Interspeech両方で2024年に爆発（notably ×7、underscore系 ×100超）。em-dashは24年間137/M前後で安定→2025年に両会議とも500/M弱へ（再現性あり）
- **AI語の流行は動く**：delve/realm/pivotal等は2024年ピーク→悪名が広がり2025-26は減少。underscoring/notably/comprehensively等は上昇中。避けるリストは定期再生成が必要
- **現世代AIは有名AI語を既に回避**するため、語彙リストだけでは不十分。差が出るのは構造面：文長（AIは長い）、段落均質性、修辞疑問、三点列挙、**人間マーカー表現の完全欠落**（Note that / It can be seen that / in order to / On the other hand / In other words——AI生成実験で出現ゼロ）
- **会議別作法**：ICASSPは CONCLUSION・Fig. N・全大文字見出し、Interspeechは Conclusions・Figure N・Title Case・Discussion節・番号付き謝辞
- 世間の「AI語リスト」には実測で否定されるものがある（sheds light on / plethora / myriad はLLM後も増えていない）
- ICASSP 2025のen-dash・引用符急増は年固有の組版変更疑い（2026年で半減、特定ファイル集中なし）→スキル不採用

## 決定事項と理由
- 既存の paper_writing / field_literature_survey スキルを**アップグレード**する方針（新規スキル乱立を避ける）
- 「避ける表現」の特定は3手法併用：AI典型表現×コーパス頻度照合／AI生成vs実論文差分（語彙＋構成レベル）／一般学術英語比較（余力があれば）
- コーパス分析は「全文テキスト化＋統計」を主軸に、サブ分野（音声対話・相槌・応答タイミング）論文を優先精読
- 完成スキルはグローバル（~/.claude/skills/）に設置
- コピー完了を待たず、手元にある年度から分析着手
