from typing import Any, Callable, cast
import traceback

from deltav.config import CONFIG
from deltav.defaults import Defaults
from deltav.spacetraders.agent import Agent
from deltav.spacetraders.api.response import SpaceTradersAPIResponse
from deltav.spacetraders.enums.faction import FactionSymbol
from deltav.spacetraders.game import SpaceTradersGame
from deltav.spacetraders.models.agent import AgentShape, RegisterAgentData
from deltav.spacetraders.api.client import SpaceTradersAPIClient
from deltav.spacetraders.ship import Ship
from deltav.spacetraders.contract import Contract
from deltav.spacetraders.enums.error import SpaceTradersAPIErrorCodes
from deltav.spacetraders.api.error import SpaceTradersAPIError

DEFAULT_FACTION = 'COSMIC'
active_agent: AgentShape | None = None


# def index_or_none(indexable, index: int) -> (Any | None):
#     try:
#         return indexable[index]
#     except IndexError:
#         return None
#
#
def get_next_command() -> list[str]:
    raw = input("cmd > ")
    return raw.split(' ')


# def get_prompt_answer(
#         prompt: str = '', 
#         answer = None, 
#         default = None, 
#         generate: Callable | None = None,  # pyright: ignore[reportMissingTypeArgument]
#         validate: Callable | None = None,  # pyright: ignore[reportMissingTypeArgument] 
#         allow_empty = False
#     ) -> str:
#
#     while (
#         answer is None or
#         answer == '' and allow_empty is False or
#         validate is not None and validate(answer) is False
#     ):
#         answer = input(prompt)
#
#     match answer:
#         case '{}' if generate is not None:
#             return generate()
#         case '-' if default is not None:
#             return default
#         case '' if allow_empty:
#             return answer
#         case _:
#             return answer
#
#
# def make_new_agent(args: list[str]):
#     callsign: str = ''
#     faction: str = ''
#
#
#     def generate_callsign() -> str:
#         return 'test_user'
#
#
#     def validate_callsign(callsign) -> bool:
#         return len(callsign) > 2 and len(callsign) < 15
#
#
#     def get_callsign(arg=None) -> str:
#         prompt = '[REQ] Enter agent\'s callsign: '
#         answer = get_prompt_answer(
#             prompt=prompt,
#             answer=arg, 
#             generate=generate_callsign, 
#             validate=validate_callsign
#         )
#         return answer.upper()
#
#
#     def get_faction(arg=None):
#         default = Defaults.FACTION.value
#         prompt = f'[OPT] Enter agent\'s faction (default: {default}): '
#         answer = get_prompt_answer(prompt=prompt, answer=arg, default=default)
#         return answer.upper()
#
#
#     # def get_email(arg=None):
#     #     prompt = '[OPT] Enter account email: '
#     #     answer = get_prompt_answer(prompt=prompt, answer=arg, default=CONFIG.email, allow_empty=True)
#     #     return answer
#
#
#     def confirm_agent_details() -> bool:
#         confirm = input('Confirm new agent details (y) or change value (callsign, faction): ')
#
#         match confirm:
#             case 'y':
#                 return True
#             case 'callsign':
#                 agent_data['symbol'] = get_callsign()
#             case 'faction':
#                 agent_data['faction'] = FactionSymbol[get_faction().upper()]
#             # case 'email':
#             #     agent_data['email'] = get_email()
#
#         return False
#
#     callsign = get_callsign(arg=index_or_none(args, 1)) 
#     faction = get_faction(arg=index_or_none(args, 2))
#
#     agent_data: RegisterAgentData = {
#         'symbol': callsign,
#         'faction': FactionSymbol[faction.upper()],
#     } 
#     
#     while confirm_agent_details() is not True:
#         print(agent_data)
#     
#     Agent.register(agent_data)
#
#
# def usage():
#     print('quit, new, continue, contract, game, ships, help')
#
# def get_current_agent():
#     agent_token = CONFIG.agent_token
#     
#     x = Agent.get_agent('AGENT_MOJO')
#     print(x)
#
# def accept_contract(active_agent):
#     def get_contract_id(arg=None):
#         default = Defaults.FACTION.value
#         prompt = f'Enter Contract ID: '
#         answer = get_prompt_answer(prompt=prompt, answer=arg, default=default)
#         return answer
#
#
#     contracts = Contract.get_contracts(active_agent)
#     if not contracts:
#         print('No contracts found.')
#         return
#
#     arg = ''
#     try:
#         print('Select a contract to accept by entering its index (0-based):')
#         contract_chosen = int(get_contract_id(arg=index_or_none(arg, 1)))
#         contract_id = contracts[contract_chosen].id
#     
#     except (IndexError, ValueError):
#         print(f'Invalid contract index: {contract_chosen}. Please enter a valid index.')
#         return
#     try:
#         contract = Contract.accept(contract_id)
#     except Exception as e:
#         if isinstance(e, SpaceTradersAPIErrorCodes):
#             print(f'API Error: {e}')
#         else:
#             print(f'Unexpected error: {e}')
#             traceback.print_exc()
#
#
def get_contracts():
    print('Getting contracts for active agent...')
    contracts = Contract.get_contracts()

    # print(f'Contracts for {active_agent}:')
    if not contracts:
        print('No contracts found.')
        return
    count = 0
    print('Available contracts:')
    print(contracts)
    # for x in range(len(contracts)):
    #     print(f'#{x} {contracts[x]}')
