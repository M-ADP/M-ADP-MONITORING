from src.core.client.app_deployment import AppDeploymentClient, FakeAppDeploymentClient
from src.infra.client.app_deployment import AppDeploymentClientImpl


async def get_app_deployment_client() -> AppDeploymentClient:
    # return FakeAppDeploymentClient()
    return AppDeploymentClientImpl()