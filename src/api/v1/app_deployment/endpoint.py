from fastapi import APIRouter, Depends, Header, Path

from src.api.v1.perform_ops.schema.response import (
    MetricPointResponse,
    NetworkMetricsResponse,
    ResourceMetricsResponse,
)
from src.app.perform_ops.get_perform_ops import GetNetworkMetricsUseCase, GetResourceMetricsUseCase
from src.common.schema.request import TrafficRangeRequest
from src.common.schema.response import MadpResponse

app_deployment_router = APIRouter(
    prefix="/app-deployment",
    tags=["app-deployment"],
)


@app_deployment_router.get("/{project_id}/{app_deployment_id}/traffic")
async def get_traffic(
        project_id: int = Path(...),
        app_deployment_id: int = Path(...),
        user_id: int = Header(..., alias="X-User-Id"),
        traffic_range: TrafficRangeRequest = Depends(),
        usecase: GetNetworkMetricsUseCase = Depends(GetNetworkMetricsUseCase),
) -> MadpResponse[NetworkMetricsResponse]:
    result = await usecase(
        app_deployment_id=app_deployment_id,
        traffic_range=traffic_range,
    )

    def to_points(series):
        return [MetricPointResponse(timestamp=p.timestamp, value=p.value) for p in series]

    return MadpResponse(
        message="성공적인 트래픽 조회",
        data=NetworkMetricsResponse(
            start=result.start,
            end=result.end,
            rps=to_points(result.rps),
            by_response_code={
                code: to_points(pts)
                for code, pts in result.by_response_code.items()
            },
            latency_p95=to_points(result.latency_p95),
        ),
    )


@app_deployment_router.get("/{project_id}/{app_deployment_id}/resource")
async def get_resource(
        project_id: int = Path(...),
        app_deployment_id: int = Path(...),
        user_id: int = Header(..., alias="X-User-Id"),
        traffic_range: TrafficRangeRequest = Depends(),
        usecase: GetResourceMetricsUseCase = Depends(GetResourceMetricsUseCase),
) -> MadpResponse[ResourceMetricsResponse]:
    result = await usecase(
        app_deployment_id=app_deployment_id,
        traffic_range=traffic_range,
    )

    def to_points(series):
        return [MetricPointResponse(timestamp=p.timestamp, value=p.value) for p in series]

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
