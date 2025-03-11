import sys
import os
import glob
import importlib
from dotenv import load_dotenv
from alembic import context
from sqlalchemy import create_engine, pool
from sqlalchemy.ext.declarative import declarative_base
from logging.config import fileConfig

# Load environment variables from .env file
load_dotenv()

# Get the database URL from environment variables
DATABASE_URL_ALEMBIC = os.getenv("DATABASE_URL_ALEMBIC")

# Add the models folder to the sys.path to allow dynamic imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../database/models')))

# Dynamically discover all model files in the 'database/models' folder
model_files = glob.glob(os.path.join(os.path.dirname(__file__), '../database/models', '*.py'))

# Dynamically import each model file found
for model_file in model_files:
    # Extract the module name (remove the file extension)
    module_name = os.path.basename(model_file)[:-3]
    if module_name != '__init__':  # Skip __init__.py
        importlib.import_module(f'database.models.{module_name}')

# Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Use the Base's metadata for target_metadata
from database.models.base import Base
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL_ALEMBIC,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = create_engine(DATABASE_URL_ALEMBIC, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

# Main function to manage the execution flow
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
