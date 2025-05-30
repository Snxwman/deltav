from dataclasses import dataclass, field
from datetime import datetime
from enum import auto, Enum
from http import HTTPMethod
import json
import pprint
from typing import Any

import requests

from spacetraders.api.apierror import SpaceTradersAPIError
from spacetraders.api.data import EndpointData
from spacetraders.api.endpoints import SpaceTradersAPIEndpoint
from spacetraders.config import CONFIG

MAX_PAGE_LIMIT = 20

@dataclass
class PagingData():
    page: int = 1
    limit: int = MAX_PAGE_LIMIT


class SpaceTradersAPIRequest:
    """A builder class for SpaceTraders API Requests"""

    def __init__(self, include_default_headers: bool = True) -> None:
        self._endpoint: SpaceTradersAPIEndpoint = SpaceTradersAPIEndpoint.GAME
        self._method: HTTPMethod = self._endpoint.method
        self._headers: dict[str, str] = {}
        self._params: list[str] = []
        self._data: EndpointData = {}
        self._token: str | None = None
        self.include_default_headers = include_default_headers


    def parameterized_endpoint(self) -> str:
        p1 = self._params[0] if len(self._params) > 0 else None
        p2 = self._params[1] if len(self._params) > 1 else None

        # TODO: This check should really be done before calling this method
        if self._endpoint is None:
            raise ValueError('Must set an endpoint')

        return SpaceTradersAPIEndpoint.with_params(self._endpoint, p1=p1, p2=p2)


    def set_headers(self) -> None:
        if self.include_default_headers:
            self._token = CONFIG.token if self._token is None else self._token
            self._headers['Authorization'] = f'Bearer {self._token}'
            self._headers['Content-Type'] = 'application/json'


    def data_as_json(self) -> str:
        return json.dumps(self._data)


    def endpoint(self, endpoint: SpaceTradersAPIEndpoint) -> 'SpaceTradersAPIRequest':
        self._endpoint = endpoint
        self._method = self._endpoint.method
        return self


    def headers(self, headers: dict[str, str]) -> 'SpaceTradersAPIRequest':
        self._headers = headers
        return self


    def params(self, params: list[str]) -> 'SpaceTradersAPIRequest':
        self._params = params
        return self


    def data(self, data: EndpointData) -> 'SpaceTradersAPIRequest':
        self._data = data
        return self


    # TODO: implement
    def page_number(self, page: int) -> 'SpaceTradersAPIRequest':
        ...


    # TODO: implement
    def page_limit(self, limit: int) -> 'SpaceTradersAPIRequest':
        ...


    def call(self) -> 'SpaceTradersAPIResponse | SpaceTradersAPIError':
        self.set_headers()
        return SpaceTradersAPI.call(self)
        

class SpaceTradersAPIResponse:
    def __init__(self, response: requests.Response):
        # TODO: These should be typed dicts
        self.http: dict[str, Any] = {  # pyright: ignore[reportExplicitAny]
            'headers': response.headers,
            'response': response.status_code,
            'data': response.json(),
        }
        print(f'response: {response.status_code} - {response.reason}')
        if response.status_code != 200 and response.status_code != 201:
            self.spacetraders: dict[str, Any] = {  # pyright: ignore[reportExplicitAny]
                'headers': response.headers,
                'response': response.status_code,
                'error': response.json().get('error', None),
                'data': None,
                # 'meta': response.json()['meta']
            }
            print(response.json())
            # print('403 error (No access)')
        
        else:
            self.spacetraders: dict[str, Any] = {  # pyright: ignore[reportExplicitAny]
                'headers': response.headers,
                'response': response.status_code,
                'error': '',
                'data': response.json()['data'],
                # 'meta': response.json()['meta']
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
    base_url: str = 'https://api.spacetraders.io'
    version: str = 'v2' 
    base_api_url: str = f'{base_url}/{version}'

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


    def update_rate_limits(self, rate_limits: dict[str, str]):
        ...


    @staticmethod
    def game_state() -> SpaceTradersAPIResponse | SpaceTradersAPIError:
        return SpaceTradersAPIRequest() \
            .endpoint(SpaceTradersAPIEndpoint.GAME) \
            .call()


    @staticmethod
    def _endpoint_with_params(e: SpaceTradersAPIEndpoint, p: dict[str, str]) -> str:
        return ''


    @staticmethod
    def call(req: SpaceTradersAPIRequest) -> SpaceTradersAPIResponse | SpaceTradersAPIError:
        url = f'{SpaceTradersAPI.base_api_url}{req.parameterized_endpoint()}'
        print(f'Calling {url} with method {req._method} and headers ') # {req._headers} ')

        match req._method:  # pyright: ignore[reportPrivateUsage]
            case HTTPMethod.GET:
                res = requests.get(url, headers=req._headers)  # pyright: ignore[reportPrivateUsage]
            case HTTPMethod.POST:
                res = requests.post(url, headers=req._headers, data=req.data_as_json())  # pyright: ignore[reportPrivateUsage]
            case _:
                res = None

        match res:
            case requests.Response():
                print()
                # pprint.pp(res.json())  # pyright: ignore[reportAny]
                print()
                return SpaceTradersAPIResponse(res)
            case None:
                raise ValueError
