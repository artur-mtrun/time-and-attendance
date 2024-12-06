from logging.config import fileConfig
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy import pool
from alembic import context
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Dodaj ścieżkę do katalogu głównego projektu
current_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.dirname(current_path)
sys.path.append(root_path)

from app.models.base import Base
from app.models import user, employee, terminal, attendance

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = os.getenv("DATABASE_URL")
    print(f"Database URL: {url}")  # Debug print
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    url = os.getenv("DATABASE_URL")
    print(f"Database URL: {url}")  # Debug print
    
    if not url:
        raise ValueError("DATABASE_URL is not set in environment variables")
        
    connectable = create_engine(url)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()