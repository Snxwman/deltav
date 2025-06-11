from __future__ import annotations

from datetime import datetime, timedelta
from typing import cast

from deltav.config.config import Config
from deltav.spacetraders.agent import Agent
from deltav.spacetraders.api.error import SpaceTradersAPIError
from deltav.spacetraders.contract import Contract
from deltav.spacetraders.enums.error import SpaceTradersAPIErrorCodes
from deltav.spacetraders.game import GAME
from deltav.spacetraders.models import NoDataResShape
from deltav.spacetraders.models.agent import AgentShape
from deltav.spacetraders.models.contract import ContractDeliverReqShape
from deltav.spacetraders.models.market import MarketShape
from deltav.spacetraders.models.ship import (
    CargoItemReqShape,
    ShipCargoInventoryShape,
    ShipCooldownShape,
    ShipEventShape,
    ShipFuelShape,
    ShipNavShape,
    ShipPurchaseReqShape,
    ShipRefuelReqShape,
)
from deltav.spacetraders.models.waypoint import WaypointShape, WaypointSymbolReqShape
from deltav.spacetraders.ship import Ship
from deltav.spacetraders.system import System

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
def usage():
    print('quit, contract, contracts, game, ships, help')


def accept_contract():
    print('Accepting contract...')
    # TODO: remove this placeholder
    temp_contract_id = 'cmb8cutehk6lxuo6x23gs1gu1'
    print(f'Available contract ID: {temp_contract_id}')
    contract_id = input('Enter contract ID to accept: ')

    contract = Contract._accept(contract_id)

    if isinstance(contract, SpaceTradersAPIError):
        print('You have already accepted the contract.')
    else:
        print(f'Contract {contract_id} accepted successfully.')

def get_contracts():
    # TODO: likely unneeded, as the game only allows for one contract at a time
    print('Getting contracts for active agent...')
    contracts = Contract.fetch_contracts()

    if not contracts:
        print('No contracts found.')
        return
    print('Available contracts:')
    print(contracts)


def get_contract(contract_id: str):
    print('Getting contracts for active agent...')
    contract = Contract.fetch_contract(contract_id)
    if not contract:
        print('No contracts found.')
        return
    print(f'Contract {contract_id} details:')
    print(contract)

def transit_time(departure_time_str: datetime, arrival_time_str: datetime) -> list[float]:
    departure_time: datetime = datetime.fromisoformat(str(departure_time_str))
    arrival_time: datetime = datetime.fromisoformat(str(arrival_time_str))
    time_difference: timedelta = arrival_time - departure_time
    total_seconds = time_difference.total_seconds()
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return [hours, minutes, seconds]

