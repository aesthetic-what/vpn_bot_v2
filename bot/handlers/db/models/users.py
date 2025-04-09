from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from handlers.db.db_core import Base
from datetime import datetime

class Users(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str]
    user_id: Mapped[str] = mapped_column(unique=True)
    count_payed: Mapped[int] = mapped_column(default=0)
    ref_id: Mapped[str] = mapped_column(ForeignKey("users.user_id"), nullable=True)
    sub_link: Mapped[str] = mapped_column(nullable=True)
    expire_time: Mapped[int] = mapped_column(nullable=True)
    role: Mapped[str] = mapped_column(default='user')
    invated_users: Mapped[int] = mapped_column(default=0)
    paid_users: Mapped[int] = mapped_column(default=0)