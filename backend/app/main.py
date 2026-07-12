from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from pathlib import Path
from app.database import init_db
from app.routes.auth import router as auth_router
from app.routes.nda import router as nda_router

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # project root
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

# Serve static assets explicitly — avoids catching API routes
if FRONTEND_OUT.exists():
    app.mount("/_next", StaticFiles(directory=str(FRONTEND_OUT / "_next"), html=False), name="next_static")
    app.mount("/favicon.ico", StaticFiles(directory=str(FRONTEND_OUT), html=False), name="favicon")
    app.mount("/next.svg", StaticFiles(directory=str(FRONTEND_OUT), html=False), name="next_svg")
    app.mount("/file.svg", StaticFiles(directory=str(FRONTEND_OUT), html=False), name="file_svg")
    app.mount("/globe.svg", StaticFiles(directory=str(FRONTEND_OUT), html=False), name="globe_svg")
    app.mount("/window.svg", StaticFiles(directory=str(FRONTEND_OUT), html=False), name="window_svg")
    app.mount("/vercel.svg", StaticFiles(directory=str(FRONTEND_OUT), html=False), name="vercel_svg")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/{path:path}")
async def serve_frontend_index(path: str):
    if FRONTEND_OUT.exists():
        index = FRONTEND_OUT / "index.html"
        if index.exists():
            return FileResponse(str(index))
    from fastapi.responses import HTMLResponse
    return HTMLResponse("<h1>404</h1>", status_code=404)


@app.get("/")
async def root():
    if FRONTEND_OUT.exists():
        return FileResponse(str(FRONTEND_OUT / "index.html"))
    from fastapi.responses import HTMLResponse
    return HTMLResponse("<h1>Prelegal API</h1><p>Run the frontend build to serve the UI.</p>")
