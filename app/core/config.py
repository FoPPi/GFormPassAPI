import os
from functools import lru_cache
from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

# Load environment variables from the new path
load_dotenv('envs/dev.env')

class Settings(BaseSettings):
    # Server settings
    PROJECT_NAME: str = "GFormPass API"
    VERSION: str = "1.0.0"

    # Database settings
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", "5432"))  # Added default for safety
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")

    # OpenAI settings
    OPENAI_ASSISTANT_ID: str = os.getenv("OPENAI_ASSISTANT_ID")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")

    # Api settings
    API_KEY: str = os.getenv("API_KEY")
    ADMIN_KEY: str = os.getenv("ADMIN_KEY")

    # Donatello settings
    DONATELLO_KEY: str = os.getenv("DONATELLO_KEY")
    DONATELLO_API_KEY: str = os.getenv("DONATELLO_API_KEY")

    # SMTP settings
    SMTP_HOST: str = os.getenv("SMTP_HOST")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD")

    class Config:
        case_sensitive = True
        env_file = 'envs/dev.env'  # Added explicit env_file configuration
        env_file_encoding = 'utf-8'

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()