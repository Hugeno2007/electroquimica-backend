import os
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import quote, urlencode

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env", override=False)


def _read_origins() -> list[str]:
    value = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173,http://localhost:4173,http://127.0.0.1:4173",
    )
    return [origin.strip() for origin in value.split(",") if origin.strip()]


def _read_database_url() -> str:
    explicit_url = os.getenv("DATABASE_URL")
    if explicit_url:
        return explicit_url

    host = os.getenv("DB_HOST")
    name = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    if host and name and user and password:
        port = os.getenv("DB_PORT", "5432")
        query = urlencode(
            {
                "sslmode": os.getenv("DB_SSLMODE", "require"),
                "channel_binding": os.getenv("DB_CHANNEL_BINDING", "require"),
            }
        )
        credentials = f"{quote(user, safe='')}:{quote(password, safe='')}"
        return f"postgresql://{credentials}@{host}:{port}/{quote(name, safe='')}?{query}"

    return "sqlite:///./electroquimica.db"


@dataclass(frozen=True)
class Settings:
    database_url: str = field(default_factory=_read_database_url)
    cors_origins: list[str] = field(default_factory=_read_origins)


settings = Settings()