from __future__ import annotations

from fastapi import APIRouter, Depends

from autoops_ai.api.dependencies import HealthChecker, get_health_checker
from autoops_ai.schemas.health import HealthResponse, ReadinessResponse

router = APIRouter(tags=["health"])


@router.get("/health/live", response_model=HealthResponse)
async def live() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get("/health/ready", response_model=ReadinessResponse)
async def ready(checker: HealthChecker = Depends(get_health_checker)) -> ReadinessResponse:
    db_ok = await checker.check_database()
    redis_ok = await checker.check_redis()
    overall = "ok" if db_ok and redis_ok else "degraded"
    return ReadinessResponse(
        status=overall,
        database="ok" if db_ok else "unavailable",
        redis="ok" if redis_ok else "unavailable",
    )
