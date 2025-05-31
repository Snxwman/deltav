# pyright: reportPrivateUsage=false

from http import HTTPMethod, HTTPStatus
import json

from deltav.config import CONFIG
from deltav.spacetraders.api import SPACETRADERS_API_URL
from deltav.spacetraders.enums.endpoints import SpaceTradersAPIEndpoint
from deltav.spacetraders.enums.error import SpaceTradersAPIErrorCodes
from deltav.spacetraders.models import SpaceTradersAPIReqShape, SpaceTradersAPIResShape


class SpaceTradersAPIRequest:
    """A builder class for SpaceTraders API Requests"""

    def __init__(self) -> None:
        self._endpoint: SpaceTradersAPIEndpoint = SpaceTradersAPIEndpoint.GAME
        self._method: HTTPMethod = self._endpoint.method
        self._headers: dict[str, str] = {}
        self._params: list[str] = []
        self._data: SpaceTradersAPIResShape = {}

        # Request meta properties
        self._retries: int | None = None
        self._cancel_on_ratelimit: bool = False
        self._cancel_on_http_errors: list[HTTPStatus] = []
        self._cancel_on_spacetrader_errors: list[SpaceTradersAPIErrorCodes] = []

        # The token to use for the request, could be account or agent
        self._token: str | None = None

        # Set default headers
        self._headers['Content-Type'] = 'application/json'


    @property
    def endpoint(self) -> SpaceTradersAPIEndpoint:
        return self._endpoint


    @property
    def data(self) -> str:
        return json.dumps(self._data)


    @property
    def headers(self) -> dict[str, str]:
        return self._headers


    @property
    def parameterized_path(self) -> str:
        mapping = dict(zip(self._endpoint.path.get_identifiers(), self._params))
        path = self._endpoint.path.substitute(mapping)
        return path[1:] if path[0] == '/' else path


    @property
    def url(self) -> str:
        return f'{SPACETRADERS_API_URL}/{self.parameterized_path}'


    def builder(self) -> 'SpaceTradersAPIRequestBuilder':
        return SpaceTradersAPIRequestBuilder(self)


class SpaceTradersAPIRequestBuilder:
    def __init__(self, req: SpaceTradersAPIRequest) -> None:
        self.req: SpaceTradersAPIRequest = req


    def endpoint(self, endpoint: SpaceTradersAPIEndpoint) -> 'SpaceTradersAPIRequestBuilder':
        self.req._endpoint = endpoint
        self.req._method = endpoint.method
        return self


    def data(self, data: SpaceTradersAPIReqShape) -> 'SpaceTradersAPIRequestBuilder':
        self.req._data = data
        return self


    def headers(self, *headers: tuple[str, str]) -> 'SpaceTradersAPIRequestBuilder':
        for header in headers:
            key, value = header[0], header[1]
            self.req._headers[key] = value

        return self


    def path_params(self, *params: str) -> 'SpaceTradersAPIRequestBuilder':
        self.req._params = [str(param) for param in params]
        return self


    # TODO: implement
    def pages(self, start: int, end: int) -> 'SpaceTradersAPIRequestBuilder':
        ...


    # TODO: implement
    def page_limit(self, limit: int) -> 'SpaceTradersAPIRequestBuilder':
        ...


    def retries(self, times: int) -> 'SpaceTradersAPIRequestBuilder':
        self.req._retries = times
        return self


    def with_account_token(self) -> 'SpaceTradersAPIRequestBuilder':
        self.req._token = CONFIG.token if self.req._token is None else self.req._token
        self.req._headers['Authorization'] = f'Bearer {self.req._token}'
        return self


    def with_agent_token(self) -> 'SpaceTradersAPIRequestBuilder':
        self.req._token = CONFIG.token if self.req._token is None else self.req._token
        self.req._headers['Authorization'] = f'Bearer {self.req._token}'
        return self


    def cancel_on_ratelimit(self) -> 'SpaceTradersAPIRequestBuilder':
        self.req._cancel_on_ratelimit = True
        return self


    def cancel_on_http_errors(self, *status: HTTPStatus) -> 'SpaceTradersAPIRequestBuilder':
        ...


    def cancel_on_spacetrader_errors(self, *codes: SpaceTradersAPIErrorCodes) -> 'SpaceTradersAPIRequestBuilder':
        ...


    def build(self) -> SpaceTradersAPIRequest:
        return self.req
