from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import engine, Base
from app.routers import vehicles, packages, enquiries
from app.seed import seed as run_seed

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.
    Runs on startup:  create tables + seed default data.
    Runs on shutdown: (add cleanup here if needed).
    """
    Base.metadata.create_all(bind=engine)
    run_seed()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=(
            "REST API for Syelon Wedding — manages the vehicle fleet, "
            "pricing packages, and customer enquiries."
        ),
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        lifespan=lifespan,
    )

    # ── CORS ─────────────────────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Routers ──────────────────────────────────────────────────────────────
    API_PREFIX = "/api/v1"
    app.include_router(vehicles.router,  prefix=API_PREFIX)
    app.include_router(packages.router,  prefix=API_PREFIX)
    app.include_router(enquiries.router, prefix=API_PREFIX)

    # ── Health check ─────────────────────────────────────────────────────────
    @app.get("/api/health", tags=["Health"])
    def health():
        return {"status": "ok", "version": settings.app_version}

    return app


app = create_app()
