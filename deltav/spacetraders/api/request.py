# pyright: reportPrivateUsage=false

from http import HTTPStatus
from typing import override

from deltav.config import CONFIG
from deltav.spacetraders.api import DEFAULT_PAGE_LIMIT, MAX_PAGE_LIMIT, SPACETRADERS_API_URL
from deltav.spacetraders.enums.endpoints import SpaceTradersAPIEndpoint
from deltav.spacetraders.enums.error import SpaceTradersAPIErrorCodes
from deltav.spacetraders.enums.token import TokenType
from deltav.spacetraders.errors.request import InvalidRequestError
from deltav.spacetraders.models import NoDataReqShape, SpaceTradersAPIReqShape, UnknownReqShape
from deltav.util import generic__repr__


class SpaceTradersAPIRequest:
    """A builder class for SpaceTraders API Requests"""

    def __init__(self) -> None:
        self._endpoint: SpaceTradersAPIEndpoint = SpaceTradersAPIEndpoint.GET_SERVER_STATUS
        self._headers: dict[str, str] = {}
        self._params: list[str] = []
        self._data: SpaceTradersAPIReqShape = UnknownReqShape()

        # Request meta properties
        self._is_paged: bool = False
        self._all_pages: bool = False
        self._start_page: int = 0
        self._end_page: int = 0
        self._page_limit: int = DEFAULT_PAGE_LIMIT

        self._should_retry: bool = False
        self._retries: int | None = None
        self._cancel_on_ratelimit: bool = False
        self._cancel_on_http_errors: list[HTTPStatus] = []
        self._cancel_on_spacetrader_errors: list[SpaceTradersAPIErrorCodes] = []
        self._timeout: int = 60

        # The token to use for the request, could be account or agent
        self._token: str | None = None

    @property
    def endpoint(self) -> SpaceTradersAPIEndpoint:
        return self._endpoint

    @property
    def json_data(self) -> str:
        if self.endpoint.request_shape is NoDataReqShape:
            return '{}'
        else:
            return self._data.model_dump_json(by_alias=True)

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

    @override
    def __repr__(self) -> str:
        return generic__repr__(self)

    @override
    def __str__(self) -> str:
        def indent(string: str, level: int, start_even: bool = False) -> str:
            level = level - 1 if start_even else level

            _string = ''.join(
                f'\n{'\t' * level}{line.replace("\r", "")}'
                for line in str(string).splitlines()
            )  # fmt: skip

            return _string.lstrip('\n\t') if start_even else _string

        headers = '\n'.join(
            f'{k}: {v}'
            for k, v in self.headers.items()
        )  # fmt: skip

        pages = (
            'none' if not self._is_paged
            else 'all' if self._all_pages
            else f'{self._start_page} -> {self._end_page}'
        )  # fmt: skip

        return '\n\t'.join(
            [
                f'\n\r{self.__class__.__name__}',
                f'Headers: {indent(headers, 2)}',
                f'URL: {self.url}',
                f'Endpoint: {self.endpoint}{indent(self.endpoint.value, 2)}',
                f'Path Params: {self._params}',
                f'Data: {indent(str(self._data), 2, start_even=True)}',
                f'Token: {self._endpoint.token_type}',
                f'Pages: {pages}',
                f'Retry: {self._should_retry}\n',
            ]
        ).expandtabs(4)


