from abc import ABC, abstractmethod
from datetime import datetime

from src.core.app_deployment.model import AppDeployment, NetworkMetrics, ResourceMetrics, UserMetrics


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

    @abstractmethod
    async def app_users(self, app_deployment: AppDeployment) -> UserMetrics:
        raise NotImplementedError

    @abstractmethod
    async def project_users(self, project_id: int | str) -> UserMetrics:
        raise NotImplementedError
