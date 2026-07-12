from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from pathlib import Path
from app.database import init_db
from app.routes.auth import router as auth_router
from app.routes.nda import router as nda_router

BASE_DIR = Path(__file__).resolve().parent.parent.parent
FRONTEND_OUT = BASE_DIR / "frontend" / "out"


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="Prelegal API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(nda_router)

# Serve static assets only (these paths can't conflict with API routes)
if FRONTEND_OUT.exists():
    app.mount("/_next", StaticFiles(directory=str(FRONTEND_OUT / "_next"), html=False))


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/{path:path}")
async def serve_frontend(request: Request, path: str):
    """
    Serve the correct pre-built HTML for Next.js routes (SPA).
    Fall back to index.html for client-side navigation.
    """
    if FRONTEND_OUT.exists():
        # Check if the requested path has a pre-built HTML file
        for candidate in [FRONTEND_OUT / f"{path}.html", FRONTEND_OUT / path]:
            if candidate.exists() and candidate.is_file():
                return FileResponse(str(candidate))
        # Fallback to index.html for client-side routing
        index = FRONTEND_OUT / "index.html"
        if index.exists():
            return FileResponse(str(index))
    return HTMLResponse("<h1>404 — Not found</h1>", status_code=404)


@app.get("/")
async def root():
    if FRONTEND_OUT.exists():
        return FileResponse(str(FRONTEND_OUT / "index.html"))
    return HTMLResponse("<h1>Prelegal API</h1>")
