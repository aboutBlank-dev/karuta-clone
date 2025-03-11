from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database.models.base import Base

class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    pokemon_id = Column(Integer, nullable=False)
    pokemon_is_shiny = Column(Boolean, nullable=False, default=False)

# CRUD functions
# async def create_card(db: AsyncSession, name: str):
#     card = Card(name=name)
#     db.add(card)
#     await db.commit()
#     await db.refresh(card)
#     return card

# async def get_card_by_name(db: AsyncSession, name: str):
#     result = await db.execute(select(Card).filter(Card.name == name))
#     return result.scalars().first()
