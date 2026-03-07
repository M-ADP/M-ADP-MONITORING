from fastapi import FastAPI, APIRouter

from src.api.v1.app_deployment.endpoint import app_deployment_router


def register_routers(app: FastAPI) -> None:

    monitoring_router = APIRouter(prefix="/monitoring")
    monitoring_router.include_router(app_deployment_router)

    app.include_router(monitoring_router)
