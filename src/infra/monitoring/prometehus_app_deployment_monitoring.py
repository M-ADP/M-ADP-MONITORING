from datetime import datetime, timezone
from typing import Any

from src.core.app_deployment.model import AppDeployment
from src.core.app_deployment.monitoring import AppDeploymentMonitoringClient
from src.core.client.metrics import MetricsClient
from src.core.traffic.model import Traffic, TrafficPoint
from src.infra.client.prometheus_metrics import PrometheusMetrics


class PrometehusAppDeploymentMonitoring(AppDeploymentMonitoringClient):

    # 총 요청 수 = istio_requests_total
    #


    # TODO: 실제 메트릭명 확인 후 수정 예정
    _TRAFFIC_QUERY = (
        'sum(rate(istio_requests_total{{deployment_id="{deployment_id}"}}[1m]))'
    )

    def __init__(
            self,
            metrics_client: MetricsClient = PrometheusMetrics(),
    ):
        self.metrics_client = metrics_client

    async def traffic(
            self,
            app_deployment: AppDeployment,
            start: datetime,
            end: datetime,
    ) -> Traffic:
        ql = self._TRAFFIC_QUERY.format(deployment_id=app_deployment.id)
        step = self._auto_step(start, end)
        data = await self.metrics_client.query_range(ql=ql, start=start, end=end, step=step)
        series = self._parse_series(data)
        return Traffic(
            id=app_deployment.id,
            start=start,
            end=end,
            series=series,
        )

    @staticmethod
    def _auto_step(start: datetime, end: datetime) -> int:
        """시간 범위에서 step(초)을 자동 계산 — 약 300 포인트, 최소 15초"""
        duration_seconds = (end - start).total_seconds()
        return max(15, int(duration_seconds / 300))

    @staticmethod
    def _parse_series(data: dict[str, Any]) -> list[TrafficPoint]:
        points: list[TrafficPoint] = []
        for result in data.get("result", []):
            for ts, val in result.get("values", []):
                points.append(TrafficPoint(
                    timestamp=datetime.fromtimestamp(float(ts), tz=timezone.utc),
                    value=float(val),
                ))
        points.sort(key=lambda p: p.timestamp)
        return points
