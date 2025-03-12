from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from sqlalchemy.future import select

from database.models.user_model import User
from database.session import get_db
from database.session import engine


async def list_all_users(db: AsyncSession):
    async with db.begin():
        result = await db.execute(select(User))
        users = result.scalars().all()  # Returns a list of User objects
        return users

async def test_db_operations():
    async for db in get_db():  # Get the AsyncSession from get_db
        users = await list_all_users(db)
        for user in users:
            print(f"User id: {user.id} discord id: {user.discord_id}")

async def main():
    await test_db_operations()
    await engine.dispose()  

if __name__ == "__main__":
    asyncio.run(main())

