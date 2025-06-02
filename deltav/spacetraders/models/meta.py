from __future__ import annotations

from deltav.spacetraders.models import SpaceTradersAPIResShape


class MetaShape(SpaceTradersAPIResShape):
    total: int
    page: int
    limit: int
