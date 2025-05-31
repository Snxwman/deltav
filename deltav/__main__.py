from deltav import cli
from deltav.spacetraders.api.client import SpaceTradersAPIClient


def main():
    client = SpaceTradersAPIClient()
    cli.run(client)


if __name__ == '__main__':
    main()
