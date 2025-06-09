from datetime import date, datetime, timedelta
from hashlib import sha256, shake_128
from typing import Any, final, override

import jwt

from deltav.spacetraders.enums.token import TokenType 


class Token:
    def __init__(self, token: str) -> None:
        self._alg: str = 'RS256' 
        self._typ: str = 'JWT'
        self._encoded: str = token
        self._decoded: dict[str, Any] = jwt.decode(
            token, algorithms=self._alg, options={'verify_signature': False}
        )  # fmt: skip
        self._identifier: str = self.decoded['identifier']
        self._version: str = self.decoded['version']
        self._iat: int = self.decoded['iat']
        self._sub: str = self.decoded['sub']

    @property
    def encoded(self) -> str:
        return self._encoded

    @property
    def decoded(self) -> dict[str, Any]:
        return self._decoded

    @property
    def issued_at(self) -> datetime:
        return datetime.fromtimestamp(self._iat)

    @property
    def type(self) -> TokenType:
        match self._sub:
            case 'account-token':
                return TokenType.ACCOUNT
            case 'agent-token':
                return TokenType.AGENT
            case _:
                raise ValueError(f'Unknown token type \'{self._sub}\'')

    @property
    def hash(self) -> str:
        return sha256(self.encoded.encode('utf-8')).hexdigest()

    @override
    def __str__(self) -> str:
        return self.encoded


@final
class AccountToken(Token):
    def __init__(self, token: str) -> None:
        super().__init__(token)

    @property
    def account_id(self) -> str:
        return self._identifier


@final
class AgentToken(Token):
    def __init__(self, token: str) -> None:
        super().__init__(token)
        self._reset_date: str = self.decoded['reset_date']

    @property
    def agent_symbol(self) -> str:
        return self._identifier

    @property
    def expiration(self) -> date:
        return date.fromisoformat(self._reset_date) + timedelta(days=7)  # TODO: Make this dynamic somehow

    @property
    def is_expired(self) -> bool:
        return date.today() >= self.expiration
