from sqlalchemy import Column, Integer, ForeignKey, String
from database.models.base_model import Base

class UserCardModel(Base):
    __tablename__ = "user_cards"

    id = Column(String, primary_key=True, unique=True)
    collection_index = Column(Integer, autoincrement=True, unique=True)

    pokemon_tcg_card_id = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
