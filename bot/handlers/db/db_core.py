from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()

username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASS")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

engine_str = f'postgresql+asyncpg://{username}:{password}@{host}:{port}/{db_name}'
# engine_str = 'postgresql+asyncpg://postgres:pass@localhost:5432/testDB'
# engine_str = 'postgresql+psycopg2://postgres:pass@localhost:5432/testDB'

engine = create_async_engine(engine_str)
local_session = async_sessionmaker(bind=engine)

class Base(AsyncAttrs, DeclarativeBase): pass

async def get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.close()

async def init_db():
    # print(username, password, host, port, db_name)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)