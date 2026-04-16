from fastapi import Depends

from src.app.base_use_case import BaseUseCase
from src.core.app_deployment.model import AppDeployment, UserMetrics
from src.core.app_deployment.monitoring import AppDeploymentMonitoringClient
from src.dependencies.get_app_deployment_monitoring import get_app_deployment_monitoring


class GetAppDeploymentUsersUseCase(BaseUseCase):
    def __init__(
        self,
        monitoring_client: AppDeploymentMonitoringClient = Depends(
            get_app_deployment_monitoring
        ),
    ) -> None:
        self.monitoring_client = monitoring_client

    async def __call__(self, app_deployment: AppDeployment) -> UserMetrics:
        return await self.monitoring_client.app_users(app_deployment=app_deployment)


class GetProjectUsersUseCase(BaseUseCase):
    def __init__(
        self,
        monitoring_client: AppDeploymentMonitoringClient = Depends(
            get_app_deployment_monitoring
        ),
    ) -> None:
        self.monitoring_client = monitoring_client

    async def __call__(self, project_id: int) -> UserMetrics:
        return await self.monitoring_client.project_users(project_id=project_id)
