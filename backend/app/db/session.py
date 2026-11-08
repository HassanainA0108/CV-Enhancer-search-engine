from functools import lru_cache
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import get_settings
from app.db.models import Base


@lru_cache
def get_engine():
    url = get_settings().database_url
    if url.startswith('sqlite:///') and not url.startswith('sqlite:///:memory:'):
        Path(url[len('sqlite:///'):]).parent.mkdir(parents=True, exist_ok=True)
    return create_engine(url, connect_args={"check_same_thread": False} if url.startswith("sqlite") else {}, pool_pre_ping=True)


def init_db():
    Base.metadata.create_all(get_engine())


def session_scope():
    return sessionmaker(bind=get_engine(), expire_on_commit=False)()
