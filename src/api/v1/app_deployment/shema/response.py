from pydantic import BaseModel

from src.common.schema.response import TrafficResponse


class AppDeploymentResponse(BaseModel):
    id: int
    name: str
    owner_id: int
    cpu_usage_percentage: int
    memory_used: str
    memory_total: str
    disk_used: str
    disk_total: str
    current_instance: int
    available_instances: int


class AppDeploymentTrafficResponse(BaseModel):
    app_deployment: AppDeploymentResponse
    traffic: TrafficResponse
