#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
LOG_DIR="$PROJECT_DIR/logs"

mkdir -p "$LOG_DIR"

# Load .env if present
if [ -f "$PROJECT_DIR/.env" ]; then
  set -a
  source "$PROJECT_DIR/.env"
  set +a
fi

echo "Starting backend (FastAPI)..."
cd "$PROJECT_DIR/backend"
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 > "$LOG_DIR/backend.log" 2>&1 &
BACKEND_PID=$!
echo "$BACKEND_PID" > "$LOG_DIR/backend.pid"
echo "Backend PID: $BACKEND_PID"

echo "Starting frontend (NextJS)..."
cd "$PROJECT_DIR/frontend"
npm run start -- -p 3000 > "$LOG_DIR/frontend.log" 2>&1 &
FRONTEND_PID=$!
echo "$FRONTEND_PID" > "$LOG_DIR/frontend.pid"
echo "Frontend PID: $FRONTEND_PID"

echo "Waiting for services to come up..."
sleep 5

# Health check backend
if curl -sf http://localhost:8000/health > /dev/null 2>&1; then
  echo "Backend ready at http://localhost:8000"
else
  echo "WARNING: Backend health check failed. See logs/backend.log"
fi

echo "Done. Backend: http://localhost:8000  Frontend: http://localhost:3000"
echo "PIDs saved in $LOG_DIR/"
