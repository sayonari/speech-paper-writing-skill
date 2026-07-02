#!/bin/bash
# 研究室NAS (Synology) から対象年度を _ref/papers/ へ同期するスクリプト【SSH経由rsync版】
# Usage: ./sync_nas.sh
# 前提: SSH ControlMaster接続が確立済みであること
#   （~/.ssh/cm/nishimura@133.15.57.7:22 のソケットが生きていること。
#     切れていたら ssh -o ControlMaster=yes -o ControlPath=~/.ssh/cm/%r@%h:%p \
#     -o ControlPersist=8h -fN nishimura@133.15.57.7 で再確立）
# - rsyncなので中断・再開可能。コピー済みファイルはスキップされる
# - SMB経由（約0.1〜2.5MB/s）に対しSSH経由は約7MB/s（2026-07-02計測）

set -u
NAS_HOST="nishimura@133.15.57.7"
NAS_BASE="/volume1/Kitaoka_lab/Proceedings"
SSH_CMD="ssh -o ControlPath=/Users/sayonari/.ssh/cm/%r@%h:%p -o BatchMode=yes"
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DEST_BASE="$PROJECT_DIR/_ref/papers"

RSYNC_OPTS=(-a --partial --exclude='@eaDir' --exclude='._*' --exclude='.DS_Store' --exclude='Thumbs.db')

sync_year() { # sync_year <NAS側会議名> <ローカル側会議名> <year>
    local src="$NAS_BASE/$1/$3" dest="$DEST_BASE/$2/$3"
    mkdir -p "$dest"
    echo "=== $(date '+%H:%M:%S') sync start: $1/$3 ==="
    rsync "${RSYNC_OPTS[@]}" -e "$SSH_CMD" "$NAS_HOST:$src/" "$dest/"
    echo "=== $(date '+%H:%M:%S') sync done : $1/$3 (exit $?) ==="
}

# ICASSP 全年度（NASにあるのは2001-2026）
for y in $(seq 2001 2026); do
    sync_year ICASSP ICASSP "$y"
done

# INTERSPEECH 全年度（NASは2007-2017,2019-2023。2018はNASに無し、2020はNASに論文PDFなし
# → 2018/2020/2024/2025 はISCA Archiveから取得）
for y in $(seq 2007 2017) $(seq 2019 2023); do
    sync_year INTERSPEECH InterSpeech "$y"
done

echo "=== 全同期完了 $(date '+%Y-%m-%d %H:%M:%S') ==="
