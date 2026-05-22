from dataclasses import dataclass
from typing import Optional


@dataclass
class Area:
    area_id: int
    name: str


@dataclass
class Canton:
    canton_id: int
    name: str


@dataclass
class FarmingCategory:
    category_id: int
    name: str


@dataclass
class Observation:
    observation_id: int
    area: str
    canton: str
    category: str
    value: Optional[float]


@dataclass
class DirectPaymentCategory:
    payment_category_id: int
    name: str


@dataclass
class DirectPaymentObservation:
    direct_payment_observation_id: int
    canton: str
    payment_category: str
    value: Optional[float]
