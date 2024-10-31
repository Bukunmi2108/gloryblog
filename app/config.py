from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_url: str
    db_password: str
    db_user: str
    db_name: str
    db_host: str
    db_port: int = 5432
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()