from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

SQLALCHEMY_DB_URL = f'sqlite+aiosqlite:///proxy.db'

engine = create_async_engine(SQLALCHEMY_DB_URL, echo=True)
DBAsyncSession = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)