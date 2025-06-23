from __future__ import annotations

import signal
import sys
from enum import Enum, auto
from types import FrameType  # noqa: TC003

from loguru import logger

from deltav.config.config import Config
from deltav.deltav import Deltav
from deltav.spacetraders.api.client import SpaceTradersAPIClient
from deltav.store.db import Base, engine
from deltav.store.db.account import AccountRecord


class LaunchMode(Enum):
    CLI = auto()
    TUI = auto()
    DAEMON = auto()


def signal_handler(sig: int, _: FrameType | None) -> None:
    match sig:
        case signal.SIGINT:
            SpaceTradersAPIClient.http_client.close()
            sys.exit(0)
        case _:
            pass


def main(launch_mode: LaunchMode):
    logger.trace('Registering signal handlers')
    _ = signal.signal(signal.SIGINT, signal_handler)

    logger.trace('Initializing database')
    Base.metadata.create_all(engine)

    logger.trace('Initializing config')
    config = Config()

    AccountRecord.preload_from_config(list(config.spacetraders.accounts.values()))

    logger.trace('Initializing SpaceTradersAPIClient')
    _ = SpaceTradersAPIClient()

    logger.trace('Initializing Deltav object')
    _ = Deltav()

    match launch_mode:
        case LaunchMode.CLI:
            logger.trace('Launching deltav cli')
            from deltav import cli

            cli.run()

        case LaunchMode.TUI:
            logger.trace('Launching vantage tui')
            from deltav.vantage import __main__ as vantage

            vantage.main()

        case LaunchMode.DAEMON:
            # TODO: implement functionality
            ...


def launch_deltav():
    main(LaunchMode.CLI)


def launch_vantage():
    main(LaunchMode.TUI)
