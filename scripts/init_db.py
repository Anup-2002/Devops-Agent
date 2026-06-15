from __future__ import annotations

import asyncio

from autoops_ai.db.base import Base
from autoops_ai.db.session import engine
from autoops_ai.db import models  # noqa: F401


async def init_db() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(init_db())
