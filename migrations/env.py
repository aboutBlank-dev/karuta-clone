from database.models.base_model import Base
from database.session import engine
from database import user, card, user_card  # Import all models

def run_migrations_online():
    with engine.begin() as connection:
        Base.metadata.create_all(bind=connection)