class SpaceTradersAPIRequestBuilder:
    def __init__(self, req: SpaceTradersAPIRequest) -> None:
        self.__called_endpoint: bool = False
        self.__called_path_params: bool = False
        self.__called_data: bool = False
        self.__called_page_method: bool = False
        self.__called_token: bool = False
        self.req: SpaceTradersAPIRequest = req

    def endpoint(self, endpoint: SpaceTradersAPIEndpoint) -> 'SpaceTradersAPIRequestBuilder':
        self.__called_endpoint = True

        if endpoint.request_shape is NoDataReqShape:
            _ = self.data(NoDataReqShape())

        self.req._endpoint = endpoint
        return self

    def data(self, data: SpaceTradersAPIReqShape) -> 'SpaceTradersAPIRequestBuilder':
        self.__check_must_call_endpoint_before('.data()')
        self.__called_data = True

        endpoint = self.req.endpoint
        if not isinstance(data, endpoint.request_shape):
            raise InvalidRequestError(
                f'Endpoint {endpoint.name} requires a {endpoint.request_shape} data. Received a {data.__repr_name__} data.'
            )

        self.req._data = data
        return self

    def headers(self, *headers: tuple[str, str]) -> 'SpaceTradersAPIRequestBuilder':
        for header in headers:
            key, value = header[0], header[1]
            self.req._headers[key] = value

        return self

    def path_params(self, *params: str) -> 'SpaceTradersAPIRequestBuilder':
        self.__check_must_call_endpoint_before('.path_params()')
        self.__called_path_params = True

        e_params = self.req.endpoint.get_query_params()
        l_e_params = len(e_params)
        p_params = [param for param in params if param != '']
        l_p_params = len(p_params)

        if l_p_params != l_e_params:
            raise InvalidRequestError(
                f'Endpoint {self.req.endpoint.name} requires {l_e_params} path params ({e_params}). Received {l_p_params} ({p_params})'
            )

        self.req._params = p_params
        return self

    # TODO: implement
    def pages(
        self, start: int | None = None, end: int | None = None
    ) -> 'SpaceTradersAPIRequestBuilder':
        self.__check_must_call_endpoint_before('.pages()')
        self.__called_page_method = True

        if self.req._is_paged:
            raise InvalidRequestError('cannot call .pages(...) after calling .all_pages()')

        start = 1 if start is None else start
        end = 1 if end is None else end

        if start > end:
            raise InvalidRequestError(f'{start=} must be less than {end=}')
        elif end > MAX_PAGE_LIMIT:
            raise InvalidRequestError(f'{end=} must be between 1 and {MAX_PAGE_LIMIT}')
        elif start < 1 and start > MAX_PAGE_LIMIT:
            raise InvalidRequestError(f'{start=} and {end=} must be between 1 and {MAX_PAGE_LIMIT}')

        self.req._start_page = start
        self.req._end_page = end
        self.req._is_paged = True
        return self

    def all_pages(self) -> 'SpaceTradersAPIRequestBuilder':
        self.__check_must_call_endpoint_before('.all_pages()')
        self.__called_page_method = True

        if self.req._is_paged:
            raise InvalidRequestError('cannot call .all_pages() after calling .pages(...)')

        self.req._all_pages = True
        self.req._is_paged = True
        return self

    def page_limit(self, limit: int) -> 'SpaceTradersAPIRequestBuilder':
        if limit < 1 or limit > MAX_PAGE_LIMIT:
            raise InvalidRequestError(f'{limit=} must be bewteen 1 and {MAX_PAGE_LIMIT}')

        self.req._page_limit = limit
        self.req._is_paged = True
        return self

    def retries(self, times: int) -> 'SpaceTradersAPIRequestBuilder':
        if times < 1:
            raise InvalidRequestError(f'times={times} must be greater than 1')
        self.req._retries = times
        self.req._should_retry = True
        return self

    def token(self) -> 'SpaceTradersAPIRequestBuilder':
        self.__check_must_call_endpoint_before('.token()')
        self.__called_token = True

        self.req._token = CONFIG.token if self.req._token is None else self.req._token
        self.req._headers['Authorization'] = f'Bearer {self.req._token}'
        return self

    def cancel_on_ratelimit(self) -> 'SpaceTradersAPIRequestBuilder':
        self.req._cancel_on_ratelimit = True
        return self

    def cancel_on_http_errors(self, *statuses: HTTPStatus) -> 'SpaceTradersAPIRequestBuilder':
        self.req._cancel_on_http_errors = [status for status in statuses]
        return self

    def cancel_on_spacetrader_errors(
        self, *codes: SpaceTradersAPIErrorCodes
    ) -> 'SpaceTradersAPIRequestBuilder':
        self.req._cancel_on_spacetrader_errors = [code for code in codes]
        return self

    def timeout(self, seconds: int) -> 'SpaceTradersAPIRequestBuilder':
        self.req._timeout = seconds
        return self

    def build(self) -> SpaceTradersAPIRequest:
        if not self.__called_endpoint:
            raise InvalidRequestError('')

        if self.req.endpoint and not self.__called_path_params:
            raise InvalidRequestError('')

        if self.req.endpoint.request_shape is not NoDataReqShape and not self.__called_data:
            raise InvalidRequestError('')

        if self.req.endpoint.paginated and not self.__called_page_method:
            raise InvalidRequestError('')

        if self.req.endpoint.token_type is not TokenType.NONE and not self.__called_token:
            raise InvalidRequestError('')

        # Default headers
        if self.req.endpoint.request_shape is not NoDataReqShape:
            self.req._headers['Content-Type'] = 'application/json'

        return self.req

    def __check_must_call_endpoint_before(self, method: str) -> None:
        if not self.__called_endpoint:
            raise InvalidRequestError(
                f'Must call .endpoint() before calling {method}'
            )
