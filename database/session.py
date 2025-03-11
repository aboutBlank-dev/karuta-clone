import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
database_url = os.getenv("DATABASE_URL")

# Set up logging to only show errors
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.ERROR)

# Create async database engine with echo disabled
engine = create_async_engine(database_url, echo=False)

# Create session factory
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with SessionLocal() as session:
        yield session
