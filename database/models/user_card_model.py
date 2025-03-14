from sqlalchemy import BigInteger, CheckConstraint, Column, DateTime, Float, ForeignKey, Integer, String, func
from database.models.base import Base
from drops.card_drop_event import CardDropEvent
from schemas.pokemon_card_schema import PokemonCardSchema


class UserCardModel(Base):
    __tablename__ = "user_cards"

    created_at = Column(DateTime, default=func.now())

    id = Column(BigInteger, primary_key=True)
    pokemon_tcg_card_id = Column(String, nullable=False)

    # Foreign Keys
    owner_id = Column(BigInteger, ForeignKey("users.discord_user_id"))
    drop_event_id = Column(String, ForeignKey("card_drop_events.id"))

    @classmethod
    def new_user_card_claim_event(cls, discord_user_id: int, pokemon_tcg_card: PokemonCardSchema, card_drop_event: CardDropEvent):
        return cls(
            pokemon_tcg_card_id=pokemon_tcg_card.id,
            owner_id=discord_user_id,
            drop_event_id=card_drop_event.id
        ) 