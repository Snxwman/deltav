from enum import Enum, auto

from deltav.spacetraders.enums import serialize_by_name

@serialize_by_name
class ShipComponent(Enum):
    """

    FRAME
    REACTOR
    ENGINE
    """

    FRAME = auto()
    REACTOR = auto()
    ENGINE = auto()


@serialize_by_name
class ShipConditionEvent(Enum):
    """

    ATMOSPHERIC_ENTRY_HEAT
    BEARING_LUBRICATION_FADE
    COOLANT_LEAK
    COOLANT_SYSTEM_AGEING
    CORROSIVE_MINERAL_CONTAMINATION
    DUST_MICROABRASIONS
    ELECTROMAGNETIC_FIELD_INTERFERENCE
    ELECTROMAGNETIC_SURGE_EFFECTS
    ENERGY_SPIKE_FROM_MINERAL
    EXHAUST_PORT_CLOGGING
    FUEL_EFFICIENCY_DEGRADATION
    HULL_MICROMETEORITE_DAMAGE
    HULL_MICROMETEORITE_STRIKES
    IMPACT_WITH_EXTRACTED_DEBRIS
    MAGNETIC_FIELD_DISRUPTION
    POWER_DISTRIBUTION_FLUCTUATION
    PRESSURE_DIFFERENTIAL_STRESS
    REACTOR_OVERLOAD
    SENSOR_CALIBRATION_DRIFT
    SOLAR_FLARE_INTERFERENCE
    SPACE_DEBRIS_COLLISION
    STRUCTURAL_STRESS_FRACTURES
    THERMAL_EXPANSION_MISMATCH
    THERMAL_STRESS
    THRUSTER_NOZZLE_WEAR
    VIBRATION_DAMAGE_FROM_DRILLING
    VIBRATION_OVERLOAD
    """

    ATMOSPHERIC_ENTRY_HEAT = auto()
    BEARING_LUBRICATION_FADE = auto()
    COOLANT_LEAK = auto()
    COOLANT_SYSTEM_AGEING = auto()
    CORROSIVE_MINERAL_CONTAMINATION = auto()
    DUST_MICROABRASIONS = auto()
    ELECTROMAGNETIC_FIELD_INTERFERENCE = auto()
    ELECTROMAGNETIC_SURGE_EFFECTS = auto()
    ENERGY_SPIKE_FROM_MINERAL = auto()
    EXHAUST_PORT_CLOGGING = auto()
    FUEL_EFFICIENCY_DEGRADATION = auto()
    HULL_MICROMETEORITE_DAMAGE = auto()
    HULL_MICROMETEORITE_STRIKES = auto()
    IMPACT_WITH_EXTRACTED_DEBRIS = auto()
    MAGNETIC_FIELD_DISRUPTION = auto()
    POWER_DISTRIBUTION_FLUCTUATION = auto()
    PRESSURE_DIFFERENTIAL_STRESS = auto()
    REACTOR_OVERLOAD = auto()
    SENSOR_CALIBRATION_DRIFT = auto()
    SOLAR_FLARE_INTERFERENCE = auto()
    SPACE_DEBRIS_COLLISION = auto()
    STRUCTURAL_STRESS_FRACTURES = auto()
    THERMAL_EXPANSION_MISMATCH = auto()
    THERMAL_STRESS = auto()
    THRUSTER_NOZZLE_WEAR = auto()
    VIBRATION_DAMAGE_FROM_DRILLING = auto()
    VIBRATION_OVERLOAD = auto()


@serialize_by_name
class ShipCrewRotationShape(Enum):
    """

    STRICT
    RELAXED
    """

    STRICT = auto()
    RELAXED = auto()


@serialize_by_name
class ShipEngines(Enum):
    """

    ENGINE_HYPER_DRIVE_I
    ENGINE_IMPULSE_DRIVE_I
    ENGINE_ION_DRIVE_I
    ENGINE_ION_DRIVE_II
    """

    ENGINE_HYPER_DRIVE_I = auto()
    ENGINE_IMPULSE_DRIVE_I = auto()
    ENGINE_ION_DRIVE_I = auto()
    ENGINE_ION_DRIVE_II = auto()


