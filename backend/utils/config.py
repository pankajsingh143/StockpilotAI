from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str
    app_version: str

    ollama_base_url: str 

    database_url: str 

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
        )

settings = Settings()
