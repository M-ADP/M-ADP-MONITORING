from dataclasses import dataclass

from src.core.traffic.model import Traffic


@dataclass
class AppDeployment:
    id : int
    owner_id : int


@dataclass
class AppDeploymentTraffic:
    app_deployment : AppDeployment
    traffic : Traffic
