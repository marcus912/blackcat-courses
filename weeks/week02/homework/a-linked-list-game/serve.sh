#!/usr/bin/env bash
# Serve the Cache Crash sandbox on http://localhost:PORT
# Usage:  ./serve.sh           # default port 8000
#         ./serve.sh 9000      # custom port

set -euo pipefail

PORT="${1:-8000}"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Serving $DIR"
echo "Open http://localhost:$PORT/"
echo "Press Ctrl+C to stop."
cd "$DIR"
exec python3 -m http.server "$PORT"
