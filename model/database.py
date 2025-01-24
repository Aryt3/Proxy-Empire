from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DB_URL = f'sqlite:///proxy.db'

engine = create_engine(SQLALCHEMY_DB_URL, echo=True, pool_size=100, max_overflow=100)
DBSession = sessionmaker(engine, autoflush=False)