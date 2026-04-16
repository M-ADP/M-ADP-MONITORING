from src.core.perform_ops.monitoring import PerformOpsMonitoringClient
from src.infra.monitoring.prometheus_perform_ops_monitoring import PrometheusPerformOpsMonitoring


async def get_perform_ops_monitoring() -> PerformOpsMonitoringClient:
    return PrometheusPerformOpsMonitoring()
