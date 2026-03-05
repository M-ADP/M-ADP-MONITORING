from pydantic_settings import BaseSettings
from src.common.const.vault import VAULT_ENV_FILE


class AppDeploymentConfig(BaseSettings):
    url: str = "http://localhost:8000"

    class Config:
        env_prefix = "APP_DEPLOYMENT_"
        env_file = VAULT_ENV_FILE
        env_file_encoding = "utf-8"
        extra = "ignore"
