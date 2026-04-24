from fastapi import APIRouter, Depends, Path

from src.api.v1.app_deployment.shema.response import UserMetricsResponse
from src.app.app_deployment.get_users import GetProjectUsersUseCase
from src.common.schema.response import MadpResponse

project_router = APIRouter(
    prefix="",
    tags=["project"],
)


@project_router.get("/{project_id}/users")
async def get_project_users(
    project_id: str = Path(...),
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
