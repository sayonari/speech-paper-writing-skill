#!/bin/bash
# _ref/papers/<会議>/<年>/ 配下のPDFをテキスト化して corpus/<会議>/<年>/ に保存
# Usage: ./extract_text.sh <会議> <年>   (例: ./extract_text.sh ICASSP 2020)
# - 抽出済み（.txtが存在しサイズ>0）はスキップ → 再実行可能
# - InterspeechのNAS由来PDFは大文字.PDFがあるため -iname で検索

set -u
CONF="${1:?conference required}"
YEAR="${2:?year required}"
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$PROJECT_DIR/_ref/papers/$CONF/$YEAR"
DEST="$PROJECT_DIR/corpus/$CONF/$YEAR"
mkdir -p "$DEST"

N=0; SKIP=0; FAIL=0
while IFS= read -r -d '' pdf; do
    base=$(basename "$pdf")
    out="$DEST/${base%.*}.txt"
    if [ -s "$out" ]; then SKIP=$((SKIP+1)); continue; fi
    if pdftotext -q "$pdf" "$out" 2>/dev/null && [ -s "$out" ]; then
        N=$((N+1))
    else
        rm -f "$out"; FAIL=$((FAIL+1)); echo "FAIL: $pdf"
    fi
    if [ $(( (N + SKIP + FAIL) % 200 )) -eq 0 ]; then echo "progress: ok=$N skip=$SKIP fail=$FAIL"; fi
done < <(find "$SRC" -iname "*.pdf" -type f -print0)

echo "=== $CONF/$YEAR 抽出完了: ok=$N skip=$SKIP fail=$FAIL ==="
