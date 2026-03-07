from dataclasses import dataclass

from src.core.traffic.model import Traffic


@dataclass
class AppDeployment:
    id : int
    name : str
    owner_id : int
    cpu_usage_percentage : int
    memory_used : str
    memory_total: str
    disk_used : str

    disk_total: str
    current_instance : int
    available_instances : int


@dataclass
class AppDeploymentTraffic:
    app_deployment : AppDeployment
    traffic : Traffic
