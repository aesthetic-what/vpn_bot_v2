from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from handlers.db.db_core import Base
from datetime import datetime

class Users(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str]
    user_id: Mapped[str] = mapped_column(unique=True)
    sub_link: Mapped[str]
    expire_time: Mapped[int]
    role: Mapped[str] = mapped_column(default='user')