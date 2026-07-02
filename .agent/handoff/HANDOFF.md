# HANDOFF - 2026-07-02 13:59

## 使用ツール
Claude Code（Fable 5）

## 現在のタスクと進捗
- [x] コーパス構築・統計分析・スキル改訂（前回ハンドオフ 2026-07-02-1317.md 参照。62,977本・166.9M語）
- [x] リポジトリ公開：https://github.com/sayonari/speech-paper-writing-skill （PUBLIC）
- [x] ショーケース論文 `paper/main.pdf` 完成（5ページ：本文＋謝辞が4ページ末、Referencesが5ページ目）
  - Fig.1（em-dash/notablyの26年推移）、定型表現表、Discussion節（倫理・限界）、自己検査の顛末を含む
  - 著者確定：Ryota Nishimura / Toyohashi Univ. of Tech. / nishimura.ryota.tz@tut.jp
  - 参考文献4件は実在検証済み（paper/references_verification.md）
- [x] 比較用「スキルなし版」 `paper_ai_default/main.pdf` 公開（同一データ・同一テンプレート、謝辞捏造のデモ含む、1ページ目に引用禁止注記）
- [x] スキル同梱（skills/）＋ `scripts/install_skills.sh` でワンコマンド導入可能
- [x] README.md 整備（発見一覧・インストール・読み比べセクション・再生成手順）
- [ ] サブ分野精読（analysis/subfield_papers.tsv の1,117本）→ 質的表現集の追補（次サイクル候補、/newplan 推奨）
- [ ] Interspeech 2020/2025 のDL失敗 各4件の確認（撤回論文の可能性、実害小）

## 試したこと・結果
- **成功**：論文の増ページは「水増し」でなく未掲載実データ（図・表・議論）の追加で実現。ページ境界調整は 図の高さ縮小 → titlespacing詰め → 謝辞文の短縮 → `\enlargethispage{2\baselineskip}` の順で解決
- **成功**：図の配色は dataviz スキルの validate_palette.js で検証（Okabe-Ito #0072B2/#D55E00、ΔE 91.9）。生成は paper/make_figure.py
- **成功**：論文自体を scripts/compare_style.py で自己検査 → セミコロン超過を検出し3箇所修正（この顛末は論文5節に記載）
- **失敗と対策**：シェルのヒアドキュメント内でLaTeXのバッククォート（``）がコマンド置換として実行され、スキルなし版の文献リストが破損 → **バッククォートを含むLaTeXはWrite/Editツールで書くこと**（シェルheredocは危険）
- **知見**：スキルなし版でも語彙は比較的まとも＝論文の内容自体が避けるべき語を教えるため。純粋な文体差の実験は analysis/ai_vs_human/（人間マーカー 0 vs 6.88/1k語）

## 次のセッションで最初にやること
1. `.agent/memory/MEMORY.md` と本ファイルを読む（AGENTS.md のルール通り）
2. 未コミットの変更がないか `git status` を確認（現時点では全てpush済み、HEAD=869247a）
3. 次サイクルに入るなら `/newplan` を実行し、サブ分野精読（相槌・応答タイミング216本から）をPLAN化

## 注意点・ブロッカー
- **NASパスワードがチャット履歴に残っているため変更推奨**（ユーザーに伝達済み・未対応の可能性）
- リポジトリはPUBLIC。paper_ai_default は意図的にAnti-patternと捏造謝辞を含むデモなので、編集時も注記（Do not cite）を消さないこと
- paper/ のコンパイルは必ず `./compile.sh`（pdflatex系）。図の再生成は `python3 paper/make_figure.py`（プロジェクトルートから）
- スキルの原本は `~/.claude/skills/`、配布版は `skills/`。更新時は原本→skills/へコピーしてコミット（README記載の運用）
- MEMORY.md は今回未更新（AGENTS.mdルール上、次回更新時は日付アーカイブしてから）
