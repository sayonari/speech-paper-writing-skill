# 「避ける表現」確定リスト（データ根拠付き）

- baseline: 2015–2022 ICASSP+InterSpeech 加重平均 per million words（人間の適正頻度）
- post_llm: 2024–2026 ICASSP 加重平均 per million words
- BAN=人間はそもそも使わない / LIMIT=適正頻度を超えるな / WATCH=多用注意 / OK=問題なし

## 語
| 項目 | baseline | post_llm | 倍率 | 判定 |
|---|---|---|---|---|
| underscoring | 0.3 | 30.0 | ×89.9 | **BAN** |
| underscores | 0.7 | 24.5 | ×34.0 | **BAN** |
| meticulously | 0.3 | 8.6 | ×27.2 | **BAN** |
| bolster | 0.1 | 2.7 | ×25.5 | **BAN** |
| underscore | 0.7 | 18.7 | ×25.3 | **BAN** |
| delves | 0.0 | 1.8 | ×18.1 | **BAN** |
| nuanced | 1.2 | 19.1 | ×15.7 | **BAN** |
| showcasing | 1.2 | 18.4 | ×15.6 | **BAN** |
| pivotal | 1.7 | 24.4 | ×14.6 | **BAN** |
| garnered | 0.7 | 10.2 | ×13.8 | **BAN** |
| intricate | 2.7 | 36.4 | ×13.2 | **BAN** |
| bolsters | 0.0 | 1.1 | ×11.2 | **BAN** |
| harnesses | 0.4 | 4.1 | ×10.2 | **BAN** |
| delving | 0.3 | 3.2 | ×10.0 | **BAN** |
| intricacies | 0.2 | 2.4 | ×9.8 | **BAN** |
| fosters | 0.3 | 2.5 | ×9.5 | **BAN** |
| delve | 0.7 | 5.8 | ×8.4 | **BAN** |
| harnessing | 1.1 | 9.2 | ×8.3 | **BAN** |
| meticulous | 0.4 | 2.9 | ×7.9 | **BAN** |
| multifaceted | 0.4 | 3.1 | ×7.4 | **BAN** |
| empowers | 0.6 | 4.4 | ×7.3 | **BAN** |
| showcases | 1.2 | 8.2 | ×7.0 | **BAN** |
| seamless | 2.3 | 14.1 | ×6.1 | **BAN** |
| cutting-edge | 0.8 | 4.3 | ×5.5 | **BAN** |
| fostering | 0.8 | 4.2 | ×5.1 | **BAN** |
| harness | 1.7 | 8.0 | ×4.7 | **BAN** |
| realm | 2.0 | 9.0 | ×4.6 | **BAN** |
| elucidates | 0.3 | 1.2 | ×4.5 | **BAN** |
| groundbreaking | 0.4 | 1.7 | ×4.5 | **BAN** |
| empower | 0.5 | 2.2 | ×4.0 | **BAN** |
| elucidate | 1.4 | 3.3 | ×2.4 | **BAN** |
| unveils | 0.3 | 0.6 | ×2.0 | **BAN** |
| foster | 2.9 | 5.1 | ×1.8 | **BAN** |
| unveil | 1.0 | 1.5 | ×1.6 | **BAN** |
| garners | 0.0 | 0.1 | ×1.4 | **BAN** |
| tapestry | 0.5 | 0.2 | ×0.4 | **BAN** |
| garner | 1.2 | 0.3 | ×0.3 | **BAN** |
| comprehensively | 4.5 | 31.2 | ×6.9 | **LIMIT** |
| seamlessly | 3.5 | 22.4 | ×6.4 | **LIMIT** |
| notably | 24.2 | 148.9 | ×6.2 | **LIMIT** |
| innovative | 7.0 | 40.5 | ×5.8 | **LIMIT** |
| crucially | 3.7 | 14.1 | ×3.8 | **LIMIT** |
| holistic | 8.0 | 26.4 | ×3.3 | **LIMIT** |
| crucial | 63.5 | 205.0 | ×3.2 | **LIMIT** |
| landscape | 4.8 | 14.7 | ×3.1 | **LIMIT** |
| additionally | 117.7 | 308.5 | ×2.6 | **WATCH** |
| paradigm | 52.5 | 137.4 | ×2.6 | **WATCH** |
| showcase | 4.6 | 12.1 | ×2.6 | **WATCH** |
| vital | 14.6 | 38.4 | ×2.6 | **WATCH** |
| essential | 59.2 | 138.3 | ×2.3 | **WATCH** |
| consequently | 68.2 | 120.4 | ×1.8 | **OK** |
| noteworthy | 8.2 | 14.3 | ×1.7 | **OK** |
| overall | 322.8 | 563.2 | ×1.7 | **OK** |
| significantly | 347.5 | 491.5 | ×1.4 | **OK** |
| remarkably | 10.9 | 13.9 | ×1.3 | **OK** |
| robustly | 12.3 | 16.5 | ×1.3 | **OK** |
| furthermore | 236.6 | 277.7 | ×1.2 | **OK** |
| moreover | 253.8 | 238.0 | ×0.9 | **OK** |

