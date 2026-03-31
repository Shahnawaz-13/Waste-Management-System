from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Smart Waste Management API"
    environment: str = "development"
    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db_name: str = "smart_waste_db"
    upload_dir: str = "uploads"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
