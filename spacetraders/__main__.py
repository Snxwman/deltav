from spacetraders.api.api import SpaceTradersAPI, SpaceTradersAPIRequest
from spacetraders import cli


def main():
    client = SpaceTradersAPI()
    cli.run(client)

if __name__ == '__main__':
    main()
