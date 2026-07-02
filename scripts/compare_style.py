#!/usr/bin/env python3
"""AI生成テキストと実論文テキストのスタイル指標比較

任意のテキストファイル群について以下を per 1,000 words で算出：
- BAN語（avoid_list準拠の主要語）・LIMIT語の出現率
- 記号（em-dash, セミコロン, 箇条書き, コロン）
- 文長（平均・中央値）・段落長（空行区切り、PDFテキストでは参考値）
- 「人間マーカー」表現（It can be seen / Note that / In other words / On the other hand 等）

Usage: python3 scripts/compare_style.py label1=file1 label2=file2 ...
"""
import re
import statistics
import sys

BAN = '''underscore underscores underscoring pivotal nuanced intricate intricacies delve delves delving
meticulous meticulously showcasing showcases seamless realm harness harnessing harnesses bolster bolsters
cutting-edge groundbreaking fostering fosters empower empowers garnered multifaceted elucidate elucidates'''.split()
LIMIT = 'notably crucial crucially comprehensively seamlessly innovative holistic'.split()
HUMAN = ['it can be seen', 'we can see that', 'note that', 'in other words', 'on the other hand',
         'it should be noted', 'in order to']

def metrics(text: str) -> dict:
    words = re.findall(r"[a-zA-Z][a-zA-Z'\-]*", text)
    n = max(len(words), 1)
    lower = re.sub(r'\s+', ' ', text).lower()
    flat = re.sub(r'\s+', ' ', text)
    sents = [s for s in re.split(r'(?<=[.!?])\s+(?=[A-Z(])', flat) if 4 <= len(s.split()) <= 120]
    slens = [len(s.split()) for s in sents] or [0]
    paras = [p for p in re.split(r'\n\s*\n', text) if len(p.split()) > 10]
    k = 1000 / n
    return {
        'words': n,
        'sent_mean': round(statistics.mean(slens), 1),
        'sent_median': statistics.median(slens),
        'para_count': len(paras),
        'para_mean_words': round(statistics.mean([len(p.split()) for p in paras]), 0) if paras else 0,
        'em_dash/1k': round(text.count('—') * k, 2),
        'semicolon/1k': round(text.count(';') * k, 2),
        'bullet/1k': round((text.count('•') + len(re.findall(r'^\s*[-*]\s', text, re.M))) * k, 2),
        'colon/1k': round(text.count(':') * k, 2),
        'BAN/1k': round(sum(len(re.findall(r'\b' + w + r'\b', lower)) for w in BAN) * k, 2),
        'LIMIT/1k': round(sum(len(re.findall(r'\b' + w + r'\b', lower)) for w in LIMIT) * k, 2),
        'HUMAN/1k': round(sum(lower.count(p) for p in HUMAN) * k, 2),
    }

def main():
    cols = []
    for arg in sys.argv[1:]:
        label, path = arg.split('=', 1)
        cols.append((label, metrics(open(path, errors='replace').read())))
    keys = list(cols[0][1].keys())
    w = max(len(k) for k in keys) + 2
    print(' ' * w + ''.join(f'{l:>14}' for l, _ in cols))
    for k in keys:
        print(f'{k:<{w}}' + ''.join(f'{m[k]:>14}' for _, m in cols))

if __name__ == '__main__':
    main()
