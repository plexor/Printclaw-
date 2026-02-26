from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from printclaw.core.paths import DB_PATH


class Base(DeclarativeBase):
    pass


engine = create_engine(f"sqlite:///{DB_PATH}", future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def init_db() -> None:
    from printclaw.db import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
