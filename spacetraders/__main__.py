from string import Template
from spacetraders.api.endpoints import SpaceTradersAPIEndpoint as e

from spacetraders.config import Config

def main():
    config = Config('config.toml')
    print(e.with_params(e.REGISTER, config.token))

if __name__ == '__main__':
    main()
