from sqlalchemy import ARRAY, BigInteger, Column, DateTime, ForeignKey, String, func
from database.models.base import Base
from drops.card_drop_event import CardDropEvent

class CardDropEventModel(Base):
    __tablename__ = "card_drop_events"
    
    created_at = Column(DateTime, default=func.now())

    id = Column(String, primary_key=True, unique=True)
    cards_dropped_ids = Column(ARRAY(String), nullable=False)
    started_by_user_id = Column(BigInteger, ForeignKey("users.discord_user_id"), nullable=False)

    @classmethod
    def from_card_drop_event(cls, card_drop_event: CardDropEvent):
        return cls(
            id=card_drop_event.id,
            cards_dropped_ids=[card.id for card in card_drop_event.all_cards],
            started_by_user_id = card_drop_event.owner_discord_id
        )