from pydantic import IPvAnyAddress
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='api_')
    host: IPvAnyAddress = '0.0.0.0'
    port: int = 8000
    version: str = "local"
    root_path: str = ""
