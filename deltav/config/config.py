# pyright: reportAny=false
# pyright: reportAssignmentType=false
# pyright: reportAttributeAccessIssue=false
# pyright: reportOptionalMemberAccess=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false

from __future__ import annotations

import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import override

import tomlkit
from loguru import logger
from tomlkit import TOMLDocument
from tomlkit.items import AoT, Table

from deltav.config import get_default_config_paths, get_default_db_path, get_default_log_path
from deltav.config.errors import ConfigNotFoundError
from deltav.spacetraders.enums.faction import FactionSymbol
from deltav.spacetraders.token import AccountToken, AgentToken
from deltav.util import generic__repr__
from deltav.util.strings import indent


class LogLevel(Enum):
    NONE = 100
    CRITICAL = 50
    ERROR = 40
    WARN = 30
    INFO = 20
    SUCCESS = 25
    DEBUG = 10
    TRACE = 5

    @staticmethod
    def default() -> LogLevel:
        return LogLevel.INFO


@dataclass
class DeltavConfig:
    proxy: str | None = None
    log_level: LogLevel = LogLevel.default()
    log_directory: Path = get_default_log_path()
    db_directory: Path = get_default_db_path()

    @override
    def __str__(self) -> str:
        return '\n\t'.join([
            'DeltaV',
            f'Proxy: {self.proxy}',
            f'Logging:\n\t\tLevel: {self.log_level.name.lower()}\n\t\tDir: {self.log_directory}',
            f'Database:\n\t\tDir: {self.db_directory}',
        ])  # fmt: skip


@dataclass
class VantageConfig:
    theme: str = 'dark'

    @override
    def __str__(self) -> str:
        return '\n\t'.join([
            'Vantage',
            f'Theme: {self.theme}'
        ])  # fmt: skip


@dataclass
class StAccountConfig:
    nickname: str
    email: str
    token: AccountToken
    agents: dict[str, StAgentConfig]
    autocreate: bool = False
    proxy: str | None = None

    def get_agent(self, agent: str) -> StAgentConfig:
        agent_config = self.agents.get(agent, None)
        if agent_config is None:
            raise ValueError(f'No agent {agent} found.')
        return agent_config

    @override
    def __str__(self) -> str:
        agents = ''.join(str(agent) for agent in self.agents.values())
        return '\n\t'.join([
            f'nickname: {self.nickname}',
            f'email: {self.email}',
            f'token: {self.token.hash}',
            f'autocreate: {self.autocreate}',
            f'proxy: {self.proxy}',
            f'agents: {indent(agents, 2)}',
        ])  # fmt: skip


@dataclass
class StAgentConfig:
    nickname: str
    symbol: str
    faction: FactionSymbol
    token: AgentToken
    account: str
    autocreate: bool = False

    @override
    def __str__(self) -> str:
        name = (
            f'{self.symbol} ({self.nickname})'
            if self.symbol != self.nickname
            else f'{self.nickname}'
        )
        return '\n\t'.join([
            f'\n{name}',
            f'token: {self.token.hash}',
            f'autocreate: {self.autocreate}',
        ])  # fmt: skip


@dataclass
class StConfig:
    accounts: dict[str, StAccountConfig]
    default_email: str
    default_autocreate_accounts: bool = False
    default_autocreate_agents: bool = False

    def get_account(self, agent: str) -> StAccountConfig:
        account_config = self.accounts.get(agent, None)
        if account_config is None:
            raise ValueError(f'No agent {agent} found.')
        return account_config

    @override
    def __str__(self) -> str:
        accounts = ''.join(f'\n{str(account)}' for account in self.accounts.values())

        return '\n\t'.join([
            'Defaults:',
            f'Email: {self.default_email}',
            'Autocreate:',
            f'\tAccounts: {self.default_autocreate_accounts}',
            f'\tAgents: {self.default_autocreate_agents}',
            f'Accounts: {indent(accounts, 2)}',
        ])  # fmt: skip


