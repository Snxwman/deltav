from dataclasses import dataclass
from http import HTTPMethod, HTTPStatus
from typing import Optional, TypedDict

import requests

from spacetraders.api.apierror import SpaceTradersAPIError
from spacetraders.api.endpoints import SpaceTradersAPIEndpoint

@dataclass
class SpaceTradersAPIRequest:
    endpoint: SpaceTradersAPIEndpoint
    params: list = []
    data: dict = {}

    def parameterized_endpoint(self) -> str:
        p1 = self.params[0] if len(self.params) > 0 else None
        p2 = self.params[1] if len(self.params) > 1 else None
        return SpaceTradersAPIEndpoint.with_params(self.endpoint, p1=p1, p2=p2)

class SpaceTradersAPIResponse:
    def __init__(self, response: requests.Response):
        self.http: dict = {
            'headers': '',
            'response': '',
            'data': '',
        }
        self.spacetraders: dict = {
            'headers': '',
            'response': '',
            'error': '',
            'data': '',
        }

class SpaceTradersAPI:
    base_url = 'https://spacetraders.io'
    version = 'v2' 
    base_api_url = f'{base_url}/{version}'

    def __init__(self):
        pass


    @staticmethod
    def _endpoint_with_params(e: SpaceTradersAPIEndpoint, p: dict) -> str:
        return ''


    @staticmethod
    def call(req: SpaceTradersAPIRequest) -> (SpaceTradersAPIResponse | SpaceTradersAPIError):
        url = f'{SpaceTradersAPI.base_api_url}/{req.parameterized_endpoint}'

        match req.endpoint.method:
            case HTTPMethod.GET:
                res = requests.get(url)
            case HTTPMethod.POST:
                res = requests.post(url)
            case _:
                res = None

        match res:
            case requests.Response():
                return SpaceTradersAPIResponse(res)
            case None:
                raise ValueError
            case _:
                raise TypeError

