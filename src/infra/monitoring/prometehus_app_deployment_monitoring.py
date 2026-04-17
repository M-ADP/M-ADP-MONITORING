import asyncio
from datetime import datetime, timezone
from typing import Any

from src.core.app_deployment.model import AppDeployment, MetricPoint, NetworkMetrics, ResourceMetrics, UserMetrics
from src.core.app_deployment.monitoring import AppDeploymentMonitoringClient
from src.core.client.metrics import MetricsClient
from src.infra.client.prometheus_metrics import PrometheusMetrics

_TRAFFIC_RPS_QUERY = (
    'sum(rate(istio_requests_total{{x_app_deployment_id="{id}"}}[1m]))'
)
_TRAFFIC_BY_CODE_QUERY = (
    'sum by (response_code)'
    '(rate(istio_requests_total{{x_app_deployment_id="{id}"}}[1m]))'
)
_LATENCY_P95_QUERY = (
    'histogram_quantile(0.95,'
    ' sum by (le)'
    ' (rate(istio_request_duration_milliseconds_bucket{{x_app_deployment_id="{id}"}}[1m])))'
)
_CPU_QUERY = (
    'sum(rate(container_cpu_usage_seconds_total{{x_app_deployment_id="{id}",container!=""}}[1m]))'
)
_MEMORY_QUERY = (
    'sum(container_memory_working_set_bytes{{x_app_deployment_id="{id}",container!=""}})'
)
_DISK_QUERY = (
    'sum(container_fs_usage_bytes{{x_app_deployment_id="{id}",container!=""}})'
)

_APP_USER_QUERY = (
    'count(count by (x_user_id) (istio_requests_total{{x_app_deployment_id="{id}"}}[{range}]))'
)
_PROJECT_USER_QUERY = (
    'count(count by (x_user_id) (istio_requests_total{{namespace="project-{id}"}}[{range}]))'
)


class PrometehusAppDeploymentMonitoring(AppDeploymentMonitoringClient):

    def __init__(self, metrics_client: MetricsClient = PrometheusMetrics()):
        self.metrics_client = metrics_client

    async def network(
            self,
            app_deployment: AppDeployment,
            start: datetime,
            end: datetime,
    ) -> NetworkMetrics:
        step = self._auto_step(start, end)
        sid = str(app_deployment.id)

        rps_data, code_data, lat_data = await asyncio.gather(
            self._query_range(_TRAFFIC_RPS_QUERY.format(id=sid), start, end, step),
            self._query_range(_TRAFFIC_BY_CODE_QUERY.format(id=sid), start, end, step),
            self._query_range(_LATENCY_P95_QUERY.format(id=sid), start, end, step),
        )

        return NetworkMetrics(
            start=start,
            end=end,
            rps=self._parse_flat(rps_data),
            by_response_code=self._parse_by_label(code_data, "response_code"),
            latency_p95=self._parse_flat(lat_data),
        )

    async def resource(
            self,
            app_deployment: AppDeployment,
            start: datetime,
            end: datetime,
    ) -> ResourceMetrics:
        step = self._auto_step(start, end)
        sid = str(app_deployment.id)

        cpu_data, mem_data, disk_data = await asyncio.gather(
            self._query_range(_CPU_QUERY.format(id=sid), start, end, step),
            self._query_range(_MEMORY_QUERY.format(id=sid), start, end, step),
            self._query_range(_DISK_QUERY.format(id=sid), start, end, step),
        )

        return ResourceMetrics(
            start=start,
            end=end,
            cpu=self._parse_flat(cpu_data),
            memory=self._parse_flat(mem_data),
            disk=self._parse_flat(disk_data),
        )

    async def app_users(self, app_deployment: AppDeployment) -> UserMetrics:
        sid = str(app_deployment.id)
        now = datetime.now(timezone.utc)

        dau_data, wau_data, mau_data = await asyncio.gather(
            self._query(_APP_USER_QUERY.format(id=sid, range="24h"), now),
            self._query(_APP_USER_QUERY.format(id=sid, range="7d"), now),
            self._query(_APP_USER_QUERY.format(id=sid, range="30d"), now),
        )

        return UserMetrics(
            dau=self._parse_scalar(dau_data),
            wau=self._parse_scalar(wau_data),
            mau=self._parse_scalar(mau_data),
        )

    async def project_users(self, project_id: int | str) -> UserMetrics:
        sid = str(project_id)
        now = datetime.now(timezone.utc)

        dau_data, wau_data, mau_data = await asyncio.gather(
            self._query(_PROJECT_USER_QUERY.format(id=sid, range="24h"), now),
            self._query(_PROJECT_USER_QUERY.format(id=sid, range="7d"), now),
            self._query(_PROJECT_USER_QUERY.format(id=sid, range="30d"), now),
        )

        return UserMetrics(
            dau=self._parse_scalar(dau_data),
            wau=self._parse_scalar(wau_data),
            mau=self._parse_scalar(mau_data),
        )

    async def _query(self, ql: str, ts: datetime) -> dict:
        return await self.metrics_client.query(ql=ql, ts=ts)

    async def _query_range(self, ql: str, start: datetime, end: datetime, step: int) -> dict:
        return await self.metrics_client.query_range(ql=ql, start=start, end=end, step=step)

    @staticmethod
    def _auto_step(start: datetime, end: datetime) -> int:
        duration_seconds = (end - start).total_seconds()
        return max(15, int(duration_seconds / 300))

    @staticmethod
    def _parse_flat(data: dict[str, Any]) -> list[MetricPoint]:
        points: list[MetricPoint] = []
        for result in data.get("result", []):
            for ts, val in result.get("values", []):
                points.append(MetricPoint(
                    timestamp=datetime.fromtimestamp(float(ts), tz=timezone.utc),
                    value=float(val),
                ))
        points.sort(key=lambda p: p.timestamp)
        return points

    @staticmethod
    def _parse_scalar(data: dict[str, Any]) -> int:
        results = data.get("result", [])
        if not results:
            return 0
        # result_type이 "vector"인 경우 첫 번째 요소의 value[1]을 반환
        return int(float(results[0].get("value", [0, 0])[1]))

    @staticmethod
    def _parse_by_label(data: dict[str, Any], label: str) -> dict[str, list[MetricPoint]]:
        result: dict[str, list[MetricPoint]] = {}
        for series in data.get("result", []):
            key = series.get("metric", {}).get(label, "unknown")
            points = sorted(
                [
                    MetricPoint(
                        timestamp=datetime.fromtimestamp(float(ts), tz=timezone.utc),
                        value=float(val),
                    )
                    for ts, val in series.get("values", [])
                ],
                key=lambda p: p.timestamp,
            )
            result[key] = points
        return result