# FIX: Temporary hacky impl
class Config:
    __accounts: dict[str, StAccountConfig] = {}

    def __init__(self, path: Path | str | None = None):
        logger.debug('Loading config')
        self.__config_file_path: Path = Config.__locate_config_file(path)
        self.__original_toml: TOMLDocument = self.__load_toml_file()
        self.__current_toml: TOMLDocument = self.__load_toml_file()
        self.deltav: DeltavConfig = DeltavConfig()
        self.vantage: VantageConfig = VantageConfig()
        self.spacetraders: StConfig

        toml_deltav: Table = self.__original_toml.get('deltav')
        log_level = toml_deltav.get('log').get('level', self.deltav.log_level)
        if isinstance(log_level, str):
            log_level = LogLevel[log_level.upper()]
        self.deltav = DeltavConfig(
            proxy=toml_deltav.get('proxy', None),
            log_level=log_level,
            log_directory=toml_deltav.get('log.directory', self.deltav.log_directory),
            db_directory=toml_deltav.get('directory', self.deltav.db_directory),
        )

        logger.remove()
        _ = logger.add(sys.stderr, level=self.deltav.log_level.name.upper())
        logger.trace('Loaded table: [deltav]')

        toml_vantage: Table = self.__original_toml.get('vantage')
        self.vantage = VantageConfig(theme=toml_vantage.get('theme', self.vantage.theme))
        logger.trace('Loaded table: [vantage]')

        toml_st_default: Table = self.__original_toml.get('spacetraders').get('defaults')
        default_email: str = toml_st_default.get('email')
        self.spacetraders = StConfig(
            default_email=default_email,
            default_autocreate_accounts=toml_st_default.get('autocreate.accounts', False),
            default_autocreate_agents=toml_st_default.get('autocreate.agents', False),
            accounts={},
        )
        logger.trace('Loaded table: [spacetraders.defaults]')

        toml_st_accounts: AoT = self.__original_toml.get('spacetraders').get('accounts')
        for account in toml_st_accounts:
            nick = account.get('nickname').lower()
            account = StAccountConfig(
                nickname=nick,
                email=account.get('email', self.spacetraders.default_email),
                token=AccountToken(account.get('token')),
                autocreate=account.get('autocreate', False),
                proxy=account.get('proxy', None),
                agents={},
            )
            self.spacetraders.accounts[nick] = account
            Config.__accounts[nick] = account
            logger.debug(f'Loaded account: {nick}')
        logger.trace('Loaded tables: [[spacetraders.accounts]]')

        toml_st_agents: AoT = self.__original_toml.get('spacetraders').get('agents')
        for agent in toml_st_agents:
            account: StAccountConfig = self.get_account(agent.get('account'))
            nick: str = agent.get('nickname', agent.get('callsign')).lower()
            faction = agent.get('faction', 'cosmic').upper()
            agent = StAgentConfig(
                nickname=nick,
                account=agent.get('account').lower(),
                symbol=agent.get('callsign').lower(),
                faction=FactionSymbol[faction],
                token=AgentToken(agent.get('token')),
                autocreate=agent.get('autocreate', False),
            )
            account.agents[nick] = agent
            logger.debug(f'Loaded agent: ({account.nickname}) {nick}')
        logger.trace('Loaded tables: [[spacetraders.agents]]')
        logger.success('Loaded config')
        logger.trace(f'Config values: {self}')

    def update_agent_token(self, token: AgentToken) -> None: ...

    @classmethod
    def get_account(cls, account: str) -> StAccountConfig:
        """Get an account config object by account nickname"""
        account_config = cls.__accounts.get(account, None)

        if account_config is None:
            raise ValueError(f'No account {account} found.')

        return account_config

    @classmethod
    def get_account_from_agent_token(cls, token: AgentToken) -> StAccountConfig | None:
        for account in cls.__accounts.values():
            for agent in account.agents.values():
                if token.agent_symbol.lower() == agent.symbol:
                    return account
        return None

    @classmethod
    def get_account_from_token(cls, token: AccountToken) -> StAccountConfig | None:
        for account in cls.__accounts.values():
            if account.token == token:
                return account
        return None

    @classmethod
    def get_agent(cls, account: str, agent: str) -> StAgentConfig:
        """Get an agent config object by account nickname and agent nickname.
        Agent nicknames default to thier callsigns (symbols) unless explicity set.
        """
        account_config = cls.get_account(account)
        return account_config.get_agent(agent.lower())

    @classmethod
    def get_agent_from_token(cls, token: AgentToken) -> StAgentConfig | None:
        for account in cls.__accounts.values():
            for agent in account.agents.values():
                if agent.token == token:
                    return agent

    def __load_toml_file(self) -> TOMLDocument:
        if not self.__config_file_path:
            raise ValueError(
                'self.__config_file_path must be set before calling self.__get_toml_from_file()'
            )

        with open(self.__config_file_path, 'r') as config_file:
            return tomlkit.load(config_file)

    def __write_toml_file(self) -> None:
        backup_path = Path(f'{self.__config_file_path}.bak')

        with open(backup_path, 'w') as backup_file:
            tomlkit.dump(self.__original_toml, backup_file)

        with open(self.__config_file_path, 'w') as config_file:
            tomlkit.dump(self.__original_toml, config_file)

    @staticmethod
    def __locate_config_file(path: Path | str | None) -> Path:
        # Path was passed in
        if path is not None:
            _path = Path(path)
            if _path.is_file():
                logger.debug(f'Using config file: {_path}')
                return _path
            else:
                raise ValueError(f'Path {_path} is not a file.')

        # Path was not passed in
        default_paths = get_default_config_paths()
        for default_path in default_paths:
            if default_path.is_file():
                logger.debug(f'Found config file: {default_path}')
                return default_path

        raise ConfigNotFoundError(
            f"""Path to config file was not provided, and none at default locations:
            \r\t{'\n\t'.join(f'- {default_path}' for default_path in default_paths)}"""
        )

    @staticmethod
    def __verify_or_make_dir() -> None: ...

    @override
    def __repr__(self) -> str:
        return generic__repr__(self)

    @override
    def __str__(self) -> str:
        return '\n' + '\n'.join([
            f'{self.deltav}',
            f'{self.vantage}',
            f'{self.spacetraders}',
        ]).expandtabs(4)  # fmt: skip
