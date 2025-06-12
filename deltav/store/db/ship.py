from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from deltav.store.db import Base
from deltav.store.db.agent import AgentRecord


class ShipCargoRecord(Base):
    __tablename__: str = 'ship_cargo'

    id: Mapped[int] = mapped_column(primary_key=True)
    units: Mapped[int] = mapped_column()

    ship_id: Mapped[str] = mapped_column(ForeignKey('ships.id'))

    ship: Mapped['ShipRecord'] = relationship(back_populates='cargo')
    # needs relationship to the trade good this is
    # trade_good: Mapped[list] = relationship()


class ShipEngineTypeRecord(Base):
    __tablename__: str = 'ship_engine_types'

    id: Mapped[int] = mapped_column(primary_key=True)
    crew: Mapped[int | None] = mapped_column()
    description: Mapped[str] = mapped_column()
    module_slots: Mapped[int] = mapped_column()
    name: Mapped[str] = mapped_column()
    power: Mapped[int | None] = mapped_column()
    slots: Mapped[int | None] = mapped_column()
    speed: Mapped[int] = mapped_column()
    symbol: Mapped[str] = mapped_column()


class ShipEngineRecord(Base):
    __tablename__: str = 'ship_engines'

    id: Mapped[int] = mapped_column(primary_key=True)
    condition: Mapped[int] = mapped_column()
    integrity: Mapped[int] = mapped_column()
    quality: Mapped[int] = mapped_column()

    engine_type_id: Mapped[int] = mapped_column(ForeignKey('ship_engine_types.id'))
    ship_id: Mapped[int] = mapped_column(ForeignKey('ships.id'))

    engine_type: Mapped[ShipEngineTypeRecord] = relationship()
    ship: Mapped['ShipRecord'] = relationship(back_populates='engine')


class ShipFrameTypeRecord(Base):
    __tablename__: str = 'ship_frame_types'

    id: Mapped[int] = mapped_column(primary_key=True)
    crew: Mapped[int | None] = mapped_column()
    description: Mapped[str] = mapped_column()
    fuel_capacity: Mapped[int] = mapped_column()
    module_slots: Mapped[int] = mapped_column()
    mounting_points: Mapped[int] = mapped_column()
    name: Mapped[str] = mapped_column()
    power: Mapped[int | None] = mapped_column()
    slots: Mapped[int | None] = mapped_column()
    symbol: Mapped[str] = mapped_column()


class ShipFrameRecord(Base):
    __tablename__: str = 'ship_frames'

    id: Mapped[int] = mapped_column(primary_key=True)
    condition: Mapped[int] = mapped_column()
    integrity: Mapped[int] = mapped_column()
    quality: Mapped[int] = mapped_column()

    frame_type_id: Mapped[int] = mapped_column(ForeignKey('ship_frame_types.id'))
    ship_id: Mapped[int] = mapped_column(ForeignKey('ships.id'))

    frame_type: Mapped[ShipFrameTypeRecord] = relationship()
    ship: Mapped['ShipRecord'] = relationship(back_populates='frame')


class FuelConsumedRecord(Base):
    __tablename__: str = 'ship_fuel_consumed'

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[int] = mapped_column()
    timestamp: Mapped[datetime] = mapped_column()

    ship_id: Mapped[int] = mapped_column(ForeignKey('ships.id'))

    ship: Mapped['ShipRecord'] = relationship(back_populates='fuel_consumed')


class ShipModuleTypesRecord(Base):
    __tablename__: str = 'ship_module_types'

    id: Mapped[int] = mapped_column(primary_key=True)
    capacity: Mapped[int] = mapped_column()
    crew: Mapped[int | None] = mapped_column()
    description: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
    power: Mapped[int | None] = mapped_column()
    range: Mapped[int] = mapped_column()
    slots: Mapped[int | None] = mapped_column()
    symbol: Mapped[str] = mapped_column()


class ShipModuleRecord(Base):
    __tablename__: str = 'ship_modules'

    id: Mapped[int] = mapped_column(primary_key=True)

    module_type_id: Mapped[int] = mapped_column(ForeignKey('ship_module_types.id'))
    ship_id: Mapped[int] = mapped_column(ForeignKey('ships.id'))

    ship: Mapped['ShipRecord'] = relationship(back_populates='modules')


class ShipMountTypesRecord(Base):
    __tablename__: str = 'ship_mount_types'

    id: Mapped[int] = mapped_column(primary_key=True)
    crew: Mapped[int | None] = mapped_column()
    description: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
    power: Mapped[int | None] = mapped_column()
    range: Mapped[int] = mapped_column()
    slots: Mapped[int | None] = mapped_column()
    strength: Mapped[int] = mapped_column()
    symbol: Mapped[str] = mapped_column()
    # deposits


