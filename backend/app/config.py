from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    azure_openai_endpoint: str = ""
    azure_openai_base_url: str = ""
    azure_openai_api_key: str = ""
    azure_openai_deployment: str = "gpt-5.4-mini"
    enable_llm: bool = True
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str = ""
    database_url: str = "sqlite:///./data/app.db"
    resume_directory: str = "./data/resumes"
    dense_model: str = "BAAI/bge-small-en-v1.5"
    reranker_model: str = "Xenova/ms-marco-MiniLM-L-6-v2"
    cors_origins: str = "http://localhost:5173"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def azure_base_url(self) -> str:
        if self.azure_openai_base_url:
            return self.azure_openai_base_url.rstrip("/") + "/"
        if not self.azure_openai_endpoint:
            raise ValueError("AZURE_OPENAI_ENDPOINT not configured")
        return self.azure_openai_endpoint.rstrip("/") + "/openai/v1/"


@lru_cache
def get_settings() -> Settings:
    return Settings()
