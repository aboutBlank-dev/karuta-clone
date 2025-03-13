from sqlalchemy.ext.asyncio import AsyncSession

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