class ShipMountRecord(Base):
    __tablename__: str = 'ship_mounts'

    id: Mapped[int] = mapped_column(primary_key=True)

    mount_type_id: Mapped[int] = mapped_column(ForeignKey('ship_mount_types.id'))
    ship_id: Mapped[int] = mapped_column(ForeignKey('ships.id'))

    ship: Mapped['ShipRecord'] = relationship(back_populates='mounts')


class ShipRouteRecord(Base):
    __tablename__: str = 'ship_routes'

    id: Mapped[int] = mapped_column(primary_key=True)
    arrival: Mapped[datetime] = mapped_column()
    departure: Mapped[datetime] = mapped_column()
    destination_system: Mapped[str] = mapped_column()
    destination_type: Mapped[str] = mapped_column()
    destination_waypoint: Mapped[str] = mapped_column()
    destination_x: Mapped[int] = mapped_column()
    destination_y: Mapped[int] = mapped_column()
    origin_system: Mapped[str] = mapped_column()
    origin_type: Mapped[str] = mapped_column()
    origin_waypoint: Mapped[str] = mapped_column()
    origin_x: Mapped[int] = mapped_column()
    origin_y: Mapped[int] = mapped_column()

    ship: Mapped['ShipRecord'] = relationship(back_populates='nav_routes')


class ShipReactorTypeRecord(Base):
    __tablename__: str = 'ship_reactor_types'

    id: Mapped[int] = mapped_column(primary_key=True)
    crew: Mapped[int] = mapped_column()
    description: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
    power: Mapped[int] = mapped_column()
    power_output: Mapped[int] = mapped_column()
    range: Mapped[int] = mapped_column()
    slots: Mapped[int] = mapped_column()
    symbol: Mapped[str] = mapped_column()


class ShipReactorRecord(Base):
    __tablename__: str = 'ship_reactors'

    id: Mapped[int] = mapped_column(primary_key=True)
    condition: Mapped[int] = mapped_column()
    integrity: Mapped[int] = mapped_column()
    quality: Mapped[int] = mapped_column()

    reactor_type_id: Mapped[int] = mapped_column(ForeignKey('ship_reactor_types.id'))
    ship_id: Mapped[int] = mapped_column(ForeignKey('ships.id'))

    ship: Mapped['ShipRecord'] = relationship(back_populates='reactor')


class ShipRecord(Base):
    __tablename__: str = 'ships'

    id: Mapped[int] = mapped_column(primary_key=True)
    cargo_capacity: Mapped[int] = mapped_column()
    # cargo_inventory
    cargo_units: Mapped[int] = mapped_column()
    cooldown_total: Mapped[int] = mapped_column()
    cooldown_remaining: Mapped[int] = mapped_column()
    cooldown_expiration: Mapped[datetime] = mapped_column()
    crew_current: Mapped[int] = mapped_column()
    crew_required: Mapped[int] = mapped_column()
    crew_capacity: Mapped[int] = mapped_column()
    crew_morale: Mapped[int] = mapped_column()
    crew_rotation: Mapped[str] = mapped_column()
    crew_wages: Mapped[int] = mapped_column()
    faction: Mapped[str] = mapped_column()
    fuel_current: Mapped[int] = mapped_column()
    fuel_capacity: Mapped[int] = mapped_column()
    nav_system: Mapped[str] = mapped_column()
    nav_waypoint: Mapped[str] = mapped_column()
    nav_flight_mode: Mapped[str] = mapped_column()
    nav_status: Mapped[str] = mapped_column()
    role: Mapped[str] = mapped_column()
    symbol: Mapped[str] = mapped_column(unique=True)

    agent_id: Mapped[int] = mapped_column(ForeignKey('agents.id'))
    engine_id: Mapped[int] = mapped_column(ForeignKey('ship_engines.id'))
    frame_id: Mapped[int] = mapped_column(ForeignKey('ship_frames.id'))
    reactor_id: Mapped[int] = mapped_column(ForeignKey('ship_reactors.id'))

    agent: Mapped[AgentRecord] = relationship(back_populates='ships')
    cargo: Mapped[list[ShipCargoRecord]] = relationship(back_populates='ship')
    engine: Mapped[ShipEngineRecord] = relationship(back_populates='ship')
    frame: Mapped[ShipFrameRecord] = relationship(back_populates='ship')
    fuel_consumed: Mapped[list[FuelConsumedRecord]] = relationship(back_populates='ship')
    modules: Mapped[list[ShipModuleRecord]] = relationship(back_populates='ship')
    mounts: Mapped[list[ShipMountRecord]] = relationship(back_populates='ship')
    nav_routes: Mapped[list[ShipRouteRecord]] = relationship(back_populates='ship')
    reactor: Mapped[ShipReactorRecord] = relationship(back_populates='ship')
