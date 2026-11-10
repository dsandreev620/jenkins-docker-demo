import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, create_engine
from alembic import context

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

from app import db
target_metadata = db.metadata

def get_url():
    """Получает URL и гарантирует использование psycopg2"""
    url = os.getenv("DATABASE_URL")
    if not url:
        url = config.get_main_option("sqlalchemy.url")
    
    # Принудительно меняем драйвер на psycopg2
    if url and url.startswith('postgresql://'):
        url = url.replace('postgresql://', 'postgresql+psycopg2://', 1)
        
    return url

def run_migrations_offline() -> None:
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    url = get_url()
    connectable = create_engine(url, poolclass=pool.NullPool)

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