def cli_ships(active_agent: AgentShape | None):
    if active_agent is None:
        print('No active agent set. Please set an active agent first.')
        return
    
    def navigate(ship_symbol: str, waypoint: WaypointSymbolReqShape):
        waypoint_symbol = waypoint.waypoint_symbol
        print(f'Navigating ship {ship_symbol} to waypoint {waypoint_symbol}...')
        res = Ship.navigate(ship_symbol, waypoint)
        if isinstance(res, SpaceTradersAPIError):
            print(f'Error navigating ship {ship_symbol} to waypoint {waypoint_symbol}: {res}')
            return
        navigation_data: ShipNavShape = res.nav
        fuel: ShipFuelShape = res.fuel
        if hasattr(res, 'event'):
            event: ShipEventShape | None = res.event
            if event and isinstance(event, dict) and "message" in event:
                print(f'Event during navigation: {event["message"]}')

        print(f'Ship {ship_symbol} is now navigating to waypoint {waypoint_symbol}.')
        print(f'Fuel remaining: {fuel.current}/{fuel.capacity} units')
        print(f'Fuel consumed on this trip: {fuel.consumed} units')


    def scanWaypoints(ship_symbol: str):
        print(f'Scanning waypoints for ship {ship_symbol}...')

        data = Ship.scan_waypoints(ship_symbol)
        if isinstance(data, SpaceTradersAPIError):
            print(f'Error scanning waypoints: {data.code.value} - {data.message}')
            return
        
        cooldown: ShipCooldownShape = cast(ShipCooldownShape, data.cooldown)
        print(cooldown)
        waypoints: list[WaypointShape] = cast(list[WaypointShape], data.waypoints)
        print(f'Waypoints for ship {ship_symbol}:')
        if isinstance(waypoints, list):
            for waypoint in waypoints:
                faction = getattr(waypoint, 'faction', None)
                print(f'Location: {waypoint.symbol} ({waypoint.type}) at ({waypoint.x}, {waypoint.y})')
                print(f'Faction: {faction}')
                
                traits = getattr(waypoint, 'traits', [])
                for trait in traits:
                    print(f'Trait: {trait["symbol"]} - {trait["name"]}')
                print()
        else:
            print(waypoints)
            print('Error: Waypoints data is not in the expected format.')


    def getNavStatus(ship_symbol: str):
        print(f'Getting navigation status for ship {ship_symbol}...')
        status = Ship.fetch_nav_status(ship_symbol)
        if isinstance(status, SpaceTradersAPIError):
            print(f'No navigation status found for ship {ship_symbol}. Error: {status.message}')
            return
        print(f'Navigation status for ship {ship_symbol}:')
        if (status.status =='IN_TRANSIT'):
            departure_time_str = status.route.departure_time
            arrival_time_str = status.route.arrival
            hours, minutes, seconds = transit_time(departure_time_str, arrival_time_str)
            print(f'Ship {ship_symbol} is currently in transit.')
            print(f'Origin: {status.route.origin.symbol}')
            print(f'Destination: {status.route.destination.symbol}')
            print(f"Arriving to destination in: {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds")
        else:
            print(f'Location: {status.waypoint_symbol}\tStatus: {status.status}\tFlight Mode: {status.flight_mode}')


    def orbitShip(ship_symbol: str):
        print(f'Orbiting ship {ship_symbol}...')
        try:
            Ship.orbit_ship(ship_symbol)
            print(f'Ship {ship_symbol} is now orbiting.')
        except ValueError as e:
            print(f'Error orbiting ship: {e}')
    

    def dockShip(ship_symbol: str):
        print(f'Docking ship {ship_symbol}...')
        try:
            Ship.dock_ship(ship_symbol)
            print(f'Ship {ship_symbol} is now docked.')
        except ValueError as e:
            print(f'Error docking ship: {e}')


    def purchaseCargo(ship_symbol: str):
        cargo_symbol = input('Enter cargo symbol to purchase: ')
        units = int(input('Enter number of units to purchase: '))
        print(f'Purchasing {units} units of {cargo_symbol} for ship {ship_symbol}...')
        try:
            
            purchase = cast(CargoItemReqShape, {
                'symbol': cargo_symbol,
                'units': units,
            })
            Ship.purchase_cargo(ship_symbol, purchase)
            print(f'Purchased {units} units of {cargo_symbol} for ship {ship_symbol}.')
        except ValueError as e:
            print(f'Error purchasing cargo: {e}')


    def sellCargo(ship_symbol: str, trade_symbol: str, units: int):
        print(f'Selling {units} units of {trade_symbol} for ship {ship_symbol}...')
        try:
            sell = cast(CargoItemReqShape, {
                'symbol': trade_symbol,
                'units': units,
            })
            data = Ship.sell_cargo(ship_symbol, sell)
            if isinstance(data, SpaceTradersAPIError):

                print(f'Error selling cargo: {data.message}')
                return
            print(f'Successfully sold {units} units of {trade_symbol} for ship {ship_symbol}.')
        except ValueError as e:
            print(f'Error selling cargo: {e}')


    def viewCargo(ship_symbol: str):
        print(f'Viewing cargo for ship {ship_symbol}...')
        cargo = Ship.fetch_cargo(ship_symbol)
        if isinstance(cargo, SpaceTradersAPIError):
            print(f'Error getting cargo for ship {ship_symbol}: {cargo}')
            return
        print(f'Cargo for ship {ship_symbol}:')
        print(f'Cargo Hold: {cargo.units}/{cargo.capacity} units')
        inventory_data = cargo.inventory
        if isinstance(inventory_data, list):
            inventory: ShipCargoInventoryShape = cast(ShipCargoInventoryShape, inventory_data)
            for item in inventory:
                item_casted = cast(CargoItemReqShape, item)
                print(f'{item_casted.symbol}: {item_casted.units} units')
        else:
            print("Error: Inventory data is not in the expected format.")
            

    def deliverCargo(ship_symbol: str):
        print(f'Delivering cargo for ship {ship_symbol}...')
        try:
            contract_id = input('Enter contract ID to deliver cargo for: ')
            trade_symbol = input('Enter trade symbol: ').upper()
            units = int(input('Enter number of units to deliver: '))
            deliver = cast(ContractDeliverReqShape, {
                'ship_symbol': ship_symbol,
                'trade_symbol': trade_symbol,
                'units': units
            })
            delivery = Contract._fulfill(contract_id, deliver)
            print(f'Cargo delivered for ship {ship_symbol}:')
            print(delivery)
        except ValueError as e:
            print(f'Error delivering cargo: {e}')
    
    
    def extract_resources(ship_symbol: str):
        print(f'Extracting resources for ship {ship_symbol}...')
        extract = Ship.extract(ship_symbol)
        if isinstance(extract, SpaceTradersAPIError):
            print(f'Error extracting resources for ship {ship_symbol}: {extract}')
            return
        
        print(f'Resources extracted for ship {ship_symbol}:')
        print(f'Cargo Hold: {extract.cargo.units}/{extract.cargo.capacity} units')
        for item in extract.cargo.inventory:
            item_casted = cast(CargoItemReqShape, item)
            print(f'{item_casted.symbol}: {item_casted.units} units')
        print(f'Ship on cooldown for {extract.cooldown.remaining_seconds} seconds.')
        print(f'Ship {ship_symbol} has finished extracting resources.')


    def getCooldown(ship_symbol: str):
        print(f'Getting cooldowns for ship {ship_symbol}...')
        cooldown = Ship.fetch_cooldown(ship_symbol)
        if isinstance(cooldown, SpaceTradersAPIError):
            print(f'Error getting cooldown for ship {ship_symbol}: {cooldown}')
            print(f'Error code: {cooldown.code}')
            print('Probably means no cooldown?')
            return
        elif isinstance(cooldown, NoDataResShape):
            print(f'No cooldown data available for ship {ship_symbol}.')
            return
        
        print(f'Cooldowns for ship {ship_symbol}:')
        print(f'Total Cooldown: {cooldown.total_seconds} seconds')
        print(f'Remaining: {cooldown.remaining_seconds} seconds')


    def jettisonCargo(ship_symbol: str, cargo_symbol: str, units):
        print(f'Jettisoning {units} units of {cargo_symbol} from ship {ship_symbol}...')
        try:
            jettison = cast(CargoItemReqShape, {
                'symbol': cargo_symbol,
                'units': units,
            })
            cargo_jettisoned = Ship.jettison_cargo(ship_symbol, jettison)
            if isinstance(cargo_jettisoned, SpaceTradersAPIError):
                print(f'Error jettisoning cargo: {cargo_jettisoned}')
                return
            print(f'Jettisoned {units} units of {cargo_symbol} from ship {ship_symbol}.')
        except ValueError as e:
            print(f'Error jettisoning cargo: {e}')

    
    def purchase_ship(waypoint_symbol: str):
        shipyard = System.get_shipyard(waypoint_symbol)

            
        if isinstance(shipyard, SpaceTradersAPIError):
            print(f'Error getting shipyard at waypoint {waypoint_symbol}: {shipyard}')
            print(f'Error: {shipyard.code.value} - {shipyard.message}')
            return
        print(f'Available ships for purchase at waypoint {waypoint_symbol}:')
        if not isinstance(shipyard, dict) or 'ships' not in shipyard or not shipyard['ships']:
            print('No ships available for purchase at this waypoint.')
            return
        transactions = shipyard['transactions']

        ship_prices = {}
        count = 0
        for transaction in transactions:
            agent_symbol = transaction['agent_symbol']
            if agent_symbol == active_agent.symbol:
                continue
            ship_type = transaction['ship_type']
            price = transaction['price']
            ship_prices[ship_type] = price
            print(f"# - {count}Ship Type: {ship_type} - Price: {price} credits")
            count += 1

        ship_type = input('Enter ship type to purchase (e.g. EXPLORER, FIGHTER, etc.): ').upper()
        print(f'Purchasing ship of type {ship_type} at waypoint {waypoint_symbol}...')
        shape = cast(ShipPurchaseReqShape, {
            'ship_type': ship_type,
            'waypoint_symbol': waypoint_symbol
        })
        res = Ship.purchase_ship(shape)
        if isinstance(res, SpaceTradersAPIError):
            print(f'Error purchasing ship: Error Code: {res.code.value} - {res.message}')
            if res.code == SpaceTradersAPIErrorCodes.PURCHASE_SHIP_CREDITS_ERROR:
                print('You do not have enough credits to purchase this ship.')
            elif res.code == SpaceTradersAPIErrorCodes.SHIP_NOT_AVAILABLE_FOR_PURCHASE_ERROR:
                print('Ship not available for purchase at this waypoint.')
            else:
                print('An unexpected error occurred while purchasing the ship.')
            return
        ship = res.ship
        agent = res.agent
        transaction = res.transaction

        print(f'Ship purchased successfully: {ship.symbol} for {transaction.price} credits.')


    def refuel_ship(ship_symbol: str):
        # one unit of fuel from marketplace/cargo = 100 fuel units TODO: verify?
        print(f'Refueling ship {ship_symbol}...')
        refuel = cast(ShipRefuelReqShape, {
            'units': 0,  
            'from_cargo': True 
        })

        # if not at marketplace with fuel, check if ship cargo has fuel, if so use it
        req = Ship.fetch_ship(ship_symbol)
        if isinstance(req, SpaceTradersAPIError):
            print(f'Error getting ship during refueling {ship_symbol}: {req.code.value} - {req.message}')
            return
        cargo = req.cargo
        fuel = None
        for item in cargo.inventory:
            if item.symbol == 'FUEL':
                fuel = item
                break
        # need to check if ship is docked in a waypoint with a marketplace that sells fuel
        waypoint_symbol = req.nav.waypoint_symbol
        
        market_request = System.get_market(waypoint_symbol)

        market: MarketShape | None = None

            
        if isinstance(market, SpaceTradersAPIError):
            print(f'Possibly just not docked at a waypoint with a market, or no market at waypoint {waypoint_symbol}.')
            print(f'Error getting market at waypoint during refueling {waypoint_symbol}: {market.code.value} - {market.message}')
            return
        
        if market:
            print('Market found, refueling from market')
            refuel['from_cargo'] = False
        
        print(f'Current Fuel: {req.fuel.consumed}/{req.fuel.capacity} units')
        refuel_amount = input('Enter amount of fuel to refuel (negative to fill): ')
        try:
            refuel_amount = int(refuel_amount)
            if refuel_amount < 0:
                refuel.units = req.fuel.capacity - req.fuel.current
            else:
                refuel.units = refuel_amount
            if refuel.units > req.fuel.capacity - req.fuel.current:
                print(f'Cannot refuel more than the remaining capacity: {req.fuel.capacity - req.fuel.current} units')
                return
        except ValueError as e:
            print(f'Invalid fuel amount: {e}')
            return
        

        res = Ship.refuel_ship(ship_symbol, refuel)
        if isinstance(res, SpaceTradersAPIError):
            print(f'Error refueling ship {ship_symbol}: {res.code.value} {res.message}')
            return
        agent = res.agent
        fuel = res.fuel
        # cargo = res['cargo']
        transaction = res.transaction

        print(f'Ship {ship_symbol} refueled successfully.')
        print(f'Fuel: {fuel.current}/{fuel.capacity} units')
        print(f'Spent {transaction.total_price} credits on refueling.')
        

    print('Printing ships details...')
    current_ships = []
    if active_agent is not None:
        agent_instance = Agent(CONFIG.agent_token, active_agent)

    current_ships = Ship.fetch_ships()
    if isinstance(current_ships, SpaceTradersAPIError):
        print(f'Error retrieving ships: {current_ships.message}')
        return

    if not current_ships:
        if active_agent is not None:
            print(f'No ships found for agent {active_agent.symbol}.')
        else:
            print('No ships found because no active agent is set.')
        
    if isinstance(current_ships, list):
        for x in range(len(current_ships)):
            ship = current_ships[x]
            if ship['nav']['status'] == 'IN_ORBIT':
                status: str = 'IN_ORBIT  '
            elif ship['nav']['status'] == 'IN_TRANSIT':
                status: str = 'IN_TRANSIT'
            elif ship['nav']['status'] == 'DOCKED':
                status: str = 'DOCKED    '
            else:
                status: str = 'UNKNOWN   '
            print(f'#{x} + Ship Name: {ship['symbol']}\tLocation: {ship['nav']['waypoint_symbol']}\tType: {ship['registration']['role']}\tStatus: {status}\tFuel: {ship['fuel']['current']}/{ship['fuel']['capacity']}\tCargo: {ship['cargo']['units']}/{ship['cargo']['capacity']} units')
    elif isinstance(current_ships, SpaceTradersAPIError):
        print(f'Error retrieving ships: {current_ships}')
        return
    else:
        print("Unexpected error: current_ships is not a list.")
        return
    
    print('Select a ship by entering its index (0-based):')
    ship_chosen = input('Ship index: ')
    try:
        ship_index = int(ship_chosen)
        if ship_index < 0 or ship_index >= len(current_ships):
            raise IndexError
        chosen_ship = current_ships[ship_index]
    
    except (IndexError, ValueError):
        print(f'Invalid ship index: {ship_chosen}. Please enter a valid index.')
        return
    
    def functions_on_orbit(ship_symbol: str):
        print('1. Get Navigation Status')
        print('1. Get Cooldown')
        print('3. Dock Ship')
        print('4. Scan waypoints')
        print('5. Navigate to a waypoint')
        print('6. Extract Resources')
        print('7. View Cargo')

        action = input('Enter action number (1-9): ')
        match action:
            case '1':
                getNavStatus(ship_symbol)
            case '2':
                getCooldown(ship_symbol)
            case '3':
                dockShip(ship_symbol)
            case '4':
                print('Available waypoints:')
                scanWaypoints(ship_symbol)
            case '5':
                waypoint_symbol = input('Enter waypoint symbol to navigate to: ').upper()
                waypoint: WaypointSymbolReqShape = WaypointSymbolReqShape(waypoint_symbol=waypoint_symbol)
                navigate(ship_symbol, waypoint)
                if not waypoint_symbol:
                    print('No waypoint symbol provided. Aborting navigation.')
                    return
            case '6':
                extract_resources(ship_symbol)
            case '7':
                viewCargo(ship_symbol)
                
        
    def functions_while_docked(ship_symbol: str):
        print('1. Get Navigation Status')
        print('1. Get Cooldown')
        print('3. Orbit Ship')
        print('4. View Cargo')
        print('5. Purchase Cargo')
        print('6. Sell Cargo')
        print('7. Deliver Cargo')
        print('8. Jettison Cargo')
        print('9. Purchase Ship')
        print('10. Refuel Ship')

        action = input('Enter action number (1-9): ')
        match action:
            case '1':
                getNavStatus(ship_symbol)
            case '2':
                getCooldown(ship_symbol)
            case '3':
                orbitShip(ship_symbol)
            case '4':
                viewCargo(ship_symbol)
            case '5':
                viewCargo(ship_symbol)
                purchaseCargo(ship_symbol)
            case '6':
                viewCargo(ship_symbol)
                cargo_symbol = input('Enter cargo symbol to sell: ')
                units = int(input('Enter number of units to sell: '))
                sellCargo(ship_symbol, cargo_symbol, units)
            case '7':
                # TODO: is this while docked or in orbit?
                deliverCargo(ship_symbol)
            case '8':
                viewCargo(ship_symbol)
                cargo_symbol = input('Enter cargo symbol to jettison: ')
                units = int(input('Enter number of units to jettison: '))
                jettisonCargo(ship_symbol, cargo_symbol, units)
            case '9':
                purchase_ship(waypoint_symbol=chosen_ship['nav']['waypoint_symbol'])
            case '10':
                refuel_ship(ship_symbol)

    def functions_in_transit(ship_symbol: str):
        print('1. Get Navigation Status')
        print('1. Get Cooldown')

        action = input('Enter action number (1-9): ')
        match action:
            case '1':
                getNavStatus(ship_symbol)
            case '2':
                getCooldown(ship_symbol)


    nav_status = chosen_ship['nav']['status']
    print(f'You selected ship: {chosen_ship["symbol"]} at {chosen_ship["nav"]["waypoint_symbol"]}')
    print("What would you like to do with this ship?")
    if nav_status == 'DOCKED':
        functions_while_docked(chosen_ship['symbol'])
    elif nav_status == 'IN_ORBIT':
        functions_on_orbit(chosen_ship['symbol'])
    elif nav_status == 'IN_TRANSIT':
        functions_in_transit(chosen_ship['symbol'])


