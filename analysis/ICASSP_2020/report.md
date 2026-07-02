# ICASSP 2020 コーパス統計分析レポート

- 分析日: 2026-07-02
- 対象: ICASSP 2020 proceedings 全1,896本（抽出成功分）、総語数 5,079,706語、総文数 240,841文
- 生成: `scripts/analyze_corpus.py`（詳細データは同フォルダのCSV参照）

## 1. 記号使用の実態（AI臭の定量的裏付け）

| 記号 | 1論文あたり | 100万語あたり | 所見 |
|---|---|---|---|
| em-dash（—、Index Terms定型を除く） | **0.37回** | 137 | 人間はほぼ使わない。AIは多用 → **避けるべき筆頭** |
| `---` | 0.02回 | 9.3 | 実質ゼロ（表罫線等の残骸） |
| `--` | 0.004回 | 1.4 | 実質ゼロ |
| セミコロン ; | 4.2回 | 1,560 | **0.033回/文（30文に1回）**。文接続への多用はAI臭 |
| en-dash – | 2.3回 | 843 | 範囲表記（例: 1–5）等で normal use |
| 箇条書き • | 0.87回 | 326 | 4ページ論文で1個未満 → **本文の箇条書き乱用はAI臭** |
| コロン : | 16.6回 | 6,187 | 普通に使われる |
| 括弧 ( | 96.6回 | 36,053 | 引用・略語定義で極めて高頻度（分野の特徴） |

## 2. 文長

- 平均 24.5語/文、中央値 21語、90%タイル 42語
- → 極端な短文の連打や、50語超の長文の常用はどちらも分布から外れる

## 3. 章立てパターン（トップレベル見出し）

最頻の構成（4ページ論文の骨格）:
1. `INTRODUCTION > PROPOSED METHOD > EXPERIMENTS > CONCLUSION`（最多）
2. `INTRODUCTION > METHODOLOGY > EXPERIMENTS > CONCLUSION`
3. `INTRODUCTION > PROPOSED METHOD > EXPERIMENTAL RESULTS > CONCLUSION`
4. RELATED WORK を挟む5節構成がそれに続く

見出し語の頻度: INTRODUCTION(790) / CONCLUSION(427) vs CONCLUSIONS(190) / EXPERIMENTS(216) / RELATED WORK(83) / PROPOSED METHOD(72) / METHODOLOGY(47)
→ 結論見出しは **CONCLUSION が CONCLUSIONS の約2.2倍**

## 4. 分野の定番表現（積極的に使ってよいもの）

| 表現 | 回数 | /百万語 |
|---|---|---|
| in this paper, we | 2,502 | 493 |
| in this work, we | 1,042 | 205 |
| in this section, we | 914 | 180 |
| as shown in Fig. | 776 | 153 |
| this paper we propose (=In this paper, we propose) | 755 | 149 |
| state-of-the-art | 941 | 358 |
| on the other hand | 781 | 154 |
| the proposed method | 1,025+ | 390+ |
| in terms of | 907 | 345 |
| to the best of our knowledge | 144 | 55 |
| experimental results show/demonstrate | 194 | 74 |
| (this) paper is organized as (follows) | 336 | 66 |

頻出内容語トップ: data, training, network, performance, speech, set, different, learning, number, time, signal, ...

## 5. AI典型語の実測頻度（「避けるリスト」の根拠）

### ほぼゼロ（使ったら即AI臭）: /百万語 < 3
delve系(0.2–0.4), tapestry(0), bolster(0), meticulous系(0.2–0.6), garner系(0.4–1.2),
underscore系(0.2–1.0), realm(1.0), in the realm of(0.2), nuanced(0.8), multifaceted(0.4),
intricacies(0.4), pivotal(2.4), seamless(ly)(1.8–2.6), cutting-edge(1.0), groundbreaking(0.2),
elucidate(0.6), empower(1.4), harness(2.4), foster(2.2), ever-evolving(0), rapidly evolving(0.2),
paving the way(1.2), sheds light on(1.0), plays a crucial role(1.0), a plethora of(3.2), myriad(1.2)

### 低頻度（乱用注意）: /百万語 3–30
showcase系(1.4–6.7), holistic(6.3), innovative(7.7), noteworthy(7.9), robustly(12), remarkably(13),
notably(24), vital(28), landscape(4.3), intricate(4.1), crucially(4.7), it is important to note(11),
plays an important role(12), more and more(10)

### 普通に使われる（禁止不要、ただし頻度感を守る）: /百万語 > 45
significantly(337), overall(287), moreover(266), furthermore(253), additionally(111),
consequently(77), crucial(62), essential(60), paradigm(45)

## 6. 注意事項（データの限界）

- `where is the` などの高頻度trigramは数式変数の脱落による人工物（"where **x** is the ..."）。表現集に入れる際は要文脈確認
- ICASSP 2020単年・単会議の結果。Interspeech・他年度と比較して安定性を確認予定（特に2023以降はLLM時代で頻度が変わる可能性あり→年次推移の分析が有効）
- ICASSPはIEEE 2段組4ページのspoken language processing以外（映像符号化・レーダー等）も含む。サブ分野フィルタは今後の課題
