import signal
import sys
from types import FrameType

from deltav import cli
from deltav.spacetraders.api.client import SpaceTradersAPIClient


def signal_handler(sig: int, frame: FrameType | None) -> None:
    match sig:
        case signal.CTRL_C_EVENT | signal.SIGINT:
            SpaceTradersAPIClient.http_client.close()
            sys.exit(0)
        case _:
            pass


def main():
    _ = signal.signal(signal.SIGINT, signal_handler)

    _ = SpaceTradersAPIClient()
    cli.run()


if __name__ == '__main__':
    main()
