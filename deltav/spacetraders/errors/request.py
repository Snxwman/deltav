from __future__ import annotations


class InvalidRequestError(Exception):
    def __init__(self, message: str) -> None:
        self.message: str = message
        super().__init__(self.message)


class NoEndpointError(Exception):
    def __init__(self, message: str) -> None:
        self.message: str = message
        super().__init__(self.message)


class InvalidEndpointError(Exception):
    def __init__(self, message: str) -> None:
        self.message: str = message
        super().__init__(self.message)


class NoRequestDataError(Exception):
    def __init__(self, message: str) -> None:
        self.message: str = message
        super().__init__(self.message)


class InvalidRequestShapeError(Exception):
    def __init__(self, message: str) -> None:
        self.message: str = message
        super().__init__(self.message)


class InvalidResponseShapeError(Exception):
    def __init__(self, message: str) -> None:
        self.message: str = message
        super().__init__(self.message)
