from sqlalchemy import Column, Integer, String, Boolean, DateTime
from db.db_core import Base

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    user_id = Column(Integer, unique=True)
    role = Column(String)
    bought = Column(Boolean)
    vpn_key = Column(String, default='1')
    label = Column(String, default='1')
    time_sub = Column(DateTime)
    key_id = Column(String, default='1')