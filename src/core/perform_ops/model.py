from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class MetricPoint:
    timestamp: datetime
    value: float


@dataclass
class NetworkMetrics:
    """Istio 기반 네트워크 메트릭 — traffic + latency"""
    start: datetime
    end: datetime
    rps: list[MetricPoint] = field(default_factory=list)
    by_response_code: dict[str, list[MetricPoint]] = field(default_factory=dict)
    latency_p95: list[MetricPoint] = field(default_factory=list)


@dataclass
class ResourceMetrics:
    """cAdvisor 기반 컨테이너 리소스 메트릭 — cpu + memory + disk"""
    start: datetime
    end: datetime
    cpu: list[MetricPoint] = field(default_factory=list)
    memory: list[MetricPoint] = field(default_factory=list)
    disk: list[MetricPoint] = field(default_factory=list)
