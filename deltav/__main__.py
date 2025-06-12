from __future__ import annotations

import signal
import sys
from types import FrameType

from loguru import logger
from sqlalchemy import Engine, create_engine, select

from deltav import cli
from deltav.spacetraders.api.client import SpaceTradersAPIClient
from deltav.store.db import Base, Session
from deltav.store.db.ship import ShipRecord


def signal_handler(sig: int, frame: FrameType | None) -> None:
    match sig:
        case signal.SIGINT:
            SpaceTradersAPIClient.http_client.close()
            sys.exit(0)
        case _:
            pass


def main():
    logger.trace('Registering signal handlers')
    _ = signal.signal(signal.SIGINT, signal_handler)

    engine: Engine = create_engine('sqlite:///deltav.db', echo=True)
    Base.metadata.create_all(engine)

    sys.exit()

    logger.trace('Initializing SpaceTradersAPIClient')
    _ = SpaceTradersAPIClient()

    logger.trace('Running CLI')
    cli.run()


if __name__ == '__main__':
    main()
