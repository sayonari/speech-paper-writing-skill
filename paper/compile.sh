#!/bin/bash
# ショーケース論文のコンパイルスクリプト（英語・pdflatex）
# Usage: ./compile.sh
cd "$(dirname "$0")"

rm -f main.aux main.log main.out main.toc main.synctex.gz

pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
pdflatex -interaction=nonstopmode -halt-on-error main.tex

EXIT_CODE=$?
echo ""
echo "=== Compile finished ==="
if [ -f main.pdf ]; then
    echo "Output: main.pdf (succeeded)"
    pdftotext main.pdf - 2>/dev/null | head -3
else
    echo "Error: main.pdf was not produced. See main.log."
    exit $EXIT_CODE
fi
