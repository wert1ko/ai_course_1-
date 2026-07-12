#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$(dirname "$SCRIPT_DIR")/logs"

for svc in backend frontend; do
  pidf="$LOG_DIR/${svc}.pid"
  [ -f "$pidf" ] && pid=$(cat "$pidf") && kill "$pid" 2>/dev/null || true
  rm -f "$pidf"
done
echo "Stopped."
