#!/bin/bash
# ISCA ArchiveからWeb収集したInterspeech年度を研究室NASへバックアップ（書き戻し）するスクリプト
# Usage: ./backup_to_nas.sh <year> [<year> ...]   (例: ./backup_to_nas.sh 2024 2025)
# - ローカル _ref/papers/InterSpeech/<year>/ → NAS INTERSPEECH/<year>/
# - rsyncなので再実行可能。NAS側の既存ファイルは上書きしない(--ignore-existing)

set -u
NAS_HOST="nishimura@133.15.57.7"
NAS_BASE="/volume1/Kitaoka_lab/Proceedings/INTERSPEECH"
SSH_CMD="ssh -o ControlPath=/Users/sayonari/.ssh/cm/%r@%h:%p -o BatchMode=yes"
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SRC_BASE="$PROJECT_DIR/_ref/papers/InterSpeech"

for YEAR in "$@"; do
    src="$SRC_BASE/$YEAR"
    if [ ! -d "$src" ]; then echo "SKIP (not found): $src"; continue; fi
    echo "=== $(date '+%H:%M:%S') backup start: InterSpeech $YEAR → NAS ==="
    $SSH_CMD "$NAS_HOST" "mkdir -p '$NAS_BASE/$YEAR'"
    rsync -a --partial --ignore-existing \
        --exclude='.paper_list.txt' --exclude='._*' --exclude='.DS_Store' \
        -e "$SSH_CMD" "$src/" "$NAS_HOST:$NAS_BASE/$YEAR/"
    echo "=== $(date '+%H:%M:%S') backup done : InterSpeech $YEAR (exit $?) ==="
done
