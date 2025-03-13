from sqlalchemy import BigInteger, Column, DateTime, func

from database.models.base import Base

class UserModel(Base):
    __tablename__ = "users"

    created_at = Column(DateTime, default=func.now())

    discord_user_id = Column(BigInteger, primary_key=True) ## this is the users discord id

