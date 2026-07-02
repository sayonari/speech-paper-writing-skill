#!/usr/bin/env python3
"""コーパス統計分析スクリプト

corpus/<会議>/<年>/ の抽出テキストから以下を集計する：
- 頻出語彙（内容語）・n-gram（2〜4gram）
- 記号使用統計（em-dash, セミコロン, コロン, 箇条書き記号 等）
- 文長分布
- セクション見出しの頻度と章立てパターン
- AI典型表現候補の出現頻度（per million words）

Usage:
    python3 scripts/analyze_corpus.py corpus/ICASSP/2020 [corpus/... ...] --out analysis/ICASSP_2020
"""
import argparse
import csv
import json
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

# ---------- 前処理 ----------

REF_HEADING = re.compile(r'^\s*(?:\d+\.?\s*)?REFERENCES?\s*$', re.IGNORECASE | re.MULTILINE)
ABSTRACT_HEADING = re.compile(r'^\s*ABSTRACT\s*$', re.IGNORECASE | re.MULTILINE)

def load_body(path: Path) -> str | None:
    """本文（ABSTRACT以降〜REFERENCES手前）を取り出し、行末ハイフンを結合する"""
    try:
        text = path.read_text(encoding='utf-8', errors='replace')
    except OSError:
        return None
    if len(text) < 2000:  # 抽出失敗・表紙のみ等は除外
        return None
    m = ABSTRACT_HEADING.search(text)
    start = m.start() if m else 0
    m = REF_HEADING.search(text, start + 100)
    end = m.start() if m else len(text)
    body = text[start:end]
    body = re.sub(r'-\n(?=[a-z])', '', body)   # 行末ハイフネーション結合
    return body

# ---------- 見出し抽出 ----------

# IEEE系（1. INTRODUCTION 全大文字）と ISCA系（1. Introduction タイトルケース）の両方に対応
TOP_HEADING = re.compile(r'^\s*(\d+)\.\s+([A-Z][A-Za-z0-9 ,&\-:/()]{2,58})\s*$', re.MULTILINE)

def _is_heading_like(title: str) -> bool:
    """見出しらしさの判定：全大文字、または内容語の大半が大文字始まり"""
    if title.upper() == title:
        return True
    words = [w for w in re.split(r'[ \-/]', title) if w]
    if not 1 <= len(words) <= 8:
        return False
    minor = {'and', 'or', 'of', 'the', 'a', 'an', 'in', 'on', 'for', 'with', 'to', 'from', 'by'}
    caps = sum(1 for w in words if w[0].isupper() or w.lower() in minor or w[0].isdigit())
    return caps == len(words)

def extract_headings(body: str) -> list[str]:
    """トップレベル見出し（例: '1. INTRODUCTION' / '1. Introduction'）を番号順に返す"""
    found = []
    for m in TOP_HEADING.finditer(body):
        num, title = int(m.group(1)), m.group(2).strip()
        if 1 <= num <= 12 and _is_heading_like(title):
            found.append((m.start(), num, re.sub(r'\s+', ' ', title)))
    # 番号が単調増加する最長の並びだけ残す（本文中の誤マッチ除去の簡易策）
    seq = []
    for _, num, title in found:
        if not seq or num == seq[-1][0] + 1:
            seq.append((num, title))
        elif num == 1:
            seq = [(num, title)]
    return [t for _, t in seq]

# ---------- トークン化・文分割 ----------

STOPWORDS = set('''a an the and or but if then else of in on at by for with to from as is are was were be been being
this that these those it its we our us they their them he she his her which who whom whose what when where why how
not no nor so such than too very can could may might must shall should will would do does did done have has had
having there here also into over under between among through during about above below after before more most other
some any each few both all only own same s t don now d ll m o re ve y i you your yours per via et al eq fig table
section results one two three using used use based given first second respectively proposed method model approach
paper show shown shows''' .split())

WORD_RE = re.compile(r"[a-zA-Z][a-zA-Z'\-]{1,}")
SENT_SPLIT = re.compile(r'(?<=[.!?])\s+(?=[A-Z(])')

def tokenize(body: str) -> list[str]:
    return [w.lower() for w in WORD_RE.findall(body)]

def sentences(body: str) -> list[str]:
    flat = re.sub(r'\s+', ' ', body)
    sents = SENT_SPLIT.split(flat)
    return [s for s in sents if 4 <= len(s.split()) <= 120]

# ---------- AI典型表現候補 ----------

AI_WORDS = '''delve delves delving tapestry pivotal crucial crucially meticulous meticulously showcase showcases
showcasing underscore underscores underscoring notably remarkably seamlessly seamless holistic multifaceted
intricate intricacies nuanced foster fosters fostering bolster bolsters garner garners garnered realm landscape
paradigm comprehensively robustly innovative groundbreaking cutting-edge noteworthy elucidate elucidates
harness harnesses harnessing empower empowers unveil unveils moreover furthermore additionally consequently
overall vital essential significantly'''.split()
AI_WORDS = list(dict.fromkeys(AI_WORDS))  # 重複除去（順序保持）

AI_PHRASES = [
    'it is worth noting', 'it should be noted', 'plays a crucial role', 'plays a vital role',
    'plays an important role', 'in the realm of', 'a wide range of', 'a variety of', 'has garnered',
    'in recent years', 'more and more', 'state-of-the-art', 'to the best of our knowledge',
    'experimental results show', 'experimental results demonstrate', 'the rest of this paper',
    'remainder of this paper', 'not only', 'but also', 'in this paper', 'in this work',
    'in other words', 'on the other hand', 'due to the fact that', 'it is important to note',
    'paving the way', 'sheds light on', 'a plethora of', 'myriad', 'ever-evolving', 'rapidly evolving',
]

