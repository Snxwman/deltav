from __future__ import annotations

from enum import Enum


class TokenType(Enum):
    """

    ACCOUNT
    AGENT
    NONE
    """

    ACCOUNT = 'ACCOUNT'
    AGENT = 'AGENT'
    NONE = 'NONE'