@serialize_by_name 
class ShipFrames(Enum):
    """

    FRAME_BULK_FREIGHTER
    FRAME_CARRIER
    FRAME_CRUISER
    FRAME_DESTROYER
    FRAME_DRONE
    FRAME_EXPLORER
    FRAME_FIGHTER
    FRAME_FRIGATE
    FRAME_HEAVY_FREIGHTER
    FRAME_INTERCEPTOR
    FRAME_LIGHT_FREIGHTER
    FRAME_MINER
    FRAME_PROBE
    FRAME_RACER
    FRAME_SHUTTLE
    FRAME_TRANSPORT
    """

    FRAME_BULK_FREIGHTER = auto()
    FRAME_CARRIER = auto()
    FRAME_CRUISER = auto()
    FRAME_DESTROYER = auto()
    FRAME_DRONE = auto()
    FRAME_EXPLORER = auto()
    FRAME_FIGHTER = auto()
    FRAME_FRIGATE = auto()
    FRAME_HEAVY_FREIGHTER = auto()
    FRAME_INTERCEPTOR = auto()
    FRAME_LIGHT_FREIGHTER = auto()
    FRAME_MINER = auto()
    FRAME_PROBE = auto()
    FRAME_RACER = auto()
    FRAME_SHUTTLE = auto()
    FRAME_TRANSPORT = auto()


@serialize_by_name 
class ShipModules(Enum):
    """

    MODULE_CARGO_HOLD_I
    MODULE_CARGO_HOLD_II
    MODULE_CARGO_HOLD_III
    MODULE_CREW_QUARTERS_I
    MODULE_ENVOY_QUARTERS_I
    MODULE_FUEL_REFINERY_I
    MODULE_GAS_PROCESSOR_I
    MODULE_JUMP_DRIVE_I
    MODULE_JUMP_DRIVE_II
    MODULE_JUMP_DRIVE_III
    MODULE_MICRO_REFINERY_I
    MODULE_MINERAL_PROCESSOR_I
    MODULE_ORE_REFINERY_I
    MODULE_PASSENGER_CABIN_I
    MODULE_SCIENCE_LAB_I
    MODULE_SHIELD_GENERATOR_I
    MODULE_SHIELD_GENERATOR_II
    MODULE_WARP_DRIVE_I
    MODULE_WARP_DRIVE_II
    MODULE_WARP_DRIVE_III
    """

    MODULE_CARGO_HOLD_I = auto()
    MODULE_CARGO_HOLD_II = auto()
    MODULE_CARGO_HOLD_III = auto()
    MODULE_CREW_QUARTERS_I = auto()
    MODULE_ENVOY_QUARTERS_I = auto()
    MODULE_FUEL_REFINERY_I = auto()
    MODULE_GAS_PROCESSOR_I = auto()
    MODULE_JUMP_DRIVE_I = auto()
    MODULE_JUMP_DRIVE_II = auto()
    MODULE_JUMP_DRIVE_III = auto()
    MODULE_MICRO_REFINERY_I = auto()
    MODULE_MINERAL_PROCESSOR_I = auto()
    MODULE_ORE_REFINERY_I = auto()
    MODULE_PASSENGER_CABIN_I = auto()
    MODULE_SCIENCE_LAB_I = auto()
    MODULE_SHIELD_GENERATOR_I = auto()
    MODULE_SHIELD_GENERATOR_II = auto()
    MODULE_WARP_DRIVE_I = auto()
    MODULE_WARP_DRIVE_II = auto()
    MODULE_WARP_DRIVE_III = auto()


@serialize_by_name 
class ShipMounts(Enum):
    """

    MOUNT_GAS_SIPHON_I
    MOUNT_GAS_SIPHON_II
    MOUNT_GAS_SIPHON_III
    MOUNT_LASER_CANNON_I
    MOUNT_MINING_LASER_I
    MOUNT_MINING_LASER_II
    MOUNT_MINING_LASER_III
    MOUNT_MISSILE_LAUNCHER_I
    MOUNT_SENSOR_ARRAY_I
    MOUNT_SENSOR_ARRAY_II
    MOUNT_SENSOR_ARRAY_III
    MOUNT_SURVEYOR_I
    MOUNT_SURVEYOR_II
    MOUNT_SURVEYOR_III
    MOUNT_TURRET_I
    """

    MOUNT_GAS_SIPHON_I = auto()
    MOUNT_GAS_SIPHON_II = auto()
    MOUNT_GAS_SIPHON_III = auto()
    MOUNT_LASER_CANNON_I = auto()
    MOUNT_MINING_LASER_I = auto()
    MOUNT_MINING_LASER_II = auto()
    MOUNT_MINING_LASER_III = auto()
    MOUNT_MISSILE_LAUNCHER_I = auto()
    MOUNT_SENSOR_ARRAY_I = auto()
    MOUNT_SENSOR_ARRAY_II = auto()
    MOUNT_SENSOR_ARRAY_III = auto()
    MOUNT_SURVEYOR_I = auto()
    MOUNT_SURVEYOR_II = auto()
    MOUNT_SURVEYOR_III = auto()
    MOUNT_TURRET_I = auto()


