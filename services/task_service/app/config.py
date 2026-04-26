from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    service_name: str = "task-service"
    app_port: int = 8001
    database_url: str = "postgresql+psycopg://tasks_user:tasks_password@postgres:5432/tasks_db"
    kafka_bootstrap_servers: str = "kafka:9092"
    task_created_topic: str = "task.created"
    task_completed_topic: str = "task.completed"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
