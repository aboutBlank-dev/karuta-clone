from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from database.models.base import Base

class UserCard(Base):
    __tablename__ = "user_cards"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    card_id = Column(Integer, ForeignKey("cards.id"), primary_key=True)

# CRUD function to assign a card to a user
# async def assign_card_to_user(db: AsyncSession, user_id: int, card_id: int):
#     user_card = UserCard(user_id=user_id, card_id=card_id)
#     db.add(user_card)
#     await db.commit()
#     return user_card
