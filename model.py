from dataclasses import dataclass
from datetime import datetime


@dataclass
class LegalEntity:
    id: int = -1
    contact_phone: str = None
    address: str = None
    name: str = None


@dataclass
class Contract:
    id: int = -1
    legal_entity_id: int = None
    creation_time: datetime = None
    deadline_time: datetime = None
    is_finished: bool = None
    is_violated: bool = None
    price: float = None
    resources: list[int] = None


@dataclass
class Standard:
    id: int = -1
    name: str = None
    description: str = None


@dataclass
class ProductionLine:
    id: int = -1
    standard_id: int = None
    production_start_time: datetime = None
    production_finish_time: datetime = None
    resources: list[int] = None
    results: list[int] = None
    workers: list[int] = None
    machines: list[int] = None


@dataclass
class Resource:
    id: int = -1
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
class ResourceType:
    id: int = -1
    name: str = None
    is_producible: bool = None


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
