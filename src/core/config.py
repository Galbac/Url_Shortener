from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str

    db_index: int
    db_port_redis: int

    secret_key: str
    base_url: str
    cache_ttl: int

    @property
    def async_database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def sync_database_url(self) -> str:
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def redis_url(self) -> str:
        return f"redis://{self.db_host}:{self.db_port_redis}/{self.db_index}"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding='utf-8', case_sensitive=False)

settings = Settings()