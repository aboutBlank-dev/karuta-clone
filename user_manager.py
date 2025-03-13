from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.user_card_model import UserCardModel
from database.models.user_model import UserModel
from database.session import get_session

class UserManager:

    @staticmethod
    async def get_or_create(discord_user_id: int) -> UserModel:
        async with get_session() as session:
            # Use session.get for direct retrieval by primary key (discord_user_id)
            db_user = await session.get(UserModel, discord_user_id)

            if db_user:
                # User exists, return the existing user
                return db_user

            # If user does not exist, create a new user
            new_user = UserModel(discord_user_id=discord_user_id)
            session.add(new_user)
            await session.commit()
            
            return new_user

    @staticmethod
    async def get_all_user_cards(discord_user_id: int):
        """
        Returns all cards for the given user.
        """
        async with get_session() as session:
            query = select(UserCardModel).filter(UserCardModel.owner_id == discord_user_id)

            result = await session.execute(query)
            user_cards = result.scalars().all()

            return user_cards 

    @staticmethod
    async def get_user_cards(discord_user_id: int, amount: int, cursor: int = None):
        """
        Returns X amount of cards that the user has, paginated by cursor.
        """
        async with get_session() as session:
            query = select(UserCardModel).filter(UserCardModel.owner_id == discord_user_id)
            
            # If cursor is provided, filter by cards with id greater than the cursor value (for pagination)
            if cursor:
                query = query.filter(UserCardModel.id > cursor)
            
            query = query.limit(amount)

            # Execute the query
            result = await session.execute(query)

            # Fetch the results as a list of UserCardModel instances
            user_cards = result.scalars().all()

            # If there are results, return the cards and the ID of the last card as the new cursor
            if user_cards:
                return user_cards, user_cards[-1].id  # Return the cards along with the last card's ID for pagination

            return [], None  # No cards found, return empty list and None for the cursor
    
