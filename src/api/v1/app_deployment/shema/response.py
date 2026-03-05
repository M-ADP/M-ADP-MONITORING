from pydantic import BaseModel

from src.core.app_deployment.model import AppDeploymentTraffic


class AppDeploymentTrafficResponse(BaseModel):
    app_deployment_traffic : AppDeploymentTraffic