from dataclasses import dataclass
from http import HTTPStatus
from typing import Any, Generic, TypeVar, cast

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


T = TypeVar('T', bound=SpaceTradersAPIResShape)


class SpaceTradersAPIResponse(Generic[T]):
    def __init__(self, endpoint: SpaceTradersAPIEndpoint, res: Response):
        self.__res: Response = res

        shape = endpoint.response_shapes.get(HTTPStatus(res.status_code))
        if shape is None:
            raise ValueError(f'Got unexpected http status code {res.status_code}')
        self.__shape: type[SpaceTradersAPIResShape] = shape

        http_headers, spacetraders_headers = self.__extract_headers()

        json_data: dict[Any, Any] = {} if res.status_code == 204 else res.json()

        data = self.__shape.model_validate(json_data, by_alias=True)
        meta = None if 'meta' not in json_data else cast(MetaShape, json_data['meta'])

        self.__data: T = cast(T, data)

        self.http: HttpResponse = HttpResponse(
            status_code=res.status_code, 
            headers=http_headers
        )  # fmt: skip
        self.spacetraders: SpaceTradersAPIResData = SpaceTradersAPIResData(
            data=data,
            meta=meta,
            headers=spacetraders_headers,
        )

    def unwrap(self) -> T:
        return self.__data

    def __extract_headers(self) -> tuple[CaseInsensitiveDict[str], CaseInsensitiveDict[str]]:
        http_headers = self.__res.headers.copy()
        spacetraders_headers = self.__res.headers.copy()

        for header in self.__res.headers.keys():
            if header in Ratelimit.X_HEADERS:
                _ = http_headers.pop(header)
            else:
                _ = spacetraders_headers.pop(header)

        return (http_headers, spacetraders_headers)
