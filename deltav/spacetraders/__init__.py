from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import Enum, auto
from typing import Generic, NamedTuple, TypeVar

from deltav.spacetraders.models import SpaceTradersAPIResShape
from deltav.store.db import Base


class Coordinate(NamedTuple):
    """
    ```
    Coordinate(NamedTuple)
        x: int
        y: int
    ```
    """

    x: int
    y: int


class DataSource(Enum):
    """
    API
    DB
    MANUAL
    """

    API = auto()
    DB = auto()
    MANUAL = auto()


Shape = TypeVar('Shape', bound=SpaceTradersAPIResShape)
Record = TypeVar('Record', bound=Base)
D = TypeVar('D')


@dataclass
class BackingData(Generic[D]):
    _data: D
    _synced: bool = False
    _timestamp: datetime | None = None

    @property
    def data(self) -> D:
        return self._data

    @data.setter
    def data(self, data: D) -> None:
        self._data = data

    @property
    def synced(self) -> bool:
        return self._synced

    @property
    def timestamp(self) -> datetime | None:
        return self._timestamp


@dataclass
class BackedData(Generic[Shape, Record]):
    """A container type for a class' backing data

    ```
    Shape = TypeVar('Shape', bound=SpaceTradersAPIResShape)
    Record = TypeVar('Record', bound=Base)
    D = TypeVar('D')

    BackedData(Generic[Shape, Record])
        api: BackingData[Shape] | None = None
        db: BackingData[Record] | None = None

        @property
        def newest(self) -> BackingData[Shape] | BackingData[Record] | None: ...

    BackingData(Generic[D])
        _data: D
        _synced: bool = False
        _timestamp: datetime | None = None

        @data.setter
        def data(self, data: D) -> None: ...
    ```
    """

    api: BackingData[Shape] | None = None
    db: BackingData[Record] | None = None

    @property
    def newest(self) -> BackingData[Shape] | BackingData[Record] | None:
        def _match(
            v1: BackingData[Shape] | datetime | None, v2: BackingData[Record] | datetime | None
        ) -> BackingData[Shape] | BackingData[Record] | None:
            match (v1, v2):
                case (None, None):
                    return None
                case (_, None):
                    return self.api
                case (None, _):
                    return self.db
                case (_, _):
                    return _match(
                        self.api.timestamp,  # pyright: ignore[reportOptionalMemberAccess]
                        self.db.timestamp,  # pyright: ignore[reportOptionalMemberAccess]
                    )

        return _match(self.api, self.db)


T = TypeVar('T')


@dataclass
class Timestamped[T]:
    """A wrapped type for a value that tracks it's last modified time.
    ```
    Timestamped[T]
        value: T
        timestamp: datetime
    ```
    """

    _value: T
    _timestamp: datetime

    def __init__(self, value: T) -> None:
        self.value = value

    @property
    def value(self) -> T:
        return self._value

    @value.setter
    def value(self, value: T) -> None:
        self._value = value
        self._timestamp = datetime.now(tz=UTC)

    @property
    def timestamp(self) -> datetime:
        return self._timestamp


@dataclass
class Tracked[T]:
    """
    ```
    Tracked[T]
        _value: T
        _source: DataSource
        _timestamp: datetime
    ```
    """

    _value: T
    _source: DataSource
    _timestamp: datetime

    def __init__(self, data: tuple[T, DataSource]) -> None:
        self.value = data

    @property
    def value(self) -> T:
        return self._value

    @value.setter
    def value(self, data: tuple[T, DataSource]) -> None:
        self._value = data[0]
        self._source = data[1]
        self._timestamp = datetime.now(tz=UTC)

    @property
    def source(self) -> DataSource:
        return self._source

    @property
    def timestamp(self) -> datetime:
        return self._timestamp
