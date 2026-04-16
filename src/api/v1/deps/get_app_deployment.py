from fastapi import Path, Header

from src.core.app_deployment.model import AppDeployment


async def get_app_deployment(
        project_id: int = Path(...),
        app_deployment_id: int = Path(...),
        user_id: int = Header(..., alias="X-User-Id"),
) -> AppDeployment:
    return AppDeployment(id=app_deployment_id)
