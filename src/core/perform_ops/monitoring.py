from abc import ABC, abstractmethod
from datetime import datetime

from src.core.perform_ops.model import NetworkMetrics, ResourceMetrics


class PerformOpsMonitoringClient(ABC):

    @abstractmethod
    async def network(
            self,
            app_deployment_id: int,
            start: datetime,
            end: datetime,
    ) -> NetworkMetrics:
        raise NotImplementedError

    @abstractmethod
    async def resource(
            self,
            app_deployment_id: int,
            start: datetime,
            end: datetime,
    ) -> ResourceMetrics:
        raise NotImplementedError
