from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class AppDeployment:
    id: int


@dataclass
class MetricPoint:
    timestamp: datetime
    value: float


@dataclass
class NetworkMetrics:
    start: datetime
    end: datetime
    rps: list[MetricPoint] = field(default_factory=list)
    by_response_code: dict[str, list[MetricPoint]] = field(default_factory=dict)
    latency_p95: list[MetricPoint] = field(default_factory=list)


@dataclass
class ResourceMetrics:
    start: datetime
    end: datetime
    cpu: list[MetricPoint] = field(default_factory=list)
    memory: list[MetricPoint] = field(default_factory=list)
    disk: list[MetricPoint] = field(default_factory=list)


@dataclass
class UserMetrics:
    dau: int  # 최근 24h 고유 사용자
    wau: int  # 최근 7d 고유 사용자
    mau: int  # 최근 30d 고유 사용자
