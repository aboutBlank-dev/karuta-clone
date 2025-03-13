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
    async with get_session() as session:
        new_user = UserModel(discord_user_id=1)
        session.add(new_user)
        await session.commit()
        return new_user

async def get_user(id):
    async with get_session() as session:
        return await session.get(UserModel, id)

async def create_user_card(user: UserModel):
    random_card: PokemonCardSchema = PokemonTCGCardLoader.random()

    drop_event_id = str(uuid.uuid4())

    async with get_session() as session:
        new_drop_event = CardDropEventModel(id=drop_event_id, cards_dropped_ids=[random_card.id], started_by_id=user.id)
        session.add(new_drop_event)

        new_user_card = UserCardModel(pokemon_tcg_card_id=random_card.id, owner_id=user.id, drop_event_id=drop_event_id)
        session.add(new_user_card)

        # Commit the session
        await session.commit()

        return new_user_card

async def get_all_user_cards(owner_id: int) -> list[UserCardModel]:
    # Assuming get_session() returns an AsyncSession in an async context
    async with get_session() as session:
        # Query to get all cards owned by the user with the given owner_id
        result = await session.execute(select(UserCardModel).filter(UserCardModel.owner_id == owner_id))
        
        # Fetch the results and return them
        cards = result.scalars().all()
        return cards

async def main():
    test_user = await get_user(1)
    new_card = await create_user_card(test_user)
    print(f"Using user with id: {test_user.id}")
    print(f"Card number {new_card.id} dropped. Base36 id: {to_base36(new_card.id)}")


# Set the event loop policy (Windows specific fix to prevent Even loop closed error)
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

if __name__ == "__main__":
    import logging

    # Check the current logging level
    logger = logging.getLogger('sqlalchemy.engine')
    print("Current logging level for sqlalchemy.engine:", logger.level)

    # Set it to WARNING if needed
    logger.setLevel(logging.WARNING)

    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    finally:
        loop.close()  # Ensure loop is closed when everything is done
