from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class TrafficPoint:
    timestamp: datetime
    value: float


@dataclass
class Traffic:
    id: int
    start: datetime
    end: datetime
    series: list[TrafficPoint] = field(default_factory=list)
