from abc import ABC, abstractmethod
from datetime import datetime

from src.core.traffic.model import Traffic


class AppDeploymentMonitor(ABC):

    @abstractmethod
    async def traffic(
            self,
            id : int,
            start: datetime,
            end: datetime,
    ) -> Traffic:
        raise NotImplementedError
