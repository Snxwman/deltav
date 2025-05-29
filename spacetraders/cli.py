from typing import Any, Callable, Optional
from spacetraders.config import CONFIG
from spacetraders.api.agent import Agent, RegisterAgentData
from spacetraders.api.api import SpaceTradersAPI
from spacetraders.defaults import Defaults
from spacetraders.api.ship import Ship

DEFAULT_FACTION = 'COSMIC'
active_agent: Optional[Agent] = None

def index_or_none(indexable, index: int) -> (Any | None):
    try:
        return indexable[index]
    except IndexError:
        return None

def get_next_command() -> list[str]:
    raw = input("cmd > ")
    return raw.split(' ')

def get_prompt_answer(
        prompt: str = '', 
        answer = None, 
        default = None, 
        generate: Callable | None = None, 
        validate: Callable | None = None, 
        allow_empty = False
        ) -> str:

        while (
            answer is None or
            answer == '' and allow_empty is False or
            validate is not None and validate(answer) is False
        ):
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


def make_new_agent(args: list[str]):
    callsign: str = ''
    faction: str = ''
    # email: str = ''


    def generate_callsign() -> str:
        return 'test_user'


    def validate_callsign(callsign) -> bool:
        return len(callsign) > 2 and len(callsign) < 15

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


    # def get_email(arg=None):
    #     prompt = '[OPT] Enter account email: '
    #     answer = get_prompt_answer(prompt=prompt, answer=arg, default=CONFIG.email, allow_empty=True)
    #     return answer


    def confirm_agent_details() -> bool:
        confirm = input('Confirm new agent details (y) or change value (callsign, faction): ')

        match confirm:
            case 'y':
                return True
            case 'callsign':
                agent_data['symbol'] = get_callsign()
            case 'faction':
                agent_data['faction'] = get_faction()
            # case 'email':
            #     agent_data['email'] = get_email()

        return False

    callsign = get_callsign(arg=index_or_none(args, 1)) 
    faction = get_faction(arg=index_or_none(args, 2))
    # email = get_email(arg=index_or_none(args, 3)) 

    agent_data: RegisterAgentData = {
        'symbol': callsign,
        'faction': faction,
        # 'email': email,
    } 
    
    while confirm_agent_details() is not True:
        print(agent_data)
    
    Agent.register(agent_data)


def usage():
    print('quit, new, continue, contract, game, ships, help')

def get_current_agent():
    agent_token = CONFIG.agent_token
    
    x = Agent.get_agent('AGENT_MOJO')
    print(x)

def accept_contract(active_agent):
    def get_contract_id(arg=None):
        default = Defaults.FACTION.value
        prompt = f'Enter Contract ID: '
        answer = get_prompt_answer(prompt=prompt, answer=arg, default=default)
        return answer
        
    # TODO: turn this into a function that lists available contracts
    contracts = Agent.my_contracts(active_agent)
    print(f'Contracts for {active_agent.callsign}:')
    count = 0
    for contract in contracts:
        terms = contract['terms']
        deliver = terms['deliver'][0]  
        print(f'#{count}:\tID: {contract['id']}\n\t\tAccepted: {contract['accepted']}\n\t\tDeadline: {terms['deadline']}\n\t\tPayout: {terms['payment']}')
        print(f'\t\tTerms: {deliver['tradeSymbol']} to {deliver['destinationSymbol']} ({deliver['unitsFulfilled']}/{deliver['unitsRequired']})')
        count += 1

    print('Select a contract to accept by entering its index (0-based):')
    arg = ''
    
    try:
        contract_chosen = get_contract_id(arg=index_or_none(arg, 1))
        contract_id = contracts[int(contract_chosen)]['id']
    
    except (IndexError, ValueError):
        print(f'Invalid contract index: {contract_chosen}. Please enter a valid index.')
        return
    try:
        contract = Agent.accept_contract(contract_id)
        print(f'Contract accepted: {contract}')
    except ValueError as e:
        print(f'Error accepting contract: {e}')
    except Exception as e:
        print(f'Unexpected error: {e}')

