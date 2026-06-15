from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from autoops_ai.core.config import get_settings
from autoops_ai.db.session import SessionLocal


class HealthChecker:
    async def check_database(self) -> bool:
        try:
            async with SessionLocal() as session:
                await session.execute(text("SELECT 1"))
            return True
        except SQLAlchemyError:
            return False

    async def check_redis(self) -> bool:
        settings = get_settings()
        try:
            from redis.asyncio import Redis

            client = Redis.from_url(settings.redis_url)
            pong = await client.ping()
            await client.aclose()
            return bool(pong)
        except Exception:
            return False


def get_health_checker() -> HealthChecker:
    return HealthChecker()