## フレーズ
| 項目 | baseline | post_llm | 倍率 | 判定 |
|---|---|---|---|---|
| has garnered | 0.4 | 6.4 | ×16.6 | **BAN** |
| paving the way | 0.6 | 5.2 | ×8.5 | **BAN** |
| in the realm of | 0.9 | 6.7 | ×7.3 | **BAN** |
| plays a crucial role | 2.8 | 13.0 | ×4.6 | **BAN** |
| rapidly evolving | 0.4 | 1.0 | ×2.7 | **BAN** |
| plays a vital role | 1.4 | 3.0 | ×2.2 | **BAN** |
| sheds light on | 0.8 | 0.9 | ×1.1 | **BAN** |
| ever-evolving | 0.1 | 0.1 | ×1.0 | **BAN** |
| a plethora of | 2.2 | 1.5 | ×0.7 | **BAN** |
| myriad | 1.4 | 1.0 | ×0.7 | **BAN** |
| experimental results demonstrate | 18.4 | 62.4 | ×3.4 | **LIMIT** |
| state-of-the-art | 294.8 | 425.4 | ×1.4 | **OK** |
| but also | 114.1 | 144.6 | ×1.3 | **OK** |
| it is important to note | 9.0 | 11.4 | ×1.3 | **OK** |
| a wide range of | 33.9 | 39.3 | ×1.2 | **OK** |
| in recent years | 52.3 | 62.8 | ×1.2 | **OK** |
| it is worth noting | 18.0 | 21.6 | ×1.2 | **OK** |
| not only | 119.8 | 147.3 | ×1.2 | **OK** |
| to the best of our knowledge | 43.6 | 37.4 | ×0.9 | **OK** |
| experimental results show | 60.1 | 46.3 | ×0.8 | **OK** |
| a variety of | 58.7 | 32.8 | ×0.6 | **OK** |
| in this paper | 668.7 | 367.9 | ×0.6 | **OK** |
| in this work | 293.8 | 189.7 | ×0.6 | **OK** |
| on the other hand | 140.9 | 73.3 | ×0.5 | **OK** |
| in other words | 53.6 | 21.1 | ×0.4 | **OK** |
| it should be noted | 23.0 | 10.0 | ×0.4 | **OK** |
| more and more | 12.1 | 4.5 | ×0.4 | **OK** |
| plays an important role | 13.2 | 4.7 | ×0.4 | **OK** |
| remainder of this paper | 13.4 | 5.5 | ×0.4 | **OK** |
| due to the fact that | 22.2 | 6.9 | ×0.3 | **OK** |
| the rest of this paper | 18.9 | 4.5 | ×0.2 | **OK** |

## 記号
| 項目 | baseline | post_llm | 倍率 | 判定 |
|---|---|---|---|---|
| en_dash – | 1021.3 | 3043.6 | ×3.0 | **SURGE** |
| triple_hyphen --- | 3.9 | 11.1 | ×2.9 | **SURGE** |
| double_quote " | 1414.0 | 3910.7 | ×2.8 | **SURGE** |
| em_dash — (Index Terms除く) | 152.8 | 422.1 | ×2.8 | **SURGE** |
| index_terms_template | 208.7 | 362.5 | ×1.7 | **OK** |
| bullet • | 340.9 | 550.5 | ×1.6 | **OK** |
| colon : | 6773.7 | 9893.2 | ×1.5 | **OK** |
| double_hyphen -- | 5.5 | 6.7 | ×1.2 | **OK** |
| percent % | 3066.3 | 3736.1 | ×1.2 | **OK** |
| semicolon ; | 1699.8 | 1898.3 | ×1.1 | **OK** |
| paren ( | 32221.1 | 31412.6 | ×1.0 | **OK** |
