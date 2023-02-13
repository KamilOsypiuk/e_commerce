from sqlmodel import create_engine
from sqlalchemy.orm import sessionmaker
import os


def get_url():
    user = os.environ["DB_USER"]
    password = os.environ["DB_PASS"]
    host = os.environ["DB_HOST"]
    database = os.environ["DB_NAME"]
    return f"postgresql://{user}:{password}@{host}/{database}"


engine = create_engine(get_url(), echo=True)

SessionLocal = sessionmaker(
    bind=engine, autocommit=False, autoflush=False, expire_on_commit=False
)


def get_db():
    with SessionLocal() as session:
        yield session
