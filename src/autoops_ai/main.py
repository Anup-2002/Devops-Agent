from __future__ import annotations

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from autoops_ai.api.routes.health import router as health_router
from autoops_ai.core.config import get_settings
from autoops_ai.core.exceptions import register_exception_handlers
from autoops_ai.core.logging import configure_logging
from autoops_ai.core.middleware import CorrelationIdMiddleware


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level)

    app = FastAPI(title=settings.app_name, debug=settings.app_debug)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(CorrelationIdMiddleware)

    register_exception_handlers(app)

    api_router = APIRouter(prefix=settings.api_v1_prefix)
    api_router.include_router(health_router)
    app.include_router(api_router)

    return app


app = create_app()
