#!/bin/sh
# restart the play daemon (keeps the route file; start() resumes it)
cd "$(dirname "$0")/../.."
python3 tools/play/run.py '_quit=1' 2>/dev/null; sleep 0.5
(python3 tools/play/daemon.py > work/playthrough/daemon.log 2>&1 &)
sleep 1
