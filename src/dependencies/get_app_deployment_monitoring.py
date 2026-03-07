from src.core.app_deployment.monitoring import AppDeploymentMonitoringClient
from src.infra.monitoring.prometehus_app_deployment_monitoring import PrometehusAppDeploymentMonitoring


async def get_app_deployment_monitoring() -> AppDeploymentMonitoringClient:
    return PrometehusAppDeploymentMonitoring()