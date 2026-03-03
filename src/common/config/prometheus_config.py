from pydantic_settings import BaseSettings


class PrometheusConfig(BaseSettings):
    url: str

    class Config:
        env_prefix = "PROMETHEUS_"
