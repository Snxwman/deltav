# pyright: reportPrivateUsage=false

from collections.abc import Mapping
from http import HTTPStatus
from math import ceil
from typing import Any, Generic, TypeVar, override

from loguru import logger

from deltav.config.config import Config
from deltav.spacetraders.api import DEFAULT_PAGE_LIMIT, MAX_PAGE_LIMIT, SPACETRADERS_API_URL
from deltav.spacetraders.enums.endpoints import SpaceTradersAPIEndpoint
from deltav.spacetraders.enums.error import SpaceTradersAPIErrorCodes
from deltav.spacetraders.errors.request import InvalidRequestError
from deltav.spacetraders.models import NoDataReqShape, SpaceTradersAPIReqShape, SpaceTradersAPIResShape, UnknownReqShape
from deltav.spacetraders.token import AccountToken, AgentToken
from deltav.util import generic__repr__


T = TypeVar('T', bound=SpaceTradersAPIResShape)


class SpaceTradersAPIRequest(Generic[T]):
    """A builder class for SpaceTraders API Requests"""

    def __init__(self) -> None:
        self._endpoint: SpaceTradersAPIEndpoint = SpaceTradersAPIEndpoint.GET_SERVER_STATUS
        self._headers: dict[str, str] = {}
        self._path_params: list[str] = []
        self._query_params: dict[str, str] = {}
        self._data: SpaceTradersAPIReqShape = UnknownReqShape()

        # Paging properties
        self._is_paged: bool = False
        self._all_pages: bool = False
        self._start_page: int = 0
        self._end_page: int = 0
        self._page_limit: int = DEFAULT_PAGE_LIMIT
        # Paging state
        self._total_items: int = 0
        self._total_pages: int = 1
        self._current_page: int = 1

        # Retry properties
        self._should_retry: bool = False
        self._retries: int | None = None
        self._cancel_on_ratelimit: bool = False
        self._cancel_on_http_errors: list[HTTPStatus] = []
        self._cancel_on_spacetrader_errors: list[SpaceTradersAPIErrorCodes] = []
        self._timeout_connect: int = 5
        self._timeout_response: int = 60

        # The token to use for the request, could be account or agent
        self._token: AccountToken | AgentToken | None = None

    @property
    def endpoint(self) -> SpaceTradersAPIEndpoint:
        return self._endpoint

    @property
    def json_data(self) -> Mapping[str, Any]:
        if self.endpoint.request_shape is NoDataReqShape:
            return {}
        else:
            return self._data.model_dump(mode='json', by_alias=True)

    @property
    def headers(self) -> dict[str, str]:
        return self._headers

    @property
    def params(self) -> dict[str, Any]:
        params: dict[str, Any] = {}

        if self.is_paged:
            params.update({
                'page': self.current_page,
                'limit': self.page_limit,
            })  # fmt: skip

        if self.has_query:
            params.update(self._query_params)

        return params

    @property
    def has_query(self) -> bool:
        return bool(self._query_params)

    @property
    def is_paged(self) -> bool:
        return self._is_paged

    @property
    def all_pages(self) -> bool:
        return self._all_pages

    @property
    def start_page(self) -> int:
        return self._start_page if self._start_page > 0 else 1

    @property
    def end_page(self) -> int:
        return self._end_page if self._start_page <= self._end_page else self._start_page

    @property
    def page_limit(self) -> int:
        return self._page_limit

    @property
    def total_pages(self) -> int:
        return self._total_pages

    @total_pages.setter
    def total_items(self, items: int) -> None:
        self._total_items = items
        self._total_pages = ceil(items / self.page_limit)

    @property
    def current_page(self) -> int:
        return self._current_page

    @property
    def next_page(self) -> int | None:
        next = self._current_page + 1
        return next if next < self._total_pages else None

    @property
    def timeout_connect(self) -> int:
        return self._timeout_connect

    @property
    def timeout_response(self) -> int:
        return self._timeout_response

    def parameterized_path(self) -> str:
        mapping = dict(zip(self.endpoint.path.get_identifiers(), self._path_params))
        path = self._endpoint.path.substitute(mapping)
        return path[1:] if path[0] == '/' else path

    def page_frag(self, page: int) -> str:
        return f'page={page}&limit={self._page_limit}'

    def query_frag(self) -> str:
        return '&'.join(f'{k}={v}' for k, v in self._query_params.items())

    @property
    def url(self) -> str:
        return f'{SPACETRADERS_API_URL}/{self.parameterized_path()}'

    def builder(self) -> 'SpaceTradersAPIRequestBuilder[T]':
        return SpaceTradersAPIRequestBuilder[T](self)

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
                f'URL: {self.url}',
                f'Headers: {indent(headers, 2)}',
                f'Endpoint: {self.endpoint}{indent(self.endpoint.value, 2)}',
                f'Path Params: {self._path_params}',
                f'Page Params: {self._path_params}',
                f'Query Params: {self._query_params}',
                f'Data: {indent(str(self._data), 2, start_even=True)}',
                f'Token: {self._endpoint.token_type}',
                f'Pages: {pages}',
                f'Retry: {self._should_retry}\n',
            ]
        ).expandtabs(4)


