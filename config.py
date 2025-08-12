from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """This class contains all the necessary environment variables for the application."""

    LOGGING_LEVEL: str
    PATH_TO_LOG_FOLDERS: str
    SERVICE_ROUTES_NEEDED: int
    DAYS_TO_KEEP_LOGS: int
    TASK_SCHEDULED_TIME: str

    SSH_PORT: str

    AGENTLOG_USER: str
    AGENTLOG_PASSWORD: str
    AGENTLOG_HOST: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL(self) -> str:
        """Returns DSN for async connection to postgress DB"""
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def SCHEDULED_TIME(self) -> tuple[int, int]:
        """Returns hour and minutes of scheduled time to start a task of uploading new logs"""
        hour, minute = self.TASK_SCHEDULED_TIME.split(':')
        return (int(hour), int(minute))

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
