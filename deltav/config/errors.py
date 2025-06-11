from __future__ import annotations


class UnsupportedPlatformError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class ConfigNotFoundError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class NotATomlDocument(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


