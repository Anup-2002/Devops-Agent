from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from autoops_ai.main import create_app


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
async def client(app) -> AsyncClient:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
        yield async_client
