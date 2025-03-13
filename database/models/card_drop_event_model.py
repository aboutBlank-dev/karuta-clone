from sqlalchemy import ARRAY, Column, DateTime, String, func
from database.models.base import Base

class CardDropEventModel(Base):
    __tablename__ = "card_drop_events"
    
    created_at = Column(DateTime, default=func.now())

    id = Column(String, primary_key=True, unique=True)
    cards_dropped_ids = Column(ARRAY(String))