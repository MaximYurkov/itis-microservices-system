from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    service_name: str = "notification-service"
    app_port: int = 8003
    kafka_bootstrap_servers: str = "kafka:9092"
    task_completed_topic: str = "task.completed"
    mongo_url: str = "mongodb://mongo:27017"
    mongo_db: str = "notifications_db"
    mongo_collection: str = "notifications"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
