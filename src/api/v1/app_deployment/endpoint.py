from fastapi import APIRouter, Depends, Header, Path

from src.core.app_deployment.model import AppDeployment
from src.api.v1.app_deployment.shema.response import (
    MetricPointResponse,
    NetworkMetricsResponse,
    ResourceMetricsResponse,
    UserMetricsResponse,
)
from src.app.app_deployment.get_traffic import (
    GetAppDeploymentTrafficUseCase,
    GetAppDeploymentResourceUseCase,
)
from src.app.app_deployment.get_users import (
    GetAppDeploymentUsersUseCase,
    GetProjectUsersUseCase,
)
from src.common.schema.request import TrafficRangeRequest
from src.common.schema.response import MadpResponse

app_deployment_router = APIRouter(
    prefix="/app-deployment",
    tags=["app-deployment"],
)

project_router = APIRouter(
    prefix="",
    tags=["project"],
)


@app_deployment_router.get("/{project_id}/{app_deployment_id}/users")
async def get_app_users(
    project_id: str = Path(...),
    app_deployment_id: str = Path(...),
    user_id: int = Header(..., alias="X-User-Id"),
    usecase: GetAppDeploymentUsersUseCase = Depends(GetAppDeploymentUsersUseCase),
) -> MadpResponse[UserMetricsResponse]:
    result = await usecase(app_deployment=AppDeployment(id=app_deployment_id, project_id=project_id))

    return MadpResponse(
        message="고유 사용자 조회 성공",
        data=UserMetricsResponse(
            dau=result.dau,
            wau=result.wau,
            mau=result.mau,
        ),
    )


@project_router.get("/{project_id}/users")
async def get_project_users(
    project_id: str = Path(...),
    user_id: int = Header(..., alias="X-User-Id"),
    usecase: GetProjectUsersUseCase = Depends(GetProjectUsersUseCase),
) -> MadpResponse[UserMetricsResponse]:
    result = await usecase(project_id=project_id)

    return MadpResponse(
        message="프로젝트 고유 사용자 조회 성공",
        data=UserMetricsResponse(
            dau=result.dau,
            wau=result.wau,
            mau=result.mau,
        ),
    )


@app_deployment_router.get("/{project_id}/{app_deployment_id}/traffic")
async def get_traffic(
    project_id: str = Path(...),
    app_deployment_id: str = Path(...),
    user_id: int = Header(..., alias="X-User-Id"),
    traffic_range: TrafficRangeRequest = Depends(),
    usecase: GetAppDeploymentTrafficUseCase = Depends(GetAppDeploymentTrafficUseCase),
) -> MadpResponse[NetworkMetricsResponse]:
    result = await usecase(
        app_deployment=AppDeployment(id=app_deployment_id, project_id=project_id),
        traffic_range=traffic_range,
    )

    def to_points(series):
        return [
            MetricPointResponse(timestamp=p.timestamp, value=p.value) for p in series
        ]

    return MadpResponse(
        message="성공적인 트래픽 조회",
        data=NetworkMetricsResponse(
            start=result.start,
            end=result.end,
            rps=to_points(result.rps),
            by_response_code={
                code: to_points(pts) for code, pts in result.by_response_code.items()
            },
            latency_p95=to_points(result.latency_p95),
        ),
    )


@app_deployment_router.get("/{project_id}/{app_deployment_id}/resource")
async def get_resource(
    project_id: str = Path(...),
    app_deployment_id: str = Path(...),
    user_id: int = Header(..., alias="X-User-Id"),
    traffic_range: TrafficRangeRequest = Depends(),
    usecase: GetAppDeploymentResourceUseCase = Depends(GetAppDeploymentResourceUseCase),
) -> MadpResponse[ResourceMetricsResponse]:
    result = await usecase(
        app_deployment=AppDeployment(id=app_deployment_id, project_id=project_id),
        traffic_range=traffic_range,
    )

    def to_points(series):
        return [
            MetricPointResponse(timestamp=p.timestamp, value=p.value) for p in series
        ]

    return MadpResponse(
        message="성공적인 리소스 조회",
        data=ResourceMetricsResponse(
            start=result.start,
            end=result.end,
            cpu=to_points(result.cpu),
            memory=to_points(result.memory),
            disk=to_points(result.disk),
        ),
    )
