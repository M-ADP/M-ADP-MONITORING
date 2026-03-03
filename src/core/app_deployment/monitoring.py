from abc import ABC, abstractmethod
from datetime import datetime

from src.core.app_deployment.model import AppDeployment
from src.core.traffic.model import Traffic

class AppDeploymentMonitoringClient(ABC):

    @abstractmethod
    async def traffic(
            self,
            app_deployment : AppDeployment,
            start: datetime,
            end: datetime,
    ) -> Traffic:
        raise NotImplementedError
