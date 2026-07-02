#!/bin/bash
# ISCA Archive から Interspeech proceedings を収集するスクリプト
# Usage: ./download_isca.sh <year>   (例: ./download_isca.sh 2024)
# - _ref/papers/InterSpeech/<year>/ に index.html / 各論文HTML / 各論文PDF を保存
# - 既存ファイル（サイズ>0）はスキップするので中断・再開可能
# - サーバ負荷軽減のためリクエスト間に0.3秒スリープ

set -u
YEAR="${1:?year required (e.g. 2024)}"
BASE="https://www.isca-archive.org/interspeech_${YEAR}"
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$PROJECT_DIR/_ref/papers/InterSpeech/$YEAR"
mkdir -p "$DEST"

UA="Mozilla/5.0 (academic-archive-mirror; contact: sayonari@gmail.com)"

fetch() { # fetch <url> <outfile>
    local url="$1" out="$2"
    if [ -s "$out" ]; then return 0; fi
    curl -sf --retry 3 --retry-delay 5 -A "$UA" "$url" -o "$out.tmp" && mv "$out.tmp" "$out"
    local rc=$?
    sleep 0.3
    return $rc
}

echo "=== Interspeech $YEAR : index取得 ==="
fetch "$BASE/index.html" "$DEST/index.html" || { echo "ERROR: index取得失敗"; exit 1; }

# 論文ページのリンクを抽出（相対リンク *_interspeech.html 形式）
grep -oE 'href="[^"/]+_interspeech\.html"' "$DEST/index.html" \
    | sed -E 's/^href="//; s/"$//' | sort -u > "$DEST/.paper_list.txt"

TOTAL=$(wc -l < "$DEST/.paper_list.txt" | tr -d ' ')
echo "論文数: $TOTAL"

N=0
FAIL=0
while read -r page; do
    N=$((N+1))
    pdf="${page%.html}.pdf"
    fetch "$BASE/$page" "$DEST/$page" || { echo "FAIL html: $page"; FAIL=$((FAIL+1)); }
    fetch "$BASE/$pdf"  "$DEST/$pdf"  || { echo "FAIL pdf : $pdf";  FAIL=$((FAIL+1)); }
    if [ $((N % 50)) -eq 0 ]; then echo "[$YEAR] $N / $TOTAL done (fail: $FAIL)"; fi
done < "$DEST/.paper_list.txt"

echo "=== Interspeech $YEAR 完了: $N 論文処理, 失敗 $FAIL 件 ==="
