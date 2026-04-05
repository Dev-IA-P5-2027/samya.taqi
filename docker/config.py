from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection_name: str = "test_docker"
    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    mistral_api_key: SecretStr

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

settings = Settings()