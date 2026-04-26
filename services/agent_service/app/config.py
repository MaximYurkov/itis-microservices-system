from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    service_name: str = "agent-service"
    app_port: int = 8002
    kafka_bootstrap_servers: str = "kafka:9092"
    task_created_topic: str = "task.created"
    task_completed_topic: str = "task.completed"
    redis_url: str = "redis://redis:6379/0"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
