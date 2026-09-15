from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "MINDCARE NER"
    API_V1_STR: str = "/api/v1"

    # Environment & Database (defaults for dev/testing only)
    ENVIRONMENT: str = "development"
    DATABASE_URL: str = "sqlite:///./mindcare_test.db"

    # Security & JWT (must be overridden in production)
    JWT_SECRET_KEY: str = "dev-insecure-key-do-not-use-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
