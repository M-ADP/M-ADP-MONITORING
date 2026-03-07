from abc import ABC, abstractmethod
from src.core.app_deployment.model import AppDeployment

class AppDeploymentClient(ABC):

    @abstractmethod
    async def get(
            self,
            user_id : int,
            project_id : int,
            app_deployment_name: str,
    ) -> AppDeployment:
        raise NotImplementedError

class FakeAppDeploymentClient(AppDeploymentClient):
    async def get(
            self,
            user_id: int,
            project_id : int,
            app_deployment_name: str
    ) -> AppDeployment:
        return AppDeployment(
            id=1,
            name=app_deployment_name,
            owner_id=user_id,
            cpu_usage_percentage=100,
            memory_used="5GB",
            memory_total="10GB",
            disk_used="5GB",
            disk_total="10GB",
            current_instance=10,
            available_instances=100
        )
