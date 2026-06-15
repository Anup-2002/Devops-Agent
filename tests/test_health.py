from __future__ import annotations

import pytest

from autoops_ai.api.dependencies import get_health_checker
class _HealthyChecker:
    async def check_database(self) -> bool:
        return True

    async def check_redis(self) -> bool:
        return True


@pytest.mark.unit
async def test_liveness(client):
    response = await client.get("/api/v1/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.unit
async def test_readiness_healthy(client, app):
    app.dependency_overrides[get_health_checker] = _HealthyChecker

    response = await client.get("/api/v1/health/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "ok", "redis": "ok"}
