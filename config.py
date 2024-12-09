from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
    )
    bot_token: str
    server_address: str

settings = Settings()