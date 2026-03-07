from src.common.config.app_deployment import AppDeploymentConfig
from src.core.app_deployment.model import AppDeployment
from src.core.client.app_deployment import AppDeploymentClient
from src.core.client.requester import Requester
from src.dependencies.requester import get_requester

class AppDeploymentClientImpl(AppDeploymentClient):

    def __init__(
            self,
            requester : Requester = get_requester(),
            config : AppDeploymentConfig = AppDeploymentConfig()
    ) -> None:
        self.requester = requester
        self.base_url = f"{config.url}/apps"


    async def get(
            self,
            user_id: int,
            project_id: int,
            app_deployment_name: str
    ) -> AppDeployment:
        headers = {
            "X-User-Id": user_id,
        }

        params = {
            "project_id": str(project_id),
            "app_name": app_deployment_name,
        }

        response = await self.requester.get(
            url=f"{self.base_url}/status",
            headers=headers,
            params=params,
        )

        app_deployment_response = response['data']

        return AppDeployment(
            id=app_deployment_response['id'],
            name=app_deployment_name,
            owner_id=app_deployment_response['user_id'],
            cpu_usage_percentage=app_deployment_response['cpu_usage_percentage'],
            memory_used=app_deployment_response['memory_used'],
            memory_total=app_deployment_response['memory_total'],
            disk_used=app_deployment_response['disk_used'],
            disk_total=app_deployment_response['disk_total'],
            current_instance=app_deployment_response['current_instance'],
            available_instances=app_deployment_response['available_instances'],
        )