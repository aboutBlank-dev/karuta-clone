from sqlalchemy import Column, DateTime, Integer, func

from database.models.base import Base

class UserModel(Base):
    __tablename__ = "users"

    created_at = Column(DateTime, default=func.now())

    id = Column(Integer, primary_key=True, index=True)
    discord_user_id = Column(Integer, nullable=False, unique=True)

