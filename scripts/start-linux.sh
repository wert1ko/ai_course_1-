#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
LOG_DIR="$PROJECT_DIR/logs"

mkdir -p "$LOG_DIR"

if [ -f "$PROJECT_DIR/.env" ]; then
  set -a
  source "$PROJECT_DIR/.env"
  set +a
fi

echo "Starting backend (FastAPI)..."
cd "$PROJECT_DIR/backend"
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 > "$LOG_DIR/backend.log" 2>&1 &
echo "$!" > "$LOG_DIR/backend.pid"

echo "Starting frontend (NextJS)..."
cd "$PROJECT_DIR/frontend"
npm run start -- -p 3000 > "$LOG_DIR/frontend.log" 2>&1 &
echo "$!" > "$LOG_DIR/frontend.pid"

echo "Waiting for services..."
sleep 5
curl -sf http://localhost:8000/health > /dev/null 2>&1 && echo "Backend OK" || echo "Backend check failed"
echo "Done. Backend: http://localhost:8000  Frontend: http://localhost:3000"
