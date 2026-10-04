#!/bin/sh
# restart the play daemon (keeps the route file; start() resumes it)
#   tools/play/restart.sh [game] [--en]   (default: $BBK_GAME or fmj; --en plays the English build)
cd "$(dirname "$0")/../.."
G="${1:-${BBK_GAME:-fmj}}"
[ $# -gt 0 ] && shift
DIR=$(python3 -c "from bbkrpg import games; print(games.get('$G').playthrough)") || exit 1
mkdir -p "$DIR"
python3 tools/play/run.py --game "$G" '_quit=1' 2>/dev/null; sleep 0.5
(python3 tools/play/daemon.py --game "$G" "$@" > "$DIR/daemon.log" 2>&1 &)
sleep 1