# ---------- メイン ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('corpus_dirs', nargs='+')
    ap.add_argument('--out', required=True)
    ap.add_argument('--top', type=int, default=300)
    ap.add_argument('--prune-interval', type=int, default=0,
                    help='Nファイルごとにcount==1のn-gramを破棄（大規模コーパスのメモリ対策。頻度上位リストへの影響は無視できる）')
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    uni, bi, tri, four = Counter(), Counter(), Counter(), Counter()
    headings_counter = Counter()
    structures = Counter()
    ai_word_counts = Counter()
    ai_phrase_counts = Counter()
    punct = Counter()
    sent_lengths = []
    total_words = 0
    total_sents = 0
    n_papers = 0

    files = []
    for d in args.corpus_dirs:
        files.extend(sorted(Path(d).glob('*.txt')))
    print(f'入力ファイル数: {len(files)}', file=sys.stderr)

    for i, f in enumerate(files):
        body = load_body(f)
        if body is None:
            continue
        n_papers += 1
        lower = re.sub(r'\s+', ' ', body).lower()

        toks = tokenize(body)
        total_words += len(toks)
        uni.update(t for t in toks if t not in STOPWORDS and len(t) > 2)
        bi.update(zip(toks, toks[1:]))
        tri.update(zip(toks, toks[1:], toks[2:]))
        four.update(zip(toks, toks[1:], toks[2:], toks[3:]))

        sents = sentences(body)
        total_sents += len(sents)
        sent_lengths.extend(len(s.split()) for s in sents)

        # 記号
        # 「Index Terms—」はICASSP/IEEEテンプレの定型なので本文のem-dash使用とは区別する
        punct['em_dash — (Index Terms除く)'] += body.count('—') - len(re.findall(r'Index Terms\s*—', body))
        punct['index_terms_template'] += len(re.findall(r'Index Terms\s*—', body))
        punct['en_dash –'] += body.count('–')
        punct['double_hyphen --'] += len(re.findall(r'(?<!-)--(?!-)', body))
        punct['triple_hyphen ---'] += body.count('---')
        punct['semicolon ;'] += body.count(';')
        punct['colon :'] += body.count(':')
        punct['paren ('] += body.count('(')
        punct['bullet •'] += body.count('•')
        punct['double_quote "'] += body.count('"') + body.count('“')
        punct['percent %'] += body.count('%')

        hs = extract_headings(body)
        if len(hs) >= 3:
            headings_counter.update(h.upper() for h in hs)
            structures[' > '.join(h.upper() for h in hs)] += 1

        for w in AI_WORDS:
            c = len(re.findall(r'\b' + re.escape(w) + r'\b', lower))
            if c:
                ai_word_counts[w] += c
        for p in AI_PHRASES:
            c = lower.count(p)
            if c:
                ai_phrase_counts[p] += c

        if (i + 1) % 200 == 0:
            print(f'  {i+1}/{len(files)} processed', file=sys.stderr)
        if args.prune_interval and (i + 1) % args.prune_interval == 0:
            for c in (bi, tri, four):
                for k in [k for k, v in c.items() if v == 1]:
                    del c[k]

    mw = total_words / 1e6 if total_words else 1

    def write_csv(name, rows, header):
        with open(out / name, 'w', newline='') as fh:
            w = csv.writer(fh)
            w.writerow(header)
            w.writerows(rows)

    write_csv('unigrams.csv', [(w, c, round(c / mw, 1)) for w, c in uni.most_common(args.top)],
              ['word', 'count', 'per_million'])
    write_csv('bigrams.csv', [(' '.join(g), c, round(c / mw, 1)) for g, c in bi.most_common(args.top)],
              ['ngram', 'count', 'per_million'])
    write_csv('trigrams.csv', [(' '.join(g), c, round(c / mw, 1)) for g, c in tri.most_common(args.top)],
              ['ngram', 'count', 'per_million'])
    write_csv('fourgrams.csv', [(' '.join(g), c, round(c / mw, 1)) for g, c in four.most_common(args.top)],
              ['ngram', 'count', 'per_million'])
    write_csv('headings.csv', headings_counter.most_common(200), ['heading', 'count'])
    write_csv('structures.csv', structures.most_common(100), ['structure', 'count'])
    write_csv('ai_markers_words.csv',
              sorted(((w, ai_word_counts.get(w, 0), round(ai_word_counts.get(w, 0) / mw, 2)) for w in AI_WORDS),
                     key=lambda r: -r[1]),
              ['word', 'count', 'per_million'])
    write_csv('ai_markers_phrases.csv',
              sorted(((p, ai_phrase_counts.get(p, 0), round(ai_phrase_counts.get(p, 0) / mw, 2)) for p in AI_PHRASES),
                     key=lambda r: -r[1]),
              ['phrase', 'count', 'per_million'])
    write_csv('punctuation.csv',
              [(k, v, round(v / mw, 1), round(v / n_papers, 2)) for k, v in punct.most_common()],
              ['symbol', 'count', 'per_million_words', 'per_paper'])

    summary = {
        'papers': n_papers,
        'total_words': total_words,
        'total_sentences': total_sents,
        'sent_len_mean': round(statistics.mean(sent_lengths), 1) if sent_lengths else 0,
        'sent_len_median': statistics.median(sent_lengths) if sent_lengths else 0,
        'sent_len_p90': sorted(sent_lengths)[int(len(sent_lengths) * 0.9)] if sent_lengths else 0,
        'semicolons_per_sentence': round(punct['semicolon ;'] / total_sents, 3) if total_sents else 0,
        'em_dash_per_paper': round(punct['em_dash — (Index Terms除く)'] / n_papers, 2) if n_papers else 0,
    }
    (out / 'summary.json').write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))

if __name__ == '__main__':
    main()
