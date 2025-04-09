from sqlalchemy import select, update
from handlers.db.models.users import Users
from handlers.db.db_core import local_session
from logger import Logger

logger = Logger.getinstance()


async def create_user(username: str, chat_id: str, ref_id: str = None):
    async with local_session() as session:
        user = await session.scalar(select(Users).where(Users.user_id == chat_id))

        if not user:
            session.add(Users(username=username, user_id=chat_id, ref_id=ref_id))
            print(username, chat_id, ref_id)
            if ref_id:
                logger.info(f"Ref ID: {ref_id}")
                referrer = await session.scalar(select(Users).where(Users.user_id == ref_id))

                # print(f"Referrer: {referrer}")
                if referrer:
                    # Увеличиваем количество приглашенных
                    referrer.invated_users += 1

            await session.commit()


async def set_paid(user_id: str):
    from handlers.marzban_client import add_days
    async with local_session() as session:
        user = await session.scalar(select(Users).where(Users.user_id == user_id))
        if user:
            user.count_payed += 1

            if user.ref_id:
                referrer = await session.scalar(select(Users).where(Users.user_id == user.ref_id))
                if referrer:
                    print(f"referrer: {referrer.username}, {referrer.user_id}")
                    if referrer.paid_users < 1:
                        referrer.paid_users += 1
                    await add_days(referrer.user_id, 25)

        await session.commit()


async def update_user(chat_id: str, sub_link: str, expire_time:int, ref_id: str = None):
    async with local_session() as session:
        user = await session.scalar(select(Users).where(Users.user_id == chat_id))
        if user:
            await session.execute(update(Users).
                            where(Users.user_id == chat_id).
                            values(sub_link=sub_link, expire_time=expire_time))
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



async def get_referrer(user_id: str):
    async with local_session() as session:
        result = await session.execute(select(Users.ref_id).where(Users.user_id == user_id))
        referrer_id = result.scalar_one_or_none()
        return referrer_id
            
