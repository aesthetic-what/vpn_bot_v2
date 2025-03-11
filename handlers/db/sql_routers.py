from sqlalchemy import select, update, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession
from handlers.db.models.users import Users
from handlers.db.db_core import local_session
from datetime import datetime

async def create_user(username: str, chat_id: str | int, 
                      user_uuid: str, 
                      datetime_add: datetime,
                      vpn_key: str):
    async with local_session() as session:
        user = await session.scalar(select(Users).where(Users.user_id == chat_id))

        if not user:
            session.add(Users(username=username,
                              user_id=chat_id,
                              user_uuid=user_uuid,
                              vpn_key=vpn_key,
                              time_sub=datetime_add))
            await session.commit()

async def delete_user(chat_id: str | int):
    ...

async def update_sub(chat_id: str | int, datetime_sub: datetime):
    ...



