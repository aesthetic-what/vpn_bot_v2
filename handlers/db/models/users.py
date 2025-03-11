from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from handlers.db.db_core import Base
from datetime import datetime

class Users(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str]
    user_id: Mapped[str] = mapped_column(unique=True)
    user_uuid: Mapped[str]
    role: Mapped[str] = mapped_column(default='user')
    vpn_key: Mapped[str] = mapped_column(default='1')
    time_sub = mapped_column(DateTime)