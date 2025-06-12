from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass


Session = sessionmaker()