@serialize_by_name 
class ShipMountDeposits(Enum):
    """

    ALUMINUM_ORE
    AMMONIA_ICE
    COPPER_ORE
    DIAMONDS
    GOLD_ORE
    ICE_WATER
    IRON_ORE
    MERITIUM_ORE
    PLATINUM_ORE
    PRECIOUS_STONES
    QUARTZ_SAND
    SILICON_CRYSTALS
    SILVER_ORE
    URANITE_ORE
    """

    ALUMINUM_ORE = auto()
    AMMONIA_ICE = auto()
    COPPER_ORE = auto()
    DIAMONDS = auto()
    GOLD_ORE = auto()
    ICE_WATER = auto()
    IRON_ORE = auto()
    MERITIUM_ORE = auto()
    PLATINUM_ORE = auto()
    PRECIOUS_STONES = auto()
    QUARTZ_SAND = auto()
    SILICON_CRYSTALS = auto()
    SILVER_ORE = auto()
    URANITE_ORE = auto()


@serialize_by_name 
class ShipNavFlightMode(Enum):
    """

    BURN
    CRUISE
    DRIFT
    STEALTH
    """

    BURN = auto()
    CRUISE = auto()
    DRIFT = auto()
    STEALTH = auto()


@serialize_by_name 
class ShipNavStatus(Enum):
    """

    DOCKED
    IN_ORBIT
    IN_TRANSIT
    """

    DOCKED = auto()
    IN_ORBIT = auto()
    IN_TRANSIT = auto()


@serialize_by_name 
class ShipReactors(Enum):
    """

    REACTOR_ANTIMATTER_I
    REACTOR_CHEMICAL_I
    REACTOR_FISSION_I
    REACTOR_FUSION_I
    REACTOR_SOLAR_I
    """

    REACTOR_ANTIMATTER_I = auto()
    REACTOR_CHEMICAL_I = auto()
    REACTOR_FISSION_I = auto()
    REACTOR_FUSION_I = auto()
    REACTOR_SOLAR_I = auto()


@serialize_by_name 
class ShipRole(Enum):
    """

    CARRIER
    COMMAND
    EXCAVATOR
    EXPLORER
    FABRICATOR
    HARVESTER
    HAULER
    INTERCEPTOR
    PATROL
    REFINERY
    REPAIR
    SATELLITE
    SURVEYOR
    TRANSPORT
    """

    CARRIER = auto()
    COMMAND = auto()
    EXCAVATOR = auto()
    EXPLORER = auto()
    FABRICATOR = auto()
    HARVESTER = auto()
    HAULER = auto()
    INTERCEPTOR = auto()
    PATROL = auto()
    REFINERY = auto()
    REPAIR = auto()
    SATELLITE = auto()
    SURVEYOR = auto()
    TRANSPORT = auto()


@serialize_by_name 
class ShipType(Enum):
    """

    SHIP_BULK_FREIGHTER
    SHIP_COMMAND_FRIGATE
    SHIP_EXPLORER
    SHIP_HEAVY_FREIGHTER
    SHIP_INTERCEPTOR
    SHIP_LIGHT_HAULER
    SHIP_LIGHT_SHUTTLE
    SHIP_MINING_DRONE
    SHIP_ORE_HOUND
    SHIP_PROBE
    SHIP_REFINING_FREIGHTER
    SHIP_SIPHON_DRONE
    SHIP_SURVEYOR
    """

    SHIP_BULK_FREIGHTER = auto()
    SHIP_COMMAND_FRIGATE = auto()
    SHIP_EXPLORER = auto()
    SHIP_HEAVY_FREIGHTER = auto()
    SHIP_INTERCEPTOR = auto()
    SHIP_LIGHT_HAULER = auto()
    SHIP_LIGHT_SHUTTLE = auto()
    SHIP_MINING_DRONE = auto()
    SHIP_ORE_HOUND = auto()
    SHIP_PROBE = auto()
    SHIP_REFINING_FREIGHTER = auto()
    SHIP_SIPHON_DRONE = auto()
    SHIP_SURVEYOR = auto()
