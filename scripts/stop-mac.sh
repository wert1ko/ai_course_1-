#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$(dirname "$SCRIPT_DIR")/logs"

stop_service() {
  local name="$1"
  local pid_file="$LOG_DIR/${name}.pid"
  if [ -f "$pid_file" ]; then
    local pid=$(cat "$pid_file")
    if kill -0 "$pid" 2>/dev/null; then
      echo "Stopping $name (PID $pid)..."
      kill "$pid"
      sleep 2
      # Force kill if still alive
      kill -9 "$pid" 2>/dev/null || true
    else
      echo "$name already stopped."
    fi
    rm -f "$pid_file"
  else
    echo "$name PID file not found."
  fi
}

stop_service "backend"
stop_service "frontend"
echo "All services stopped."
