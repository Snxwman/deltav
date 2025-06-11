from __future__ import annotations

from http import HTTPStatus
from typing import Any, Generic, TypeVar, cast

from httpx import Headers, Response

from deltav.spacetraders.api.ratelimit import Ratelimit
from deltav.spacetraders.enums.endpoints import SpaceTradersAPIEndpoint
from deltav.spacetraders.models import SpaceTradersAPIResShape
from deltav.spacetraders.models.meta import MetaShape

T = TypeVar('T', bound=SpaceTradersAPIResShape)


class SpaceTradersAPIResponse(Generic[T]):
    def __init__(self, endpoint: SpaceTradersAPIEndpoint, res: Response):
        self.__endpoint: SpaceTradersAPIEndpoint = endpoint
        self.__headers: Headers = res.headers.copy()
        self.__shape: type[SpaceTradersAPIResShape]
        self.__meta: MetaShape | None
        self.data: T

        self.__filter_headers()

        shape = endpoint.response_shapes.get(HTTPStatus(res.status_code))
        if shape is None:
            msg = f'Got unexpected http status code {res.status_code}'
            raise ValueError(msg)
        self.__shape = shape

        json_data: dict[str, Any] = {} if res.status_code == 204 else res.json()
        if 'meta' in json_data:
            self.__meta = MetaShape.model_validate(json_data['meta'])
        else:
            self.__meta = None

        if 'data' in json_data and isinstance(json_data['data'], dict):
            model = shape.model_validate(json_data['data'], by_alias=True)
        else:
            model = shape.model_validate(json_data, by_alias=True)

        self.data = cast(T, model)

    def unwrap(self) -> T:
        return self.data

    @property
    def meta(self) -> MetaShape | None:
        return self.__meta

    def __filter_headers(self) -> None:
        for header in self.__headers.keys():
            if header not in Ratelimit.X_HEADERS:
                _ = self.__headers.pop(header)
