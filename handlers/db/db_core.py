from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from decouple import config

username = config("DB_USERNAME")
password = config("DB_PASS")
port = config("DB_PORT")
db_name = config("DB_NAME")

engine_str = f'postgresql+asyncpg://{username}:{password}@{port}/{db_name}'

engine = create_async_engine(engine_str)
local_session = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase): pass

async def get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.close()