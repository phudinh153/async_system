from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


# API Settings
class APIUrlsSettings(BaseModel):
    """Configure public urls."""

    docs: str = "/docs"
    redoc: str = "/redoc"


class PublicApiSettings(BaseModel):
    """Configure public API settings."""

    name: str = "Backend"
    urls: APIUrlsSettings = APIUrlsSettings()


# Database Settings
class DatabaseSettings(BaseModel):
    # name: str = "db.postgres"
    is_async: bool = True
    db_schema: str = "public"
    @property
    def url(self) -> str:
        """Return synchronous database URL."""
        # return f"postgresql://postgres:postgres@localhost:5432/{self.name}"
        return "sqlite:///:memory:"

    @property
    def async_url(self) -> str:
        """Return asynchronous database URL."""
        return "sqlite+aiosqlite:///:memory:"


class KafkaSettings(BaseModel):
    bootstrap_servers: str = "localhost:9092"


# Logging Settings
class LoggingSettings(BaseModel):
    """Configure the logging engine."""

    # The time field can be formatted using more human-friendly tokens.
    # These constitute a subset of the one used by the Pendulum library
    # https://pendulum.eustace.io/docs/#tokens
    format: str = "{time:YYYY-MM-DD HH:mm:ss} | {level: <5} | {message}"

    # The .log filename
    file: str = "backend"

    # The .log file Rotation
    rotation: str = "1MB"

    # The type of compression
    compression: str = "zip"


class AccessTokenSettings(BaseModel):
    secret_key: str = "invaliad"
    ttl: int = 100  # seconds


class RefreshTokenSettings(BaseModel):
    secret_key: str = "invaliad"
    ttl: int = 100  # seconds


class AuthenticationSettings(BaseModel):
    access_token: AccessTokenSettings = AccessTokenSettings()
    refresh_token: RefreshTokenSettings = RefreshTokenSettings()
    algorithm: str = "HS256"
    scheme: str = "Bearer"


# Settings are powered by pydantic
# https://pydantic-docs.helpmanual.io/usage/settings/
class Settings(BaseSettings):
    debug: bool = True

    # Project file system
    root_dir: Path
    src_dir: Path

    # Infrastructure settings
    database: DatabaseSettings = DatabaseSettings()

    # Application configuration
    public_api: PublicApiSettings = PublicApiSettings()
    logging: LoggingSettings = LoggingSettings()
    authentication: AuthenticationSettings = AuthenticationSettings()

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=".env"
    )


# Define the root path
# --------------------------------------
ROOT_PATH = Path(__file__).parent.parent

# Load settings
# ======================================
settings = Settings(
    # NOTE: We would like to hard-code the root and applications directories
    #       to avoid overriding via environment variables
    root_dir=ROOT_PATH,
    src_dir=ROOT_PATH / "src",
)
