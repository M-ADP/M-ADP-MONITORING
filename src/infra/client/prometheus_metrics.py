from datetime import datetime, timezone
from typing import Any, Dict

from src.common.config.prometheus_config import PrometheusConfig
from src.core.client.metrics import MetricsClient
from src.infra.client.exceptions import PrometheusApiException
from src.core.client.requester import Requester
from src.dependencies.requester import get_requester


def _to_unix_seconds(dt: datetime) -> float:
    # Prometheus는 unix timestamp(sec) 받음
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)  # naive면 UTC로 간주 (정책 바꾸고 싶으면 여기)
    return dt.timestamp()


def _ensure_success(payload: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        raise PrometheusApiException(f"Prometheus returned non-object payload: {type(payload)}")

    if payload.get("status") != "success":
        err_type = payload.get("errorType", "unknown")
        err = payload.get("error", "unknown error")
        raise PrometheusApiException(f"Prometheus API error ({err_type}): {err}")

    data = payload.get("data")
    if data is None:
        raise PrometheusApiException("Prometheus response missing 'data'")
    return data

class PrometheusMetrics(MetricsClient):

    def __init__(
            self,
            config: PrometheusConfig,
            requester: Requester = get_requester(),
    ):
        self.requester = requester
        self.prometheus_url = config.url

    async def query(self, ql: str, ts: datetime) -> Any:
        url = f"{self.prometheus_url}/api/v1/query"
        params = {
            "query": ql,
            "time": _to_unix_seconds(ts),
        }
        payload = await self.requester.get(url=url, params=params)
        return _ensure_success(payload)

    async def query_range(
            self, ql: str,
            start: datetime,
            end: datetime,
            step: int
    ) -> Any:
        if end <= start:
            raise ValueError("end must be greater than start")
        if step <= 0:
            raise ValueError("step must be positive (seconds)")

        url = f"{self.prometheus_url}/api/v1/query_range"
        params = {
            "query": ql,
            "start": _to_unix_seconds(start),
            "end": _to_unix_seconds(end),
            "step": step,  # seconds (예: 15, 60, 300)
        }
        payload = await self.requester.get(url=url, params=params)
        return _ensure_success(payload)
