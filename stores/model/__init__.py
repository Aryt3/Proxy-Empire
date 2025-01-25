from . import models, database
import asyncio

async def init():
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

asyncio.run(init())