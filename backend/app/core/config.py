from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Product Metadata Platform"
    app_env: str = "development"
    database_url: str = "sqlite:///./product_metadata.db"
    storage_dir: str = "./storage"
    vector_index_path: str = "./storage/vector.index"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    allow_origins: list[str] = ["*"]

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')


settings = Settings()
