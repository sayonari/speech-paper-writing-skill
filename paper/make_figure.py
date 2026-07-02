#!/usr/bin/env python3
"""論文Fig.1生成: em-dashとnotablyの26年推移（両会議）
Usage: python3 paper/make_figure.py   （プロジェクトルートで実行）
"""
import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
A = ROOT / 'analysis'

def series(conf, fname, key, col):
    xs, ys = [], []
    for d in sorted(A.glob(f'{conf}_2*')):
        year = int(d.name.rsplit('_', 1)[1])
        f = d / fname
        if not f.exists():
            continue
        for r in csv.DictReader(open(f)):
            if r[list(r)[0]] == key:
                xs.append(year)
                ys.append(float(r[col]))
                break
    return xs, ys

# Okabe-Ito由来のCVD安全ペア（validate_palette.js で検証済み）
C_ICASSP, C_IS = '#0072B2', '#D55E00'

fig, axes = plt.subplots(2, 1, figsize=(3.35, 3.05), sharex=True, dpi=300)
plt.rcParams.update({'font.size': 8})

panels = [
    ('punctuation.csv', 'em_dash — (Index Terms除く)', 'per_million_words', 'Em-dashes / million words'),
    ('ai_markers_words.csv', 'notably', 'per_million', '"notably" / million words'),
]
for ax, (fname, key, col, ylabel) in zip(axes, panels):
    for conf, color, marker, ls, label in [('ICASSP', C_ICASSP, 'o', '-', 'ICASSP'),
                                           ('InterSpeech', C_IS, 's', '--', 'Interspeech')]:
        xs, ys = series(conf, fname, key, col)
        ax.plot(xs, ys, color=color, marker=marker, linestyle=ls, linewidth=1.4,
                markersize=3, label=label)
    ax.axvline(2022.9, color='#888888', linewidth=0.8, linestyle=':')
    ax.set_ylabel(ylabel, fontsize=8)
    ax.tick_params(labelsize=7)
    ax.grid(True, linewidth=0.3, alpha=0.4)
    ax.set_ylim(bottom=0)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)

axes[0].annotate('ChatGPT\nrelease', xy=(2022.9, 420), fontsize=6.5, ha='right',
                 xytext=(2021.2, 380), color='#555555')
axes[0].legend(fontsize=7, frameon=False, loc='upper left')
axes[1].set_xlabel('Proceedings year', fontsize=8)
axes[1].set_xticks(range(2001, 2027, 5))

fig.tight_layout(pad=0.4)
out = ROOT / 'paper' / 'fig_trends.pdf'
fig.savefig(out, bbox_inches='tight')
print(f'wrote {out}')
