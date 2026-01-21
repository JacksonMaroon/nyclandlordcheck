from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from functools import lru_cache


class Settings(BaseSettings):
    database_url: str = Field(
        default="postgresql+asyncpg://landlord:landlord_dev_password@localhost:5432/landlord_shady",
        validation_alias="DATABASE_URL"
    )
    socrata_app_token: str = ""
    socrata_base_url: str = "https://data.cityofnewyork.us"
    socrata_rate_limit: int = 10  # requests per second
    socrata_page_size: int = 50000

    # Logging
    log_level: str = "INFO"

    # Cache (optional - uses in-memory if not set)
    redis_url: str = ""

    # Dataset IDs
    hpd_violations_dataset: str = "wvxf-dwi5"
    hpd_registrations_dataset: str = "tesw-yqqr"
    registration_contacts_dataset: str = "feu5-w2e2"
    complaints_311_dataset: str = "erm2-nwe9"
    dob_violations_dataset: str = "6bgk-3dad"
    evictions_dataset: str = "6z8x-wfk4"
    acris_master_dataset: str = "bnx9-e6tj"
    acris_parties_dataset: str = "636b-3b5g"
    acris_legals_dataset: str = "8h5j-fqxa"

    @field_validator("database_url", mode="after")
    @classmethod
    def convert_database_url(cls, v: str) -> str:
        """Convert postgresql:// or postgres:// to postgresql+asyncpg:// for async support."""
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Raw DATABASE_URL value: {v[:50]}...")  # Log first 50 chars (mask credentials)

        if v.startswith("postgresql://"):
            converted = v.replace("postgresql://", "postgresql+asyncpg://", 1)
            logger.info(f"Converted postgresql:// to postgresql+asyncpg://")
            return converted
        elif v.startswith("postgres://"):
            converted = v.replace("postgres://", "postgresql+asyncpg://", 1)
            logger.info(f"Converted postgres:// to postgresql+asyncpg://")
            return converted

        logger.info(f"No conversion needed, URL starts with: {v[:20]}")
        return v

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
