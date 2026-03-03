from fastapi import Path, Header
from src.core.app_deployment.model import AppDeployment


async def get_app_deployment(
        app_deployment_id : int = Path(...),
        user_id: int = Header(..., alias="user-id")
) -> AppDeployment:
    return AppDeployment(
        id=app_deployment_id,
        owner_id=user_id
    )
