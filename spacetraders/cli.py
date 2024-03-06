from typing import Any, Callable, Optional
from spacetraders.config import CONFIG
from spacetraders.api.agent import Agent, RegisterAgentData
from spacetraders.api.api import SpaceTradersAPI
from spacetraders.defaults import Defaults

DEFAULT_FACTION = 'COSMIC'

def index_or_none(indexable, index: int) -> (Any | None):
    try:
        return indexable[index]
    except IndexError:
        return None

def get_next_command() -> list[str]:
    raw = input("cmd > ")
    return raw.split(' ')


def make_new_agent(args: list):
    callsign: str = ''
    faction: str = ''
    email: str = ''

    def generate_callsign() -> str:
        return 'test_user'

    def validate_callsign(callsign) -> bool:
        return len(callsign) <= 14

    def get_prompt_answer(prompt:str='', 
                          answer=None, 
                          default=None, 
                          generate:Optional[Callable]=None, 
                          validate:Optional[Callable]=None, 
                          allow_empty=False) -> str:

        while ( answer is None or
                answer == '' and allow_empty is False or
                validate is not None and validate(answer) is False ):
            answer = input(prompt)

        match answer:
            case '{}' if generate is not None:
                return generate()
            case '-' if default is not None:
                return default
            case '' if allow_empty:
                return answer
            case _:
                return answer

    def get_callsign(arg=None) -> str:
        prompt = '[REQ] Enter agent\'s callsign: '
        answer = get_prompt_answer(prompt=prompt, answer=arg, 
                                   generate=generate_callsign, 
                                   validate=validate_callsign)
        return answer.upper()

    def get_faction(arg=None):
        default = Defaults.FACTION.value
        prompt = f'[OPT] Enter agent\'s faction (default: {default}): '
        answer = get_prompt_answer(prompt=prompt, answer=arg, default=default)
        return answer.upper()

    def get_email(arg=None):
        prompt = '[OPT] Enter account email: '
        answer = get_prompt_answer(prompt=prompt, answer=arg, default=CONFIG.email, allow_empty=True)
        return answer

    def confirm_agent_details() -> bool:
        confirm = input('Confirm new agent details (y) or change value (callsign, faction, email): ')

        match confirm:
            case 'y':
                return True
            case 'callsign':
                agent_data['symbol'] = get_callsign()
            case 'faction':
                agent_data['faction'] = get_faction()
            case 'email':
                agent_data['email'] = get_email()

        return False

    callsign = get_callsign(arg=index_or_none(args, 1)) 
    faction = get_faction(arg=index_or_none(args, 2))
    email = get_email(arg=index_or_none(args, 3)) 

    agent_data: RegisterAgentData = {
        'symbol': callsign,
        'faction': faction,
        'email': email,
    } 
    
    while confirm_agent_details() is not True:
        print(agent_data)
    
    Agent.register(agent_data)


def usage():
    print('quit, new')


def run(client: SpaceTradersAPI):
    quit = False

    while not quit:
        args = list(filter(len, get_next_command()))

        match args[0]:
            case 'q' | 'quit':
                quit = True
            case 'h' | 'help':
                usage()
            case 'game':
                SpaceTradersAPI.game_state()
            case 'new' | 'new-agent':
                make_new_agent(args)

