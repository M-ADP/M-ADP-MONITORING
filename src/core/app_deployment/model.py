from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class AppDeployment:
    id: int | str
    name: str | None = None
    owner_id: int | None = None
    cpu_usage_percentage: float | None = None
    memory_used: int | None = None
    memory_total: int | None = None
    disk_used: int | None = None
    disk_total: int | None = None
    current_instance: int | None = None
    available_instances: int | None = None


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
