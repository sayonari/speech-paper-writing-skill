# 参考文献実在検証記録（paper/main.tex）

検証日: 2026-07-02 / 方法: Web検索で出版元ページ・arXiv・proceedingsを照合（paper_writing スキル §3.1準拠）

| cite key | 検証結果 | 確認した出典 |
|---|---|---|
| liang2024 | ✅ 実在 | ICML 2024 (PMLR v235, liang24b)・arXiv:2403.07183。著者 Weixin Liang, Zachary Izzo, Yaohui Zhang ほか。ICML 2024 Oral。https://proceedings.mlr.press/v235/liang24b.html |
| gray2024 | ✅ 実在 | arXiv:2403.16887（2024-03-25投稿）。Andrew Gray, UCL。記載のarXiv番号も一致。https://arxiv.org/abs/2403.16887 |
| kobak2024 | ✅ 実在 | Science Advances, vol. 11, no. 27, eadt3813 (2025)。著者 Kobak, González-Márquez, Horvát, Lause。巻号まで本文引用と一致。https://www.science.org/doi/10.1126/sciadv.adt3813 |
| juzek2025 | ✅ 実在 | Proceedings of the 31st International Conference on Computational Linguistics (COLING 2025)。Tom S. Juzek and Zina B. Ward。arXiv:2412.11385。 |

## 本文中の主張と出典の対応
- 「recent scholarly text の相当割合がLLM生成/編集を含む」→ liang2024（査読文の6.5–16.9%）、gray2024（2023年論文の1%超・6万本以上）: 出典の主張範囲内 ✅
- 「biomedical abstracts と general scholarly corpora での先行定量研究」→ kobak2024（PubMed 1,500万abstract、2024年の13.5%以上がLLM処理と推定）、gray2024、juzek2025 ✅
- AI典型語候補リストの出所 → kobak2024（delve, underscore等）、juzek2025（delve, explore, robust等の過剰使用） ✅
