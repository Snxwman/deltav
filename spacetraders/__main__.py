from spacetraders.api.api import SpaceTradersAPI, SpaceTradersAPIRequest
from spacetraders.api.endpoints import SpaceTradersAPIEndpoint as e
from spacetraders import cli

from spacetraders.config import Config

def main():
    client = SpaceTradersAPI()
    cli.run(client)

if __name__ == '__main__':
    main()
