#!/bin/bash
# リポジトリ同梱のスキルを ~/.claude/skills/ にインストールするスクリプト
# Usage: ./scripts/install_skills.sh
# - 既存の同名スキルがある場合は ~/.claude/skills/_backup_YYYYMMDD-HHMMSS/ に退避してから上書き

set -eu
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$HOME/.claude/skills"
STAMP="$(date '+%Y%m%d-%H%M%S')"

mkdir -p "$DEST"

for skill in paper_writing field_literature_survey; do
    if [ -d "$DEST/$skill" ]; then
        mkdir -p "$DEST/_backup_$STAMP"
        cp -r "$DEST/$skill" "$DEST/_backup_$STAMP/"
        echo "既存の $skill を $DEST/_backup_$STAMP/ に退避しました"
    fi
    mkdir -p "$DEST/$skill"
    cp "$REPO_DIR/skills/$skill/"* "$DEST/$skill/"
    echo "インストール完了: $DEST/$skill"
done

echo ""
echo "=== 完了 ==="
echo "Claude Code で /paper_writing や /field_literature_survey として利用できます。"
echo "論文執筆時は speech_style_data.md（実測スタイルデータ）が自動的に参照されます。"
