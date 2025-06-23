from __future__ import annotations

from deltav.config.config import Config
from deltav.spacetraders.account import Account
from deltav.spacetraders.agent import Agent
from deltav.spacetraders.game import SpaceTradersGame


class Deltav():
    config: Config
    spacetraders: SpaceTradersGame
    accounts: dict[str, Account] = {}
    agents: dict[str, Agent] = {}

    def __init__(self, config: Config | None = None) -> None:
        Deltav.config = config or Config()

        for account in Deltav.config.spacetraders.accounts.values():
            for agent in account.agents.values():
                Deltav.agents[agent.symbol] = Agent(agent.token)
                if account.token.hash not in Deltav.accounts:
                    Deltav.accounts[account.token.hash] = Account(account.token, agent.token)

        Deltav.spacetraders = SpaceTradersGame()

    @classmethod
    def get_account(cls, symbol: str) -> Account:
        return cls.accounts[symbol.upper()]

    @classmethod
    def get_agent(cls, symbol: str) -> Agent:
        return cls.agents[symbol.upper()]
