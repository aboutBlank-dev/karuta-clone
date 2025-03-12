from sqlalchemy import Column, Integer

from database.models.base_model import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    discord_user_id = Column(Integer, nullable=False, unique=True)


# CRUD functions
# async def create_user(db: AsyncSession, name: str):
#     user = User(name=name)
#     db.add(user)
#     await db.commit()
#     await db.refresh(user)
#     return user

# async def get_user_by_name(db: AsyncSession, name: str):
#     result = await db.execute(select(User).filter(User.name == name))
#     return result.scalars().first()

