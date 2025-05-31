from enum import Enum, auto


class ShipComponent(Enum):
    FRAME = auto()
    REACTOR = auto()
    ENGINE = auto()


class ShipConditionEvent(Enum):
    REACTOR_OVERLOAD = auto()
    ENERGY_SPIKE_FROM_MINERAL = auto()
    SOLAR_FLARE_INTERFERENCE = auto()
    COOLANT_LEAK = auto()
    POWER_DISTRIBUTION_FLUCTUATION = auto()
    MAGNETIC_FIELD_DISRUPTION = auto()
    HULL_MICROMETEORITE_STRIKES = auto()
    STRUCTURAL_STRESS_FRACTURES = auto()
    CORROSIVE_MINERAL_CONTAMINATION = auto()
    THERMAL_EXPANSION_MISMATCH = auto()
    VIBRATION_DAMAGE_FROM_DRILLING = auto()
    ELECTROMAGNETIC_FIELD_INTERFERENCE = auto()
    IMPACT_WITH_EXTRACTED_DEBRIS = auto()
    FUEL_EFFICIENCY_DEGRADATION = auto()
    COOLANT_SYSTEM_AGEING = auto()
    DUST_MICROABRASIONS = auto()
    THRUSTER_NOZZLE_WEAR = auto()
    EXHAUST_PORT_CLOGGING = auto()
    BEARING_LUBRICATION_FADE = auto()
    SENSOR_CALIBRATION_DRIFT = auto()
    HULL_MICROMETEORITE_DAMAGE = auto()
    SPACE_DEBRIS_COLLISION = auto()
    THERMAL_STRESS = auto()
    VIBRATION_OVERLOAD = auto()
    PRESSURE_DIFFERENTIAL_STRESS = auto()
    ELECTROMAGNETIC_SURGE_EFFECTS = auto()
    ATMOSPHERIC_ENTRY_HEAT = auto()


class ShipCrewRotation(Enum):
    STRICT = auto()
    RELAXED = auto()


class ShipEngines(Enum):
    ENGINE_IMPULSE_DRIVE_I = auto()
    ENGINE_ION_DRIVE_I = auto()
    ENGINE_ION_DRIVE_II = auto()
    ENGINE_HYPER_DRIVE_I = auto()


class ShipFrames(Enum):
    FRAME_PROBE = auto()
    FRAME_DRONE = auto()
    FRAME_INTERCEPTOR = auto()
    FRAME_RACER = auto()
    FRAME_FIGHTER = auto()
    FRAME_FRIGATE = auto()
    FRAME_SHUTTLE = auto()
    FRAME_EXPLORER = auto()
    FRAME_MINER = auto()
    FRAME_LIGHT_FREIGHTER = auto()
    FRAME_HEAVY_FREIGHTER = auto()
    FRAME_TRANSPORT = auto()
    FRAME_DESTROYER = auto()
    FRAME_CRUISER = auto()
    FRAME_CARRIER = auto()
    FRAME_BULK_FREIGHTER = auto()


class ShipModules(Enum):
    MODULE_MINERAL_PROCESSOR_I = auto()
    MODULE_GAS_PROCESSOR_I = auto()
    MODULE_CARGO_HOLD_I = auto()
    MODULE_CARGO_HOLD_II = auto()
    MODULE_CARGO_HOLD_III = auto()
    MODULE_CREW_QUARTERS_I = auto()
    MODULE_ENVOY_QUARTERS_I = auto()
    MODULE_PASSENGER_CABIN_I = auto()
    MODULE_MICRO_REFINERY_I = auto()
    MODULE_ORE_REFINERY_I = auto()
    MODULE_FUEL_REFINERY_I = auto()
    MODULE_SCIENCE_LAB_I = auto()
    MODULE_JUMP_DRIVE_I = auto()
    MODULE_JUMP_DRIVE_II = auto()
    MODULE_JUMP_DRIVE_III = auto()
    MODULE_WARP_DRIVE_I = auto()
    MODULE_WARP_DRIVE_II = auto()
    MODULE_WARP_DRIVE_III = auto()
    MODULE_SHIELD_GENERATOR_I = auto()
    MODULE_SHIELD_GENERATOR_II = auto()


class ShipMounts(Enum):
    MOUNT_GAS_SIPHON_I = auto()
    MOUNT_GAS_SIPHON_II = auto()
    MOUNT_GAS_SIPHON_III = auto()
    MOUNT_SURVEYOR_I = auto()
    MOUNT_SURVEYOR_II = auto()
    MOUNT_SURVEYOR_III = auto()
    MOUNT_SENSOR_ARRAY_I = auto()
    MOUNT_SENSOR_ARRAY_II = auto()
    MOUNT_SENSOR_ARRAY_III = auto()
    MOUNT_MINING_LASER_I = auto()
    MOUNT_MINING_LASER_II = auto()
    MOUNT_MINING_LASER_III = auto()
    MOUNT_LASER_CANNON_I = auto()
    MOUNT_MISSILE_LAUNCHER_I = auto()
    MOUNT_TURRET_I = auto()


class ShipMountDeposits(Enum):
    QUARTZ_SAND = auto()
    SILICON_CRYSTALS = auto()
    PRECIOUS_STONES = auto()
    ICE_WATER = auto()
    AMMONIA_ICE = auto()
    IRON_ORE = auto()
    COPPER_ORE = auto()
    SILVER_ORE = auto()
    ALUMINUM_ORE = auto()
    GOLD_ORE = auto()
    PLATINUM_ORE = auto()
    DIAMONDS = auto()
    URANITE_ORE = auto()
    MERITIUM_ORE = auto()


class ShipNavFlightMode(Enum):
    DRIFT = auto()
    STEALTH = auto()
    CRUISE = auto()
    BURN = auto()


class ShipNavStatus(Enum):
    IN_TRANSIT = auto()
    IN_ORBIT = auto()
    DOCKED = auto()


class ShipReactors(Enum):
    REACTOR_SOLAR_I = auto()
    REACTOR_FUSION_I = auto()
    REACTOR_FISSION_I = auto()
    REACTOR_CHEMICAL_I = auto()
    REACTOR_ANTIMATTER_I = auto()


class ShipRole(Enum):
    FABRICATOR = auto()
    HARVESTER = auto()
    HAULER = auto()
    INTERCEPTOR = auto()
    EXCAVATOR = auto()
    TRANSPORT = auto()
    REPAIR = auto()
    SURVEYOR = auto()
    COMMAND = auto()
    CARRIER = auto()
    PATROL = auto()
    SATELLITE = auto()
    EXPLORER = auto()
    REFINERY = auto()


class ShipType(Enum):
    SHIP_PROBE = auto()
    SHIP_MINING_DRONE = auto()
    SHIP_SIPHON_DRONE = auto()
    SHIP_INTERCEPTOR = auto()
    SHIP_LIGHT_HAULER = auto()
    SHIP_COMMAND_FRIGATE = auto()
    SHIP_EXPLORER = auto()
    SHIP_HEAVY_FREIGHTER = auto()
    SHIP_LIGHT_SHUTTLE = auto()
    SHIP_ORE_HOUND = auto()
    SHIP_REFINING_FREIGHTER = auto()
    SHIP_SURVEYOR = auto()
    SHIP_BULK_FREIGHTER = auto()

