from dataclasses import dataclass
from datetime import datetime
from typing import NewType


@dataclass
class LegalEntity:
    id: int
    contact_phone: str = None
    address: str = None
    legal_entity_name: str = None


@dataclass
class Contract:
    id: int
    legal_entity_id: int = None
    creation_time: datetime = None
    deadline_time: datetime = None
    is_finished: bool = None
    is_violated: bool = None
    price: float = None


@dataclass
class Standard:
    id: int
    name: str = None
    description: str = None


@dataclass
class ProductionLine:
    id: int
    standard_id: int = None
    production_start_time: datetime = None
    production_finish_time: datetime = None


@dataclass
class Resource:
    id: int
    type_id: int = None
    type: str = None
    production_line_id: int = None
    parent_production_line_id: int = None
    description: str = None
    flour_grade_id: int = None
    flour_grade: str = None
    vitreousness: int = None
    contamination: int = None
    grinding_grade_id: int = None
    grinding_grade: str = None
    contract_id: int = None


@dataclass
class Machine:
    id: int = -1
    is_powered: bool = None
    type_id: int = None
    type: str = None


@dataclass
class Worker:
    id: int = -1
    chief_id: int = None
    role_id: int = None
    role: str = None
    name: str = None


@dataclass
class _Primitive:
    id: int = -1
    name: str = None


class Role(_Primitive):
    pass


class MachineType(_Primitive):
    pass


class FlourGrade(_Primitive):
    pass


class GrindingGrade(_Primitive):
    pass