def get_contract(contract_id: str):
    print('Getting contracts for active agent...')
    contract = Contract.get_contract(contract_id)

    # print(f'Contracts for {active_agent}:')
    if not contract:
        print('No contracts found.')
        return
    print(f'Contract {contract_id} details:')
    print(contract)
    count = 0
    # print('Available contracts:')
    # for x in range(len(contracts)):
    #     print(f'#{x} {contracts[x]}')
#
#g
# def ships(active_agent: Agent):
#     def navigate(shipSymbol: str, waypointSymbol: str):
#         print(f'Navigating ship {shipSymbol} to waypoint {waypointSymbol}...')
#         try:
#             Ship.navigate(shipSymbol, waypointSymbol)
#             print(f'Ship {shipSymbol} is now navigating to {waypointSymbol}.')
#         except ValueError as e:
#             print(f'Error navigating ship: {e}')
#
#
#     def scanWaypoints(shipSymbol: str):
#         print(f'Scanning waypoints for ship {shipSymbol}...')
#         try:
#             waypoints = Ship.scan_waypoints(shipSymbol)
#             print(f'Waypoints for ship {shipSymbol}:')
#             count = 0
#             print(waypoints)
#             # for waypoint in waypoints:
#             #     print(f'{count}- {waypoint["symbol"]} ({waypoint["type"]})')
#             #     count += 1
#         except Exception as e:
#             print(f'Error scanning waypoints: {e}')
#         
#
#     def getNavStatus(shipSymbol: str):
#         print(f'Getting navigation status for ship {shipSymbol}...')
#         status = Ship.get_nav_status(shipSymbol)
#         if not status:
#             print(f'No navigation status found for ship {shipSymbol}. (Error likely)')
#             return
#         print(f'Navigation status for ship {shipSymbol}:')
#         print(status)
#
#
#     def orbitShip(shipSymbol: str):
#         print(f'Orbiting ship {shipSymbol}...')
#         try:
#             Ship.orbit_ship(shipSymbol)
#             print(f'Ship {shipSymbol} is now orbiting.')
#         except ValueError as e:
#             print(f'Error orbiting ship: {e}')
#     
#
#     def dockShip(shipSymbol: str):
#         print(f'Docking ship {shipSymbol}...')
#         try:
#             Ship.dock_ship(shipSymbol)
#             print(f'Ship {shipSymbol} is now docked.')
#         except ValueError as e:
#             print(f'Error docking ship: {e}')
#
#
#     def purchaseCargo(shipSymbol: str, cargoSymbol: str, units):
#         print(f'Purchasing {units} units of {cargoSymbol} for ship {shipSymbol}...')
#         try:
#             Ship.purchase_cargo(shipSymbol, cargoSymbol, units)
#             print(f'Purchased {units} units of {cargoSymbol} for ship {shipSymbol}.')
#         except ValueError as e:
#             print(f'Error purchasing cargo: {e}')
#
#
#     def extract_resources(shipSymbol: str):
#         print(f'Extracting resources for ship {shipSymbol}...')
#         try:
#             extract = Ship.extract(shipSymbol)
#             print(f'Resources extracted for ship {shipSymbol}:')
#             print(f'Cargo Hold: {extract["cargo"]["units"]}/{extract["cargo"]["capacity"]} units')
#             for item in extract['cargo']['inventory']:
#                 print(f'{item["symbol"]}: {item["units"]} units')
#
#             print(f'Ship {shipSymbol} has extracted resources.')
#         except ValueError as e:
#             print(f'Error extracting resources: {e}')
#
#
#     def viewCargo(shipSymbol: str):
#         print(f'Viewing cargo for ship {shipSymbol}...')
#         try:
#             cargo = Ship.get_cargo(shipSymbol)
#             print(f'Cargo for ship {shipSymbol}:')
#             print(f'Cargo Hold: {cargo["units"]}/{cargo["capacity"]} units')
#             for item in cargo['inventory']:
#                 print(f'{item["symbol"]}: {item["units"]} units')
#             
#         except ValueError as e:
#             print(f'Error viewing cargo: {e}')
#
#
#     def deliverCargo(shipSymbol: str):
#         print(f'Delivering cargo for ship {shipSymbol}...')
#         try:
#             contract_id = input('Enter contract ID to deliver cargo for: ')
#             tradeSymbol = input('Enter trade symbol: ').upper()
#             units = int(input('Enter number of units to deliver: '))
#             delivery = Ship.deliver_contract(contract_id, shipSymbol, tradeSymbol, units)
#             print(f'Cargo delivered for ship {shipSymbol}:')
#             print(delivery)
#         except ValueError as e:
#             print(f'Error delivering cargo: {e}')
#     
#
#     def getCooldown(shipSymbol: str):
#         print(f'Getting cooldowns for ship {shipSymbol}...')
#         try:
#             cooldown = Ship.get_cooldown(shipSymbol)
#             print(f'Cooldowns for ship {shipSymbol}:')
#             print(f'Total Cooldown: {cooldown["totalSeconds"]} seconds')
#             print(f'Remaining: {cooldown["remainingSeconds"]} seconds')
#         except ValueError as e:
#             print(f'No Cooldown found for ship {shipSymbol}.')
#         
#
#     print('Printing ships details...')
#     
#     current_ships = Agent.my_ships(active_agent)
#
#     if not current_ships:
#         print(f'No ships found for agent {active_agent.callsign}.')
#         return
#
#     print(f'Ships for {active_agent.callsign}:')
#     for x in range(len(current_ships)):
#         ship = current_ships[x]
#         print(f'#{x} + Ship Name: {ship['symbol']}\tLocation: {ship['nav']['waypointSymbol']}')
#     
#     # choose ship to do something with
#     print('Select a ship by entering its index (0-based):')
#     ship_chosen = int(input('Ship index: '))
#     try:
#         ship_index = ship_chosen
#         if ship_index < 0 or ship_index >= len(current_ships):
#             raise IndexError
#         chosen_ship = current_ships[ship_index]
#        
#     except (IndexError, ValueError):
#         print(f'Invalid ship index: {ship_chosen}. Please enter a valid index.')
#         return
#     
#     print(f'You selected ship: {chosen_ship["symbol"]} at {chosen_ship["nav"]["waypointSymbol"]}')
#     print("What would you like to do with this ship?")
#     print('1. Scan waypoints')
#     print('2. Navigate to a waypoint')
#     print('3. Orbit Ship')
#     print('4. Dock Ship')
#     print('5. Get Status of Ship')
#     print('6. Purchase Cargo')
#     print('7. Extract Resources')
#     print('8. View Cargo')
#     print('9. Deliver Cargo')
#     print('10. Get Cooldown')
#
#     action = input('Enter action number (1-9): ')
#     match action:
#         case '1':
#             print('Available waypoints:')
#             scanWaypoints(chosen_ship['symbol'])
#         case '2':
#             waypoint_symbol = input('Enter waypoint symbol to navigate to: ')
#             navigate(chosen_ship['symbol'], waypoint_symbol.upper())
#             if not waypoint_symbol:
#                 print('No waypoint symbol provided. Aborting navigation.')
#                 return
#         case '3':
#             orbitShip(chosen_ship['symbol'])
#         case '4':
#             dockShip(chosen_ship['symbol'])
#         case '5':
#             getNavStatus(chosen_ship['symbol'])
#         case '6':
#             cargo_symbol = input('Enter cargo symbol to purchase: ')
#             units = input('Enter number of units to purchase: ')
#             purchaseCargo(chosen_ship['symbol'], cargo_symbol, units)
#         case '7':
#             extract_resources(chosen_ship['symbol'])
#         case '8':
#             viewCargo(chosen_ship['symbol'])
#         case '9':
#             deliverCargo(chosen_ship['symbol'])
#         case '10':
#             getCooldown(chosen_ship['symbol'])