class SpaceTradersAPIRequestBuilder(Generic[T]):
    def __init__(self, req: SpaceTradersAPIRequest[T]) -> None:
        self.__called_endpoint: bool = False
        self.__called_path_params: bool = False
        self.__called_data: bool = False
        self.__called_page_method: bool = False
        self.__called_token: bool = False
        self.req: SpaceTradersAPIRequest[T] = req

    def endpoint(self, endpoint: SpaceTradersAPIEndpoint) -> 'SpaceTradersAPIRequestBuilder[T]':
        self.__called_endpoint = True

        if endpoint.request_shape is NoDataReqShape:
            _ = self.data(NoDataReqShape())

        self.req._endpoint = endpoint
        return self

    def data(self, data: SpaceTradersAPIReqShape) -> 'SpaceTradersAPIRequestBuilder[T]':
        self.__check_must_call_endpoint_before('.data()')
        self.__called_data = True

        endpoint = self.req.endpoint
        if not isinstance(data, endpoint.request_shape):
            raise InvalidRequestError(
                f'Endpoint {endpoint.name} requires a {endpoint.request_shape} data. Received a {data.__repr_name__} data.'
            )

        self.req._data = data
        return self

    def headers(self, *headers: tuple[str, str]) -> 'SpaceTradersAPIRequestBuilder[T]':
        for header in headers:
            key, value = header[0], header[1]
            self.req._headers[key] = value

        return self

    def path_params(self, *params: str) -> 'SpaceTradersAPIRequestBuilder[T]':
        self.__check_must_call_endpoint_before('.path_params()')
        self.__called_path_params = True

        e_params = self.req.endpoint.get_path_params()
        l_e_params = len(e_params)
        p_params = [param for param in params if param != '']
        l_p_params = len(p_params)

        if l_p_params != l_e_params:
            raise InvalidRequestError(
                f'Endpoint {self.req.endpoint.name} requires {l_e_params} path params ({e_params}). Received {l_p_params} ({p_params})'
            )

        self.req._path_params = p_params
        return self

    # TODO: implement
    def pages(self, start: int | None = None, end: int | None = None) -> 'SpaceTradersAPIRequestBuilder[T]':
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

    def all_pages(self) -> 'SpaceTradersAPIRequestBuilder[T]':
        self.__check_must_call_endpoint_before('.all_pages()')
        self.__called_page_method = True

        if self.req._is_paged:
            raise InvalidRequestError('cannot call .all_pages() after calling .pages(...)')

        self.req._all_pages = True
        self.req._is_paged = True
        return self

    def page_limit(self, limit: int) -> 'SpaceTradersAPIRequestBuilder[T]':
        if limit < 1 or limit > MAX_PAGE_LIMIT:
            raise InvalidRequestError(f'{limit=} must be bewteen 1 and {MAX_PAGE_LIMIT}')

        self.req._page_limit = limit
        self.req._is_paged = True
        return self

    def retries(self, times: int) -> 'SpaceTradersAPIRequestBuilder[T]':
        if times < 1:
            raise InvalidRequestError(f'times={times} must be greater than 1')
        self.req._retries = times
        self.req._should_retry = True
        return self

    # TODO: Find a better way to get account and agent
    def token(self, token: AccountToken | AgentToken | None = None) -> 'SpaceTradersAPIRequestBuilder[T]':
        self.__check_must_call_endpoint_before('.token()')
        self.__called_token = True

        if self.req.endpoint.token_type is None:
            logger.warning('No token type needed for this endpoint')
            return self

        if not isinstance(token, self.req.endpoint.token_type):
            raise TypeError(f'Endpoint {self.req.endpoint.name} requires {self.req.endpoint.token_type}')

        self.req._token = token
        self.req._headers['Authorization'] = f'Bearer {self.req._token}'
        return self

    def cancel_on_ratelimit(self) -> 'SpaceTradersAPIRequestBuilder[T]':
        self.req._cancel_on_ratelimit = True
        return self

    def cancel_on_http_errors(self, *statuses: HTTPStatus) -> 'SpaceTradersAPIRequestBuilder[T]':
        self.req._cancel_on_http_errors = [status for status in statuses]
        return self

    def cancel_on_spacetrader_errors(self, *codes: SpaceTradersAPIErrorCodes) -> 'SpaceTradersAPIRequestBuilder[T]':
        self.req._cancel_on_spacetrader_errors = [code for code in codes]
        return self

    def timeout(self, seconds: int) -> 'SpaceTradersAPIRequestBuilder[T]':
        self.req._timeout_response = seconds
        return self

    def build(self) -> SpaceTradersAPIRequest[T]:
        if not self.__called_endpoint:
            raise InvalidRequestError('')

        if self.req.endpoint.get_path_params() and not self.__called_path_params:
            raise InvalidRequestError('')

        if self.req.endpoint.request_shape is not NoDataReqShape and not self.__called_data:
            raise InvalidRequestError('')

        if self.req.endpoint.paginated and not self.__called_page_method:
            raise InvalidRequestError('')

        if self.req.endpoint.token_type is not None and not self.__called_token:
            raise InvalidRequestError('')

        # Default headers
        if self.req.endpoint.request_shape is not NoDataReqShape:
            self.req._headers['Content-Type'] = 'application/json'

        # Setup paging state
        if self.req.is_paged and self.req.all_pages:
            self.req._current_page = 1
        elif self.req.is_paged:
            self.req._current_page = self.req.start_page

        return self.req

    def __check_must_call_endpoint_before(self, method: str) -> None:
        if not self.__called_endpoint:
            raise InvalidRequestError(f'Must call .endpoint() before calling {method}')
