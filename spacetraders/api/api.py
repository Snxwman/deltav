from dataclasses import dataclass, field
from datetime import datetime
from enum import auto, Enum
from http import HTTPMethod, HTTPStatus
import json
from typing import Optional, TypedDict

import requests

from spacetraders.api.apierror import SpaceTradersAPIError
from spacetraders.api.endpoints import SpaceTradersAPIEndpoint
from spacetraders.config import CONFIG

MAX_PAGE_LIMIT = 20

@dataclass
class PagingData():
    page: int = 1
    limit: int = MAX_PAGE_LIMIT


@dataclass
class SpaceTradersAPIRequest:
    endpoint: SpaceTradersAPIEndpoint
    headers: dict = field(default_factory=dict)
    params: list = field(default_factory=list)
    data: dict = field(default_factory=dict)
    token: Optional[str] = None

    def parameterized_endpoint(self) -> str:
        p1 = self.params[0] if len(self.params) > 0 else None
        p2 = self.params[1] if len(self.params) > 1 else None
        return SpaceTradersAPIEndpoint.with_params(self.endpoint, p1=p1, p2=p2)

    def get_headers(self, with_defaults=True):
        if with_defaults:
            self.headers['Content-Type'] = 'application/json'

            if (self.endpoint is not SpaceTradersAPIEndpoint.REGISTER):
                token = CONFIG.token if self.token is None else self.token
                self.headers['Authorization'] = f'Bearer {token}'

        return self.headers

    def data_as_json(self) -> str:
        return json.dumps(self.data)
        
class SpaceTradersAPIResponse:
    def __init__(self, response: requests.Response):
        self.http: dict = {
            'headers': response.headers,
            'response': response.status_code,
            'data': response.json(),
        }
        self.spacetraders: dict = {
            'headers': response.headers,
            'response': response.status_code,
            'error': '',
            'data': response.json()['data'],
        }

class RateLimitType(Enum):
    IP_ADDRESS = auto()
    ACCOUNT = auto()
    DDOS_PROTECTION = auto()

@dataclass
class RateLimit():
    type: RateLimitType = RateLimitType.IP_ADDRESS 
    reset: datetime = datetime.now()
    burst: int = 30
    per_second: int = 2
    remaining: int = 2

class SpaceTradersAPI:
    base_url = 'https://api.spacetraders.io'
    version = 'v2' 
    base_api_url = f'{base_url}/{version}'

    def __init__(self):
        self.agents: int
        self.ships: int
        self.systems: int
        self.waypoints: int
        self.leaderboard_credits: list[tuple[str, int]]
        self.leaderboard_submitted_charts: list[tuple[str, int]]

        self.next_restart: datetime
        self.restart_freq: str

        self.rate_limits: RateLimit = RateLimit()

    def update_rate_limits(self, rate_limits: dict):
        ...

    @staticmethod
    def game_state():
        endpoint = SpaceTradersAPIEndpoint.GAME
        req = SpaceTradersAPIRequest(endpoint)
        res = SpaceTradersAPI.call(req)


    @staticmethod
    def _endpoint_with_params(e: SpaceTradersAPIEndpoint, p: dict) -> str:
        return ''


    @staticmethod
    def call(req: SpaceTradersAPIRequest) -> (SpaceTradersAPIResponse | SpaceTradersAPIError):
        url = f'{SpaceTradersAPI.base_api_url}{req.parameterized_endpoint()}'

        match req.endpoint.method:
            case HTTPMethod.GET:
                res = requests.get(url, headers=req.headers)
            case HTTPMethod.POST:
                res = requests.post(url, headers=req.get_headers(), data=req.data_as_json())
            case _:
                res = None

        match res:
            case requests.Response():
                print(res.json())
                return SpaceTradersAPIResponse(res)
            case None:
                raise ValueError
            case _:
                raise TypeError

