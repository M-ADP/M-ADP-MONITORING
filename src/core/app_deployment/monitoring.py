from abc import ABC, abstractmethod
from datetime import datetime

from src.core.app_deployment.model import AppDeployment, NetworkMetrics, ResourceMetrics


class AppDeploymentMonitoringClient(ABC):

    @abstractmethod
    async def network(
            self,
            app_deployment: AppDeployment,
            start: datetime,
            end: datetime,
    ) -> NetworkMetrics:
        raise NotImplementedError

    @abstractmethod
    async def resource(
            self,
            app_deployment: AppDeployment,
            start: datetime,
            end: datetime,
    ) -> ResourceMetrics:
        raise NotImplementedError
