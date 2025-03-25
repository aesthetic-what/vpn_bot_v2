from sqlalchemy import select, update, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession
from handlers.db.models.users import Users
from handlers.db.db_core import local_session
from logger import Logger
from datetime import datetime

logger = Logger.getinstance()

async def create_user(username: str, chat_id: str, sub_link: str, expire_time:int):
    async with local_session() as session:
        user = await session.scalar(select(Users).where(Users.user_id == chat_id))

        if not user:
            session.add(Users(username=username,
                              user_id=chat_id,
                              sub_link=sub_link,
                              expire_time=expire_time))
            await session.commit()


async def check_user(chat_id: str):
    async with local_session() as session:
        user = await session.scalar(select(Users).where(Users.user_id == chat_id))
        if user is None:
            return False
        else:
            return True


async def get_user_info(chat_id: str):
    async with local_session() as session:
        try:
            user = await session.scalar(select(Users).where(Users.user_id == chat_id))
            print(user)
            return user
        
        except Exception:
            logger.info('Пользователь не найден')

async def get_user_link(chat_id: str):
    async with local_session() as session:
        try:
            user = await session.scalar(select(Users.sub_link).where(Users.user_id == chat_id))
            print(user)
            return user
        
        except Exception:
            logger.info('Пользователь не найден')

async def delete_user(chat_id: str | int):
    ...

async def update_sub(chat_id: str | int, datetime_sub: datetime):
    ...



