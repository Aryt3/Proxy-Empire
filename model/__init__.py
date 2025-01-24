from . import models, database

async def __init__():
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
