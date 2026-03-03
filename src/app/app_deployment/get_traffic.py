from src.app.base_use_case import BaseUseCase
from src.common.schema.request import TrafficRangeRequest
from src.core.app_deployment.model import AppDeployment


class GetAppDeploymentTrafficUseCase(BaseUseCase):

    async def __call__(
            self,
            app_deployment : AppDeployment,
            traffic_range : TrafficRangeRequest,
    ):
        pass