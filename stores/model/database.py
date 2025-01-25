import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger('sqlalchemy.engine')
logger.setLevel(logging.ERROR)

SQLALCHEMY_DB_URL = f'sqlite+aiosqlite:///proxy.db'

# Create the async engine with the database URL
engine = create_async_engine(SQLALCHEMY_DB_URL, echo=False)

# Create a session maker using the async session
DBAsyncSession = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)