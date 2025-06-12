from __future__ import annotations

from typing import final

from deltav.store.db import Base


@final
class ContractRecord(Base):
    __tablename__: str = 'contracts'
