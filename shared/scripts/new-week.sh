#!/usr/bin/env bash
# Usage: ./shared/scripts/new-week.sh <week-number> [topic]
# Example: ./shared/scripts/new-week.sh 3 "Kubernetes intro"
#
# Scaffolds weeks/weekNN/ from shared/templates/ if it doesn't already exist.

set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <week-number 1-26> [topic]" >&2
  exit 1
fi

NUM="$1"
TOPIC="${2:-TBD}"

if ! [[ "$NUM" =~ ^[0-9]+$ ]] || (( NUM < 1 || NUM > 26 )); then
  echo "Error: week number must be 1-26, got '$NUM'" >&2
  exit 1
fi

NN=$(printf "%02d" "$NUM")
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
WEEK_DIR="$ROOT/weeks/week${NN}"
TPL_DIR="$ROOT/shared/templates"

# Date math: week1 = 2026-05-09, +7 days per week.
# Use Python for portable date arithmetic (BSD/GNU date differ).
DATE=$(python3 -c "
from datetime import date, timedelta
print((date(2026, 5, 9) + timedelta(weeks=${NUM} - 1)).isoformat())
")

mkdir -p "$WEEK_DIR/homework" "$WEEK_DIR/demo"

render() {
  sed -e "s/{{NN}}/${NN}/g" \
      -e "s/{{topic}}/${TOPIC}/g" \
      -e "s/{{YYYY-MM-DD}}/${DATE}/g" \
      "$1"
}

if [[ ! -f "$WEEK_DIR/README.md" ]]; then
  render "$TPL_DIR/week-README.md" > "$WEEK_DIR/README.md"
  echo "created $WEEK_DIR/README.md"
fi

if [[ ! -f "$WEEK_DIR/notes.md" ]]; then
  render "$TPL_DIR/week-notes.md" > "$WEEK_DIR/notes.md"
  echo "created $WEEK_DIR/notes.md"
fi

if [[ ! -f "$WEEK_DIR/homework/README.md" ]]; then
  render "$TPL_DIR/homework-README.md" > "$WEEK_DIR/homework/README.md"
  echo "created $WEEK_DIR/homework/README.md"
fi

echo
echo "Week ${NN} scaffolded at: weeks/week${NN}/  (date: ${DATE})"
