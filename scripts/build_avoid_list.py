#!/usr/bin/env python3
"""「避ける表現」確定リストの合成

各AI典型語・フレーズ・記号について：
- baseline: 第1層コア年度（2015-2022、ICASSP+InterSpeech）の加重平均 per_million ＝「人間の適正頻度」
- post_llm: 2024-2026（ICASSP、後にInterSpeech 2024/2025追加可）の加重平均 per_million
- surge = post_llm / baseline

分類ルール：
- baseline < 3/M               → BAN     「人間はそもそも使わない語。使ったら即AI臭」
- baseline ≥ 3 かつ surge ≥ 3  → LIMIT   「人間も使うがLLM後に急増。適正頻度を守る」
- surge ≥ 2                    → WATCH   「増加傾向。多用注意」
- それ以外                      → OK      「通常の使用は問題なし」

Usage: python3 scripts/build_avoid_list.py --out analysis/avoid_list.md
"""
import argparse
import csv
import json
from pathlib import Path

BASELINE_DIRS = [f'ICASSP_{y}' for y in range(2015, 2023)] + \
                [f'InterSpeech_{y}' for y in range(2015, 2023)]
POSTLLM_DIRS = [f'ICASSP_{y}' for y in (2024, 2025, 2026)]

def weighted_pm(adir: Path, dirs: list[str], fname: str, key_col: str):
    """複数年の per_million を総語数で加重平均"""
    totals, weights = {}, {}
    for d in dirs:
        p = adir / d
        if not (p / 'summary.json').exists():
            continue
        words = json.loads((p / 'summary.json').read_text())['total_words']
        f = p / fname
        if not f.exists():
            continue
        for r in csv.DictReader(open(f)):
            k = r[key_col]
            pm_col = 'per_million' if 'per_million' in r else 'per_million_words'
            totals[k] = totals.get(k, 0) + float(r[pm_col]) * words
            weights[k] = weights.get(k, 0) + words
    return {k: totals[k] / weights[k] for k in totals}

def classify(base: float, post: float) -> tuple[str, float]:
    surge = post / max(base, 0.1)
    if base < 3:
        return 'BAN', surge
    if surge >= 3:
        return 'LIMIT', surge
    if surge >= 2:
        return 'WATCH', surge
    return 'OK', surge

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--analysis-dir', default='analysis')
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    adir = Path(args.analysis_dir)

    sections = []
    for title, fname, key in [('語', 'ai_markers_words.csv', 'word'),
                              ('フレーズ', 'ai_markers_phrases.csv', 'phrase'),
                              ('記号', 'punctuation.csv', 'symbol')]:
        base = weighted_pm(adir, BASELINE_DIRS, fname, key)
        post = weighted_pm(adir, POSTLLM_DIRS, fname, key)
        rows = []
        for k in sorted(set(base) | set(post)):
            b, p = base.get(k, 0.0), post.get(k, 0.0)
            if title == '記号':  # 記号はBAN分類の閾値が意味を持たないので増加率のみ
                verdict = 'SURGE' if p / max(b, 0.1) >= 2 else 'OK'
                surge = p / max(b, 0.1)
            else:
                verdict, surge = classify(b, p)
            rows.append((k, round(b, 1), round(p, 1), round(surge, 1), verdict))
        order = {'BAN': 0, 'LIMIT': 1, 'SURGE': 1, 'WATCH': 2, 'OK': 3}
        rows.sort(key=lambda r: (order[r[4]], -r[3]))
        sections.append((title, rows))

    lines = ['# 「避ける表現」確定リスト（データ根拠付き）', '',
             '- baseline: 2015–2022 ICASSP+InterSpeech 加重平均 per million words（人間の適正頻度）',
             '- post_llm: 2024–2026 ICASSP 加重平均 per million words',
             '- BAN=人間はそもそも使わない / LIMIT=適正頻度を超えるな / WATCH=多用注意 / OK=問題なし', '']
    for title, rows in sections:
        lines.append(f'## {title}')
        lines.append('| 項目 | baseline | post_llm | 倍率 | 判定 |')
        lines.append('|---|---|---|---|---|')
        for k, b, p, s, v in rows:
            lines.append(f'| {k} | {b} | {p} | ×{s} | **{v}** |')
        lines.append('')
    Path(args.out).write_text('\n'.join(lines))
    print(f'wrote {args.out}')

if __name__ == '__main__':
    main()