def run():
    quit = False
    # contract_id = 'cmb8cutehk6lxuo6x23gs1gu1'
    # active_agent = cast(AgentShape, {
    #     'symbol': 'AGENT_MOJO',
    #     'starting_faction': FactionSymbol.COSMIC,
    #     'headquarters': 'HQ',
    #     'credits': 1000,
    #     'ship_count': 1,
    #     'account_id': None
    # })

    config = Config()
    agent_config = config.get_agent('snxwman', 'snxw')
    my_agent = Agent(agent_config.token)

    while not quit:
        args = list(filter(len, get_next_command()))

        match args[0]:
            case 'q' | 'quit' | 'e' | 'exit':
                quit = True
            case 'h' | 'help':
                usage()
            case 'game':
                print(GAME.server_status)
            case 'agents':
                GAME.update_agents()
                for agent in GAME.agents:
                    if agent.ship_count != 2:
                        print(agent)
            # case 'new' | 'new-agent':
            #     make_new_agent(args)
            # case 'current' | 'agent' | 'me':
            #     get_current_agent()
            # TODO: negotate contract
            case 'contract' | 'contract' | 'c':
                pass
            case 'contracts':
                contracts = my_agent.past_contracts
                print(contracts)
            case 'accept' | 'a' | 'accept-contract':
                accept_contract()
            case 'ships' | 'ship' | 'my-ships' | 's':
                my_ships = my_agent.ships
                for ship in my_ships:
                    print(ship)
            case 'config':
                print(config)
            case 'faction':
                print(my_agent.faction.symbol)
