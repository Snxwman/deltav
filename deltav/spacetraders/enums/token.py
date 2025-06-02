from enum import Enum, auto


class TokenType(Enum):
    """

    ACCOUNT
    AGENT
    NONE
    """

    ACCOUNT = auto()
    AGENT = auto()
    NONE = auto()
