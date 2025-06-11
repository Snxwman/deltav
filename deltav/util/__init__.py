from __future__ import annotations

from datetime import date, datetime
from typing import Any

from pydantic import BaseModel


def generic__repr__(instance: object) -> str:
    return f'{instance.__class__.__name__}({instance.__dict__})'


