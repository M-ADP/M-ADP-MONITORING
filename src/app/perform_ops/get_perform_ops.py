from fastapi import Depends

from src.app.base_use_case import BaseUseCase
from src.common.schema.request import TrafficRangeRequest
from src.core.perform_ops.model import NetworkMetrics, ResourceMetrics
from src.core.perform_ops.monitoring import PerformOpsMonitoringClient
from src.dependencies.get_perform_ops_monitoring import get_perform_ops_monitoring


class GetNetworkMetricsUseCase(BaseUseCase):

    def __init__(
            self,
            monitoring_client: PerformOpsMonitoringClient = Depends(get_perform_ops_monitoring),
    ) -> None:
        self.monitoring_client = monitoring_client

    async def __call__(
            self,
            app_deployment_id: int,
            traffic_range: TrafficRangeRequest,
    ) -> NetworkMetrics:
        return await self.monitoring_client.network(
            app_deployment_id=app_deployment_id,
            start=traffic_range.start,
            end=traffic_range.end,
        )


class GetResourceMetricsUseCase(BaseUseCase):

    def __init__(
            self,
            monitoring_client: PerformOpsMonitoringClient = Depends(get_perform_ops_monitoring),
    ) -> None:
        self.monitoring_client = monitoring_client

    async def __call__(
            self,
            app_deployment_id: int,
            traffic_range: TrafficRangeRequest,
    ) -> ResourceMetrics:
        return await self.monitoring_client.resource(
            app_deployment_id=app_deployment_id,
            start=traffic_range.start,
            end=traffic_range.end,
        )
