from __future__ import annotations

from datetime import datetime

from deltav.spacetraders.agent import PublicAgent
from deltav.spacetraders.api.error import SpaceTradersAPIError
from deltav.spacetraders.models.chart import ChartShape


class Chart:
    def __init__(self) -> None:
        self.__synced_db: bool = False

        self.__data: ChartShape
        self.__data_timestamp: datetime

        self._submitted_by: PublicAgent
        self._submitted_on: datetime

    @property
    def submitted_by(self) -> PublicAgent:
        return self._submitted_by

    @property
    def submitted_on(self) -> datetime:
        return self._submitted_on

    @staticmethod
    def _create_chart() -> ChartShape | SpaceTradersAPIError: ...
