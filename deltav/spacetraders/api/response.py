from dataclasses import dataclass
from typing import Any, cast

from requests import Response
from requests.structures import CaseInsensitiveDict

from deltav.spacetraders.api.ratelimit import Ratelimit
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
    def __init__(self, endpoint: SpaceTradersAPIEndpoint, res: Response):
        self.__res = res

        http_headers, spacetraders_headers = self.__extract_headers()

        json_data: dict[Any, Any] = {} if res.status_code == 204 else res.json()

        data = endpoint.response_shape.model_validate(json_data, by_alias=True)
        meta = None if 'meta' not in json_data else cast(MetaShape, json_data['meta'])

        self.http: HttpResponse = HttpResponse(
            status_code=res.status_code, 
            headers=http_headers
        )  # fmt: skip
        self.spacetraders: SpaceTradersAPIResData = SpaceTradersAPIResData(
            data=data,
            meta=meta,
            headers=spacetraders_headers,
        )

    def __extract_headers(self) -> tuple[CaseInsensitiveDict[str], CaseInsensitiveDict[str]]:
        http_headers = self.__res.headers.copy()
        spacetraders_headers = self.__res.headers.copy()

        for header in self.__res.headers.keys():
            if header in Ratelimit.X_HEADERS:
                _ = http_headers.pop(header)
            else:
                _ = spacetraders_headers.pop(header)

        return (http_headers, spacetraders_headers)