def ships(active_agent: Agent):
    
    def navigate(shipSymbol: str, waypointSymbol: str):
        print(f'Navigating ship {shipSymbol} to waypoint {waypointSymbol}...')
        try:
            Agent.navigate(shipSymbol, waypointSymbol)
            print(f'Ship {shipSymbol} is now navigating to {waypointSymbol}.')
        except ValueError as e:
            print(f'Error navigating ship: {e}')

    def scanWaypoints(shipSymbol: str):
        print(f'Scanning waypoints for ship {shipSymbol}...')
        try:
            waypoints = Agent.scan_waypoints(shipSymbol)
            print(f'Waypoints for ship {shipSymbol}:')
            count = 0
            for waypoint in waypoints:
                print(f'{count}- {waypoint["symbol"]} ({waypoint["type"]})')
                count += 1
        except Exception as e:
            print(f'Error scanning waypoints: {e}')
        
    def getNavStatus(shipSymbol: str):
        print(f'Getting navigation status for ship {shipSymbol}...')
        status = Agent.get_nav_status(shipSymbol)
        if not status:
            print(f'No navigation status found for ship {shipSymbol}. (Error likely)')
            return
        print(f'Navigation status for ship {shipSymbol}:')
        print(status)

    def orbitShip(shipSymbol: str):
        print(f'Orbiting ship {shipSymbol}...')
        try:
            Agent.orbit_ship(shipSymbol)
            print(f'Ship {shipSymbol} is now orbiting.')
        except ValueError as e:
            print(f'Error orbiting ship: {e}')
    
    def dockShip(shipSymbol: str):
        print(f'Docking ship {shipSymbol}...')
        try:
            Agent.dock_ship(shipSymbol)
            print(f'Ship {shipSymbol} is now docked.')
        except ValueError as e:
            print(f'Error docking ship: {e}')

    def purchaseCargo(shipSymbol: str, cargoSymbol: str, units):
        print(f'Purchasing {units} units of {cargoSymbol} for ship {shipSymbol}...')
        try:
            Agent.purchase_cargo(shipSymbol, cargoSymbol, units)
            print(f'Purchased {units} units of {cargoSymbol} for ship {shipSymbol}.')
        except ValueError as e:
            print(f'Error purchasing cargo: {e}')
        
        

    print('Printing ships details...')
    
    current_ships = Agent.my_ships(active_agent)

    if not current_ships:
        print(f'No ships found for agent {active_agent.callsign}.')
        return

    print(f'Ships for {active_agent.callsign}:')
    for x in range(len(current_ships)):
        ship = current_ships[x]
        print(f'#{x} + Ship Name: {ship['symbol']}\tLocation: {ship['nav']['waypointSymbol']}')
    
    # choose ship to do something with
    print('Select a ship by entering its index (0-based):')
    ship_chosen = int(input('Ship index: '))
    try:
        ship_index = ship_chosen
        if ship_index < 0 or ship_index >= len(current_ships):
            raise IndexError
        chosen_ship = current_ships[ship_index]
       
    except (IndexError, ValueError):
        print(f'Invalid ship index: {ship_chosen}. Please enter a valid index.')
        return
    
    print(f'You selected ship: {chosen_ship["symbol"]} at {chosen_ship["nav"]["waypointSymbol"]}')
    print("What would you like to do with this ship?")
    print('1. Scan waypoints')
    print('2. Navigate to a waypoint')
    print('3. Orbit Ship')
    print('4. Dock Ship')
    print('5. Get Status of Ship')
    print('6. Purchase Cargo')
    print('9. Deliver Cargo')


    action = input('Enter action number (1-9): ')
    if action == '1':
        print('Available waypoints:')
        scanWaypoints(chosen_ship['symbol'])
    elif action == '2':
        waypoint_symbol = input('Enter waypoint symbol to navigate to: ')
        navigate(chosen_ship['symbol'], waypoint_symbol.upper())
        if not waypoint_symbol:
            print('No waypoint symbol provided. Aborting navigation.')
            return
    elif action == '3':
        orbitShip(chosen_ship['symbol'])
    elif action == '4':
        dockShip(chosen_ship['symbol'])
    elif action == '5':
        getNavStatus(chosen_ship['symbol'])
    elif action == '6':
        cargo_symbol = input('Enter cargo symbol to purchase: ')
        units = input('Enter number of units to purchase: ')
        purchaseCargo(chosen_ship['symbol'], cargo_symbol, units)
    elif action == '9':
        print('Delivering cargo...')



def run(client: SpaceTradersAPI):
    quit = False
    active_agent = Agent.get_agent('AGENT_MOJO')
    print(f'Active agent: {active_agent.callsign} ({active_agent.starting_faction})')
    while not quit:
        args = list(filter(len, get_next_command()))

        match args[0]:
            case 'q' | 'quit' | 'e' | 'exit':
                quit = True
            case 'h' | 'help':
                usage()
            case 'game':
                SpaceTradersAPI.game_state()
            case 'new' | 'new-agent':
                make_new_agent(args)
            case 'current' | 'agent' | 'me':
                get_current_agent()
            # TODO: negotate contract
            case 'accept' | 'a' | 'contract' | 'accept-contract':
                accept_contract(active_agent)
            case 'ships' | 'ship' | 'my-ships' | 's':
                ships(active_agent)

