from fastapi import Depends

from src.app.base_use_case import BaseUseCase
from src.common.schema.request import TrafficRangeRequest
from src.core.app_deployment.model import AppDeployment, AppDeploymentTraffic
from src.core.app_deployment.monitoring import AppDeploymentMonitoringClient
from src.dependencies.get_app_deployment_monitoring import get_app_deployment_monitoring


class GetAppDeploymentTrafficUseCase(BaseUseCase):

    def __init__(
            self,
            monitoring_client : AppDeploymentMonitoringClient = Depends(get_app_deployment_monitoring)
    ) -> None:
        self.monitoring_client = monitoring_client

    async def __call__(
            self,
            app_deployment : AppDeployment,
            traffic_range : TrafficRangeRequest,
    ) -> AppDeploymentTraffic:

        traffic = await self.monitoring_client.traffic(
            app_deployment=app_deployment,
            start=traffic_range.start,
            end=traffic_range.end,
        )

        app_deployment_traffic = AppDeploymentTraffic(
            app_deployment=app_deployment,
            traffic=traffic,
        )
        return app_deployment_traffic
