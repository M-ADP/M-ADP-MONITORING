from fastapi import APIRouter, Depends

from src.api.v1.app_deployment.shema.response import AppDeploymentResponse, AppDeploymentTrafficResponse
from src.api.v1.deps.get_app_deployment import get_app_deployment
from src.app.app_deployment.get_traffic import GetAppDeploymentTrafficUseCase
from src.common.schema.request import TrafficRangeRequest
from src.common.schema.response import MadpResponse, TrafficPointResponse, TrafficResponse
from src.core.app_deployment.model import AppDeployment

app_deployment_router = APIRouter(
    prefix="/app-deployment",
    tags=["app-deployment"]
)

@app_deployment_router.get("/{project_id}/{app_deployment_name}")
async def get_app_deployment_traffic(
        app_deployment: AppDeployment = Depends(get_app_deployment),
        traffic_range: TrafficRangeRequest = Depends(),
        usecase : GetAppDeploymentTrafficUseCase = Depends(GetAppDeploymentTrafficUseCase)
) -> MadpResponse[AppDeploymentTrafficResponse]:
    app_deployment_traffic = await usecase(
        app_deployment=app_deployment,
        traffic_range=traffic_range
    )

    traffic = app_deployment_traffic.traffic
    dep = app_deployment_traffic.app_deployment

    return MadpResponse(
        message="성공적인 트래픽 조회",
        data=AppDeploymentTrafficResponse(
            app_deployment=AppDeploymentResponse(
                id=dep.id,
                name=dep.name,
                owner_id=dep.owner_id,
                cpu_usage_percentage=dep.cpu_usage_percentage,
                memory_used=dep.memory_used,
                memory_total=dep.memory_total,
                disk_used=dep.disk_used,
                disk_total=dep.disk_total,
                current_instance=dep.current_instance,
                available_instances=dep.available_instances,
            ),
            traffic=TrafficResponse(
                start=traffic.start,
                end=traffic.end,
                series=[
                    TrafficPointResponse(timestamp=p.timestamp, value=p.value)
                    for p in traffic.series
                ],
            ),
        )
    )
