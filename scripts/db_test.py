import sys
import os
import asyncio
import uuid

from sqlalchemy import select

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

from database.models.card_drop_event_model import CardDropEventModel
from database.models.user_card_model import UserCardModel
from utils.id_utils import to_base36


from database.models.user_model import UserModel
from database.session import get_session
from schemas.pokemon_card_schema import PokemonCardSchema, PokemonTCGCardLoader

async def create_user():
    async for session in get_session():
        new_user = UserModel(discord_user_id=1)
        session.add(new_user)
        await session.commit()
        return new_user

async def create_user_card():
    random_card: PokemonCardSchema = PokemonTCGCardLoader.random()

    drop_event_id = str(uuid.uuid4())

    async for session in get_session():
        new_drop_event = CardDropEventModel(id=drop_event_id, cards_dropped_ids=["1", "2", "3"])
        session.add(new_drop_event)

        new_user_card = UserCardModel(pokemon_tcg_card_id=random_card.id, owner_id=1, drop_event_id=drop_event_id)
        session.add(new_user_card)

        # Commit the session
        await session.commit()

        return new_user_card

async def get_all_user_cards(owner_id: int) -> list[UserCardModel]:
    # Assuming get_session() returns an AsyncSession in an async context
    async for session in get_session():
        # Query to get all cards owned by the user with the given owner_id
        result = await session.execute(select(UserCardModel).filter(UserCardModel.owner_id == owner_id))
        
        # Fetch the results and return them
        cards = result.scalars().all()
        return cards

async def main():
    # Assuming you have an async session
    all_user_cards = await get_all_user_cards(1)
    print(f"User with id: 1 has {len(all_user_cards)} cards.")
    for card in all_user_cards:
        print(f"Card {to_base36(card.id)}: {card.pokemon_tcg_card_id}")


if __name__ == "__main__":
    asyncio.run(main())
