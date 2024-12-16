# src/config.py


from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for the LangGraph exercises.

    This includes API keys and other configuration needed for the exercises.
    The values are loaded from environment variables or .env file.
    """

    # OpenAI API configuration
    openai_api_key: str

    # Tavily API configuration
    tavily_api_key: str

    # Optional LangSmith configuration
    langsmith_api_key: str | None = None
    langsmith_project: str | None = "deepdive-langgraph"

    # Environment configuration
    environment: str = "development"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )


# Create settings instance
settings = Settings()
