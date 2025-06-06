import pprint
from typing import TypeVar
from dataclasses import dataclass
from http import HTTPMethod

import requests

from deltav.spacetraders.api.error import SpaceTradersAPIError
from deltav.spacetraders.api.ratelimit import Ratelimit
from deltav.spacetraders.api.request import SpaceTradersAPIRequest
from deltav.spacetraders.api.response import SpaceTradersAPIResponse

MAX_PAGE_LIMIT = 20


@dataclass
class PagingData:
    page: int = 1
    limit: int = MAX_PAGE_LIMIT


class SpaceTradersAPIClient:
    def __init__(self):
        self.ratelimit: Ratelimit = Ratelimit()

    # QUESTION: How to handle partial success for paged requests
    @staticmethod
    def call(
        req: SpaceTradersAPIRequest,
    ) -> SpaceTradersAPIResponse | SpaceTradersAPIError:
        # TODO: Log the request and response properly

        res = requests.request(
            method=req.endpoint.method,
            headers=req.headers,
            url=req.url,
            data=req.data if req.endpoint.method is not HTTPMethod.GET else {},
        )

        print(
            """
            ========== REQUEST ==========
            """
        )
        print(
            f"""
            --- URL ---------
            {req.endpoint.method} {req.url}
            --- HEADERS -----
            {req.headers}
            --- DATA --------
            {req.data}
            --- END REQ -----
            """
        )

        # print(
        #     """
        #     ========== RESPONSE ==========
        #     """
        # )
        # pprint.pp(
        #     f"""
        #     --- HEADERS -----
        #     {res.headers}
        #     --- DATA --------
        #     {res.json()}
        #     --- END RES -----
        #     """
        # )

        if res.ok:
            return SpaceTradersAPIResponse(req.endpoint, res)
        else:
            return SpaceTradersAPIError(res)
