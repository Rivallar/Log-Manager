from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """This class contains all the necessary environment variables for the application."""

    LOGGING_LEVEL: str
    PATH_TO_LOG_FOLDERS: str

    SSH_PORT: str

    AGENTLOG_USER: str
    AGENTLOG_PASSWORD: str
    AGENTLOG_HOST: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
