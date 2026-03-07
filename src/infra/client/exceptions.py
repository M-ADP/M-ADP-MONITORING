from src.core.exceptions import BadRequestException


class PrometheusApiException(BadRequestException):
    """Prometheus API 호출 실패"""
    detail = "Prometheus API error"
