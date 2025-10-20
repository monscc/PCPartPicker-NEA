from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class Part:
    id: str
    name: str
    category: str
    price: float
    attributes: Dict[str, Optional[str]]


@dataclass
class Build:
    name: str
    parts: Dict[str, Optional[Part]]

    def total_price(self) -> float:
        return sum(p.price for p in self.parts.values() if p is not None)
