from sqlalchemy import BigInteger, CheckConstraint, Column, DateTime, Float, ForeignKey, Integer, String, func
from database.models.base import Base

class UserCardModel(Base):
    __tablename__ = "user_cards"

    created_at = Column(DateTime, default=func.now())

    id = Column(BigInteger, primary_key=True)
    pokemon_tcg_card_id = Column(String, nullable=False)

    pattern_number = Column(Integer, CheckConstraint('pattern_number >= 0 AND pattern_number < 500'), nullable=False)  
    float_value = Column(Float, CheckConstraint('float_value >= 0 AND float_value <= 1'), nullable=False) 
    print_number = Column(Integer, nullable=False) 

    # Foreign Keys
    owner_id = Column(BigInteger, ForeignKey("users.discord_user_id"))
    drop_event_id = Column(String, ForeignKey("card_drop_events.id"))
