import tomlkit

class Config:

    def __init__(self, config_path):
        self._config_path = config_path
        raw_config = self._from_file()

        self.token: str = str(raw_config['token'])
        self.agent_token: str = str(raw_config['agent_token'])
        self.email: str = str(raw_config['email'])

        self.accountID: str = str(raw_config['accountID'])

    def _from_file(self):
        with open(self._config_path) as config_file:
            return tomlkit.load(config_file)

CONFIG = Config('config.toml')
# print(f'account-token: {CONFIG.token}')
# print(f'agent-token: {CONFIG.agent_token}')
