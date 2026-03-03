from fastapi import APIRouter, Header, Depends
from src.api.v1.deps.get_app_deployment import get_app_deployment
from src.app.app_deployment.get_traffic import GetAppDeploymentTrafficUseCase
from src.common.schema.request import TrafficRangeRequest
from src.core.app_deployment.model import AppDeployment, AppDeploymentTraffic

app_deployment_router = APIRouter(
    prefix="/app-deployment",
    tags=["app-deployment"]
)

@app_deployment_router.get("/{app_deployment_id}")
async def get_app_deployment_traffic(
        app_deployment: AppDeployment = Depends(get_app_deployment),
        traffic_range: TrafficRangeRequest = Depends(),
        usecase : GetAppDeploymentTrafficUseCase = Depends(GetAppDeploymentTrafficUseCase)
) -> AppDeploymentTraffic:
    app_deployment_traffic = await usecase(
        app_deployment=app_deployment,
        traffic_range=traffic_range
    )

    return app_deployment_traffic