# 「使う表現」リスト（音声言語情報処理分野の定型表現）

- 出典: 第1層コアコーパス（ICASSP 2015–2022: 12,609本33.2M語 / InterSpeech 2015–2022: 5,492本18.3M語）
- 数値は per million words（ICASSP側 / InterSpeech側）。目視でノイズ（数式・前付けページ由来）を除外済み
- 「AIが使いたがらない人間の言い回し」には ★ を付した（LLM後のコーパスで減少した表現＝人間らしさのマーカー）

## 1. 研究の自己言及（論文・提案の導入）

| 表現 | ICASSP | InterSpeech | 備考 |
|---|---|---|---|
| In this paper, we propose ... | 149 | 115 | 分野の最頻導入。1論文1回まで |
| In this work, we ... | 205+ | 196 | |
| In this study, we ... | 39 | 83 | InterSpeech（実験系）で多い |
| In this section, we ... | 180 | 81 | セクション冒頭の定番 |
| The rest of the paper is organized as follows. ★ | 66 | 52 | Introduction末尾の定型 |
| To the best of our knowledge, ... | 49 | ~50 | 新規性主張の定型 |
| The contribution(s) of this paper ... | 中頻度 | 中頻度 | |

## 2. 図表・数式への参照

| 表現 | ICASSP | InterSpeech | 備考 |
|---|---|---|---|
| as shown in Fig. N / Figure N | 153+50 | 86 | ICASSPは "Fig."、ISCAは "Figure" 優勢 |
| (Results) are shown in Table N | 57 | 69 | |
| It can be seen that ... ★ | 69 | 49 | AIはあまり使わない人間の定番 |
| We can see that ... ★ | 63 | 49 | 同上。ややカジュアルだが分野で普通 |
| can be written/expressed as | 69+60 | — | 数式導入（ICASSP・信号処理系） |
| is defined as | 37 | 中頻度 | |
| where X is the ... | 極高頻度 | 高頻度 | 数式直後の変数説明 |
| Note that ... ★ | 高頻度 | 高頻度 | 注意喚起の第一選択 |

## 3. 実験・結果報告

| 表現 | ICASSP | InterSpeech | 備考 |
|---|---|---|---|
| Experimental results show that ... | 43 | 49 | |
| (The) results show that the proposed ... | 52+60 | 67 | |
| We evaluate the performance of ... | 48 | 中頻度 | |
| the effectiveness of the proposed (method) | 47 | 51 | |
| outperforms / outperform | 高頻度 | 高頻度 | 比較の動詞はこれが基準 |
| achieves ... (improvement / WER / accuracy) | 高頻度 | 高頻度 | |
| on the test set | 中頻度 | 46 | |
| improve the performance of | 中頻度 | 47 | |

## 4. 論理接続・談話標識（人間の相場感）

| 表現 | ICASSP | InterSpeech | 備考 |
|---|---|---|---|
| In order to ... | 442 | 高頻度 | AIは省きがちだが人間は多用 |
| due to (the) | 309+ | 高頻度 | |
| in terms of | 345 | 48 | |
| On the other hand, ... ★ | 154 | 135 | LLM後×0.3に減少＝人間マーカー |
| In other words, ... ★ | 62 | 中頻度 | LLM後×0.2に減少＝人間マーカー |
| in the context of | 64 | 75 | |
| At the same time, ... | 52 | 49 | |
| as well as | 高頻度 | 82 | |
| In addition to ... | 中頻度 | 46 | additionallyより句形が人間的 |
| in the presence of | 52 | 中頻度 | 雑音・残響文脈の定番 |
| It should be noted that ... ★ | 20 | 中頻度 | LLM後×0.4に減少 |
| It is worth noting that ... | 19 | 中頻度 | 適正頻度は1論文0.05回程度 |

## 5. 分野固有の語彙・慣用

| 表現 | 備考 |
|---|---|
| state-of-the-art | 360〜458/M。**AI臭どころか分野の常用語**。ただし1論文2回程度が相場 |
| automatic speech recognition (ASR) | 初出でフル+略語定義が作法（47〜160/M） |
| word error rate (WER) | 同上（IS: 65/M） |
| deep neural network (DNN) | 同上 |
| baseline / baselines | 比較対象の呼称はこれ |
| significantly (統計的文脈) | 337/M。有意差の文脈で正当 |

## 6. 謝辞・サポート文（Acknowledgements）

| 表現 | ICASSP | 備考 |
|---|---|---|
| This work was supported (in part) by ... | 70 | 定型そのもの |
| ... (grant No. XXX) | — | |

## 7. 使用上の原則（数値根拠）

- **文長**: 平均24〜25語、中央値21語。26年間不変の分野標準。90%タイルは40〜42語——それを超える長文を連発しない
- **セミコロン**: 0.03〜0.05回/文（30文に1〜1.5回）。文接続は基本ピリオドで切る
- **em-dash（—）**: 使わない（0.4回/論文が人間の相場。挿入はカンマか括弧で）
- **箇条書き**: 本文では1論文1箇所未満が相場。散文で書く
- **結論見出し**: ICASSPは CONCLUSION、InterSpeechは CONCLUSIONS が優勢
- **章立て**: ICASSP: `INTRODUCTION → (RELATED WORK) → PROPOSED METHOD → EXPERIMENTS → CONCLUSION` / InterSpeech: `Introduction → Method(s) → Results → Discussion → Conclusions →（番号付き）Acknowledgements`