def ships(client: SpaceTradersAPIClient):
    print('Fetching ships...')
    agent = Agent(CONFIG.agent_token, {
                        'symbol': 'AGENT_MOJO',
                        'starting_faction': FactionSymbol.COSMIC,
                        'account_id': CONFIG.account_id,
                        'headquarters': 'HQ-001',
                        'credits': 0,
                        'ship_count': 0
                    }
                 )
    ships = Agent.my_ships(self=agent)

    print('Ships:')
    print(ships)
    # for ship in ships:
        # print(f'Ship ID: {ship.symbol}, Location: {ship.nav.waypoint_symbol}')


def run(client: SpaceTradersAPIClient):
    quit = False

    # res = client.call(Agent.get_agent('AGENT_MOJO'))
    # match res:
    #     case SpaceTradersAPIResponse:
    #         agent_data: AgentShape = cast(AgentShape, res.spacetraders.data)
    #         active_agent: Agent = Agent(CONFIG.agent_token, agent_data)
    
    # print(f'Active agent: {active_agent.callsign} ({active_agent.starting_faction})')

    contract_id = 'cmb8cutehk6lxuo6x23gs1gu1'
    while not quit:
        args = list(filter(len, get_next_command()))

        match args[0]:
            # case 'q' | 'quit' | 'e' | 'exit':
            #     quit = True
            # case 'h' | 'help':
            #     usage()
            case 'game':
                from pprint import pp
                pp(SpaceTradersGame().fetch_game_state())
            
            # case 'new' | 'new-agent':
            #     make_new_agent(args)
            # case 'current' | 'agent' | 'me':
            #     get_current_agent()
            # TODO: negotate contract
            case 'contract' | 'contract' | 'c':
                get_contract(contract_id)
            case 'contracts':
                get_contracts()
            # case 'accept' | 'a' | 'accept-contract':
            #     accept_contract(active_agent)
            case 'ships' | 'ship' | 'my-ships' | 's':
                ships(client)
            #     ships(active_agent)
            # case 'contracts' | 'c':
            #     get_contracts(active_agent)

