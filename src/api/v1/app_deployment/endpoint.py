from fastapi import APIRouter, Depends

from src.api.v1.app_deployment.shema.response import AppDeploymentTrafficResponse
from src.api.v1.deps.get_app_deployment import get_app_deployment
from src.app.app_deployment.get_traffic import GetAppDeploymentTrafficUseCase
from src.common.schema.request import TrafficRangeRequest
from src.common.schema.response import MadpResponse
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
) -> MadpResponse[AppDeploymentTrafficResponse]:
    app_deployment_traffic = await usecase(
        app_deployment=app_deployment,
        traffic_range=traffic_range
    )

    app_deployment_response = AppDeploymentTrafficResponse(
        app_deployment_traffic=app_deployment_traffic
    )

    return MadpResponse(
        message="성공적인 트래픽 조회",
        data=app_deployment_response
    )
