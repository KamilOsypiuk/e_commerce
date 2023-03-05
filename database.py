from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine

from settings.db_settings import settings

engine = create_engine(settings.get_postgres_url, echo=True)

SessionLocal = sessionmaker(
    bind=engine, autocommit=False, autoflush=False, expire_on_commit=False
)


def get_db():
    with SessionLocal() as session:
        yield session
