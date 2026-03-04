from pydantic_settings import BaseSettings


class PrometheusConfig(BaseSettings):
    url: str = "http://localhost:9090"

    class Config:
        env_prefix = "PROMETHEUS_"
