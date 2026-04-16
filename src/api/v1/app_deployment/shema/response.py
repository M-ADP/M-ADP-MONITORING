from datetime import datetime

from pydantic import BaseModel


class MetricPointResponse(BaseModel):
    timestamp: datetime
    value: float


class NetworkMetricsResponse(BaseModel):
    start: datetime
    end: datetime
    rps: list[MetricPointResponse] = []
    by_response_code: dict[str, list[MetricPointResponse]] = {}
    latency_p95: list[MetricPointResponse] = []


class ResourceMetricsResponse(BaseModel):
    start: datetime
    end: datetime
    cpu: list[MetricPointResponse] = []
    memory: list[MetricPointResponse] = []
    disk: list[MetricPointResponse] = []


class UserMetricsResponse(BaseModel):
    dau: int
    wau: int
    mau: int
