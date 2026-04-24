from fastapi import FastAPI, APIRouter

from src.api.v1.app_deployment.endpoint import app_deployment_router
from src.api.v1.project.endpoint import project_router


def register_routers(app: FastAPI) -> None:

    monitoring_router = APIRouter(prefix="/monitoring")
    monitoring_router.include_router(app_deployment_router)

    project_monitoring_router = APIRouter(prefix="/project")
    project_monitoring_router.include_router(project_router)

    monitoring_router.include_router(project_monitoring_router)

    app.include_router(monitoring_router)
