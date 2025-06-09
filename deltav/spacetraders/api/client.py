from copy import copy
from time import sleep
from typing import TypeVar

import httpx
from loguru import logger

from deltav.spacetraders.api.error import SpaceTradersAPIError
from deltav.spacetraders.api.ratelimit import Ratelimit
from deltav.spacetraders.api.request import SpaceTradersAPIRequest
from deltav.spacetraders.api.response import SpaceTradersAPIResponse
from deltav.spacetraders.models import SpaceTradersAPIResShape, merge_models


T = TypeVar('T', bound=SpaceTradersAPIResShape)


class SpaceTradersAPIClient:
    """Client that handles sending requests to the SpaceTraders API."""

    http_client: httpx.Client = httpx.Client()
    ratelimit: Ratelimit = Ratelimit()

    def __init__(self) -> None:
        SpaceTradersAPIClient.http_client = httpx.Client()

    @classmethod
    def __call(
        cls, _req: httpx.Request, req: SpaceTradersAPIRequest[T]
    ) -> SpaceTradersAPIResponse[T] | SpaceTradersAPIError:
        # QUESTION: How to handle partial success for paged requests
        # TODO: Log the request and response properly

        logger.info(f'Requesting {_req.url}')
        res = cls.http_client.send(_req)

        if res.status_code < 300:
            logger.success(res.status_code)
            return SpaceTradersAPIResponse[T](req.endpoint, res)
        else:
            logger.error(res.status_code)
            return SpaceTradersAPIError(res)

    # FIX: REALLY BAD, probably need to refactor SpaceTradersAPIResponse
    @classmethod
    def call(cls, req: SpaceTradersAPIRequest[T]) -> SpaceTradersAPIResponse[T] | SpaceTradersAPIError:
        """Call a SpaceTraders API endpoint by passing a request object.

        Args:
            req: The request object used to construct the API call.

        Raises:
            ValidationError: If the actual response does not conform to the
            pydantic model specification.
        """
        requests: list[tuple[int, httpx.Request]] = []
        responses: list[tuple[int, SpaceTradersAPIResponse[T] | SpaceTradersAPIError]] = []

        def httpx_request(req: SpaceTradersAPIRequest[T], page: int | None = None) -> httpx.Request:
            if page is not None:
                req = copy(req)
                req._current_page = page  # pyright: ignore[reportPrivateUsage]

            return httpx.Request(
                method=req.endpoint.method,
                headers=req.headers,
                url=req.url,
                json=req.json_data,
                params=req.params,
            )

        if req.is_paged and req.all_pages:
            res = cls.__call(httpx_request(req, page=1), req)
            responses.append((1, res))
            if isinstance(res, SpaceTradersAPIResponse):
                if res.meta is not None:
                    req.total_items = res.meta.total

                for i in range(req.total_pages - 1):
                    page = i + 2
                    requests.append((page, httpx_request(req, page)))
            else:
                raise RuntimeError('Aborting since initial request failed')
        elif req.is_paged and not req.all_pages:
            for page in range(req.start_page, req.end_page + 1):
                requests.append((page, httpx_request(req, page)))
        else:
            return cls.__call(httpx_request(req), req)

        for page, _req in requests:
            responses.append((page, cls.__call(_req, req)))
            sleep(0.5)

        ret: SpaceTradersAPIResponse[T] | None = None
        for page, res in responses:
            if isinstance(res, SpaceTradersAPIResponse):
                if ret is None:
                    ret = res
                    continue

                ret.data = merge_models(ret.data, res.data)

        if ret is not None:
            return ret
        else:
            return responses[0][1]
