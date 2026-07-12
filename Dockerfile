FROM python:3.11-slim AS backend-builder
WORKDIR /app
COPY backend/pyproject.toml backend/
RUN pip install uv && uv sync --frozen

FROM node:20-alpine AS frontend-builder
WORKDIR /app
COPY frontend/package.json frontend/package-lock.json frontend/
RUN npm ci && npm run build

FROM backend-builder AS runner
WORKDIR /app
COPY --from=frontend-builder /app/frontend/out ./frontend/out
COPY backend/ ./backend/
COPY catalog.json ./
ENV PYTHONPATH=/app
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
