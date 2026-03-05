from fastapi import Path, Header, Depends
from src.core.app_deployment.model import AppDeployment
from src.core.client.app_deployment import AppDeploymentClient
from src.dependencies.app_deployment_client import get_app_deployment_client


async def get_app_deployment(
        app_deployment_id : int = Path(...),
        user_id: int = Header(..., alias="X-User-Id"),
        app_deployment_client : AppDeploymentClient = Depends(get_app_deployment_client),
) -> AppDeployment:

    return await app_deployment_client.get(
        user_id=user_id,
        app_deployment_id=app_deployment_id
    )
