#!/usr/bin/env python3
"""年次推移レポート生成

analysis/<会議>_<年>/ の出力（summary.json, ai_markers_*.csv, punctuation.csv）を集約し、
AI典型語・記号使用の年次推移テーブル（Markdown + CSV）を生成する。

Usage:
    python3 scripts/trend_report.py --conf ICASSP --out analysis/trends_ICASSP.md
"""
import argparse
import csv
import json
import re
from pathlib import Path

def read_csv_map(path: Path, key_col: str, val_col: str) -> dict:
    if not path.exists():
        return {}
    with open(path) as f:
        rows = list(csv.DictReader(f))
    return {r[key_col]: float(r[val_col]) for r in rows}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--conf', required=True)
    ap.add_argument('--analysis-dir', default='analysis')
    ap.add_argument('--out', required=True)
    ap.add_argument('--min-peak', type=float, default=2.0,
                    help='全年で per_million がこの値未満の語は表から省略')
    args = ap.parse_args()

    adir = Path(args.analysis_dir)
    years = []
    for d in sorted(adir.glob(f'{args.conf}_*')):
        m = re.match(rf'{args.conf}_(\d{{4}})$', d.name)
        if m and (d / 'summary.json').exists():
            years.append((int(m.group(1)), d))
    if not years:
        raise SystemExit(f'no analysis dirs for {args.conf}')

    summaries = {y: json.loads((d / 'summary.json').read_text()) for y, d in years}
    word_maps = {y: read_csv_map(d / 'ai_markers_words.csv', 'word', 'per_million') for y, d in years}
    phrase_maps = {y: read_csv_map(d / 'ai_markers_phrases.csv', 'phrase', 'per_million') for y, d in years}
    punct_maps = {}
    for y, d in years:
        pm = {}
        if (d / 'punctuation.csv').exists():
            with open(d / 'punctuation.csv') as f:
                for r in csv.DictReader(f):
                    pm[r['symbol']] = float(r['per_million_words'])
        punct_maps[y] = pm

    ys = [y for y, _ in years]
    lines = [f'# {args.conf} 年次推移レポート', '',
             '各セルは per million words（記号・語・フレーズ）。生成: scripts/trend_report.py', '']

    lines.append('## コーパス規模')
    lines.append('| 年 | 論文数 | 総語数 | 平均文長 | セミコロン/文 |')
    lines.append('|---' * 5 + '|')
    for y in ys:
        s = summaries[y]
        lines.append(f"| {y} | {s['papers']} | {s['total_words']:,} | {s['sent_len_mean']} | {s['semicolons_per_sentence']} |")
    lines.append('')

    def table(title, maps, all_keys):
        rows = []
        for k in all_keys:
            vals = [maps[y].get(k, 0.0) for y in ys]
            if max(vals) < args.min_peak:
                continue
            rows.append((k, vals))
        # 直近年/初年の比率（増加率）でソート
        def ratio(vals):
            base = max(vals[0], 0.1)
            return vals[-1] / base
        rows.sort(key=lambda r: -ratio(r[1]))
        out = [f'## {title}', '', '| 項目 | ' + ' | '.join(map(str, ys)) + ' | 増減率(末年/初年) |',
               '|---' * (len(ys) + 2) + '|']
        for k, vals in rows:
            r = ratio(vals)
            out.append(f'| {k} | ' + ' | '.join(f'{v:.1f}' for v in vals) + f' | ×{r:.1f} |')
        out.append('')
        return out

    all_words = sorted({k for m in word_maps.values() for k in m})
    all_phrases = sorted({k for m in phrase_maps.values() for k in m})
    all_puncts = sorted({k for m in punct_maps.values() for k in m})

    lines += table('AI典型語の推移（増加率順）', word_maps, all_words)
    lines += table('AI典型フレーズの推移（増加率順）', phrase_maps, all_phrases)
    lines += table('記号使用の推移（増加率順）', punct_maps, all_puncts)

    Path(args.out).write_text('\n'.join(lines))
    print(f'wrote {args.out} ({len(ys)} years)')

if __name__ == '__main__':
    main()
