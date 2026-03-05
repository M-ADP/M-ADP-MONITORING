from abc import ABC, abstractmethod
from src.core.app_deployment.model import AppDeployment

class AppDeploymentClient(ABC):

    @abstractmethod
    async def get(
            self,
            user_id : int,
            app_deployment_id: int,
    ) -> AppDeployment:
        raise NotImplementedError

class FakeAppDeploymentClient(AppDeploymentClient):
    async def get(
            self,
            user_id: int,
            app_deployment_id: int
    ) -> AppDeployment:
        return AppDeployment(
            id=app_deployment_id,
            owner_id=user_id,
        )