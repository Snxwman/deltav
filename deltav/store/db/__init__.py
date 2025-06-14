from __future__ import annotations

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass


engine: Engine = create_engine('sqlite:///deltav.db', echo=True)
Session = sessionmaker(engine)
