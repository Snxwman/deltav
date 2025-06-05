from dataclasses import dataclass
from http import HTTPMethod
from typing import TypeVar

import requests

from deltav.spacetraders.api.error import SpaceTradersAPIError
from deltav.spacetraders.api.ratelimit import Ratelimit
from deltav.spacetraders.api.request import SpaceTradersAPIRequest
from deltav.spacetraders.api.response import SpaceTradersAPIResponse
from deltav.spacetraders.models import SpaceTradersAPIResShape


T = TypeVar("T", bound=SpaceTradersAPIResShape)


class SpaceTradersAPIClient:
    """Client that handles sending requests to the SpaceTraders API."""
    def __init__(self):
        self.ratelimit: Ratelimit = Ratelimit()

    # QUESTION: How to handle partial success for paged requests
    @staticmethod
    def call(
        req: SpaceTradersAPIRequest,
        shape: type[T] | type[list[T]],
    ) -> SpaceTradersAPIResponse[T] | SpaceTradersAPIError:
        """Call a SpaceTraders API endpoint.
        
        Args:
            req: The request object used to construct the API call.
            shape: The expected return type of the call. This is a class
            inheriting from SpaceTradersAPIResShape which itself inherits from
            pydantic.BaseModel.

        Raises:
            ValidationError: If the actual response does not conform to the
            pydantic model specification.
        """
        # TODO: Log the request and response properly

        res = requests.request(
            method=req.endpoint.method,
            headers=req.headers,
            url=req.url,
            data=req.json_data,
        )

        print(req)

        if res.ok:
            return SpaceTradersAPIResponse[T](req.endpoint, res)
        else:
            return SpaceTradersAPIError(res)
