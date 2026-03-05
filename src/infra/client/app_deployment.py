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
            app_deployment_id: int
    ) -> AppDeployment:
        headers = {
            "X-User-Id": user_id,
        }

        response = await self.requester.get(
            url=self.base_url,
            headers=headers,
        )

        return AppDeployment(
            id=response['id'],
            owner_id=response['user_id']
        )