from dataclasses import dataclass
from typing import Any, cast

from requests import Response
from requests.structures import CaseInsensitiveDict

from deltav.spacetraders.enums.endpoints import SpaceTradersAPIEndpoint
from deltav.spacetraders.models import SpaceTradersAPIResShape
from deltav.spacetraders.models.meta import MetaShape


@dataclass
class HttpResponse:
    status_code: int
    headers: CaseInsensitiveDict[str]


@dataclass
class SpaceTradersAPIResData:
    data: SpaceTradersAPIResShape
    meta: MetaShape | None
    headers: CaseInsensitiveDict[str]


class SpaceTradersAPIResponse:
    x_headers: list[str] = [
        'X-Ratelimit-Limit-Burst',
        'X-Ratelimit-Limit-Per-Second',
        'X-Ratelimit-Remaining',
        'X-Ratelimit-Reset',
        'X-Ratelimit-Type',
    ]

    def __init__(self, endpoint: SpaceTradersAPIEndpoint, res: Response):
        http_headers = res.headers.copy()
        spacetraders_headers = res.headers.copy()

        for header in res.headers.keys():
            if header in SpaceTradersAPIResponse.x_headers:
                _ = http_headers.pop(header)
            else:
                _ = spacetraders_headers.pop(header)

        if res.status_code == 204:
            json_data: dict[Any, Any] = {}
        else:
            json_data: dict[Any, Any] = res.json()

        data: SpaceTradersAPIResShape = cast(  # pyright: ignore[reportUnknownVariableType]
            endpoint.value.response_shape,  # pyright: ignore[reportInvalidTypeForm]
            json_data if 'data' not in json_data else json_data['data']
        )
        meta = None if 'meta' not in json_data else cast(MetaShape, json_data['meta'])

        self.http: HttpResponse = HttpResponse(
            status_code = res.status_code, 
            headers = http_headers
        )
        self.spacetraders: SpaceTradersAPIResData = SpaceTradersAPIResData(
            data = data,
            meta = meta,
            headers = spacetraders_headers,
        )

