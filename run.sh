"#!/usr/bin/env bash
# Termux / VPS auto-restart wrapper
cd \"$(dirname \"$0\")\"

if [ -d \"venv\" ]; then
    # shellcheck disable=SC1091
    source venv/bin/activate
fi

if [ -f \".env\" ]; then
    set -a
    # shellcheck disable=SC1091
    source .env
    set +a
fi

MAX_BACKOFF=60
BACKOFF=2

echo \"🚀 Clone Bot Maker — launcher\"
while true; do
    python -m bot.main
    EXIT=$?
    echo \"⚠️  Bot exited (code $EXIT). Restart in ${BACKOFF}s...\"
    sleep \"$BACKOFF\"
    BACKOFF=$(( BACKOFF * 2 ))
    if [ \"$BACKOFF\" -gt \"$MAX_BACKOFF\" ]; then BACKOFF=$MAX_BACKOFF; fi
done
"
