from pydantic_settings import BaseSettings

from src.common.const.vault import VAULT_ENV_FILE


class PrometheusConfig(BaseSettings):
    url: str = "http://localhost:9090"

    class Config:
        env_prefix = "PROMETHEUS_"
        env_file = VAULT_ENV_FILE
        env_file_encoding = "utf-8"
        extra = "ignore"
