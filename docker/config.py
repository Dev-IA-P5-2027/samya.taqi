from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    qdrant_url: str = "http://qdrant-container:6333"
    collection_name: str = "test_docker"
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    mistral_api_key: SecretStr
    data_path: str = "./data"
    top_k: int = 3
    temperature: float = 0.2
    max_tokens: int = 512
    debug: bool = False
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore" #évite le crash si une variable d'environnement inconnue
    )

settings = Settings()
