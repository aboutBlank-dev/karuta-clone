from sqlalchemy import Column, DateTime, Integer, ForeignKey, String, func
from database.models.base import Base
from utils.id_utils import to_base36
from sqlalchemy.ext.asyncio import AsyncSession


class UserCardModel(Base):
    __tablename__ = "user_cards"

    created_at = Column(DateTime, default=func.now())

    id = Column(Integer, primary_key=True)
    pokemon_tcg_card_id = Column(String, nullable=False)

    # Foreign Keys
    owner_id = Column(Integer, ForeignKey("users.id"))
    drop_event_id = Column(String, ForeignKey("card_drop_events.id"))
