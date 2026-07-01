import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.api.v1.auth import router as auth_router
from app.api.v1.patients import router as patients_router
from app.api.v1.admin import router as admin_router
from app.api.v1.appointments import router as appointments_router
from app.core.config import settings
from app.core.init_db import init_db
from app.core.metrics import setup_metrics


def _resolve_frontend_dir() -> Path | None:
    candidates = []
    if settings.FRONTEND_DIR:
        candidates.append(Path(settings.FRONTEND_DIR))
    app_root = Path(__file__).resolve().parents[2]
    candidates.extend([
        app_root.parent / "frontend" / "build",
        app_root / "frontend" / "build",
        Path(os.environ.get("DMED_APP_ROOT", "")) / "frontend" / "build",
    ])
    for path in candidates:
        if path and path.exists() and (path / "index.html").exists():
            return path
    return None


FRONTEND_DIR = _resolve_frontend_dir()


@asynccontextmanager
async def lifespan(app: FastAPI):
    import time
    last_error = None
    for attempt in range(15):
        try:
            init_db()
            last_error = None
            break
        except Exception as exc:
            last_error = exc
            time.sleep(2)
    if last_error:
        raise last_error
    yield


app = FastAPI(title="DMed API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(patients_router, prefix="/api/v1/patients", tags=["patients"])
app.include_router(admin_router, prefix="/api/v1/admin", tags=["admin"])
app.include_router(appointments_router, prefix="/api/v1/appointments", tags=["appointments"])

metrics_handler = setup_metrics()
app.get("/metrics")(metrics_handler)


@app.get("/api/health")
async def health():
    return {"status": "ok", "frontend": FRONTEND_DIR is not None}


if FRONTEND_DIR:
    assets_dir = FRONTEND_DIR / "static"
    if assets_dir.exists():
        app.mount("/static", StaticFiles(directory=str(assets_dir)), name="static")

    @app.get("/")
    async def serve_frontend():
        return FileResponse(FRONTEND_DIR / "index.html")
else:

    @app.get("/")
    async def root():
        return {
            "message": "DMed API is running",
            "version": "1.0.0",
            "docs": "/docs",
        }


if FRONTEND_DIR:
    from fastapi import Request
    from fastapi.responses import JSONResponse

    @app.exception_handler(404)
    async def spa_not_found(request: Request, _exc):
        path = request.url.path
        if path.startswith("/api") or path in {"/docs", "/redoc", "/openapi.json", "/metrics"}:
            return JSONResponse({"detail": "Not Found"}, status_code=404)
        file_path = FRONTEND_DIR / path.lstrip("/")
        if file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(FRONTEND_DIR / "index.html")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
