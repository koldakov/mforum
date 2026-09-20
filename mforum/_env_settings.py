from typing import TYPE_CHECKING, Any

from dotenv import load_dotenv
from pydantic import PostgresDsn, SecretStr
from pydantic_settings import (
    BaseSettings,
    EnvSettingsSource,
    PydanticBaseSettingsSource,
)

if TYPE_CHECKING:
    from pydantic.fields import FieldInfo

# Populate os.environ from a local .env before Settings() reads it below.
# Existing environment variables always take precedence (see python-dotenv docs).
load_dotenv()


class _EnvSource(EnvSettingsSource):
    def prepare_field_value(
        self,
        field_name: str,
        field: FieldInfo,
        value: Any,
        value_is_complex: bool,
    ) -> Any:
        if field_name == "allowed_hosts":
            if not value:
                raise ValueError(f"{field_name} is a mandatory ENV variable.")
            return [str(x).strip() for x in value.split(",")]

        return super().prepare_field_value(field_name, field, value, value_is_complex)


class Settings(BaseSettings):
    secret_key: SecretStr
    database_url: PostgresDsn
    allowed_hosts: list[str]

    debug: bool = False
    admin_url: SecretStr = SecretStr("admin/")
    site_url: str = "/"

    # DB settings.
    db_conn_max_age: int = 0
    db_conn_health_checks: bool = True

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (_EnvSource(settings_cls),)


env_settings: Settings = Settings()


class FeatureFlags(BaseSettings):
    force_https: bool = False


feature_flags: FeatureFlags = FeatureFlags()
