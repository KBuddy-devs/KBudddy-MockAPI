# --------------------------------------------------------------------------
# Backend Application의 설정을 관리하는 파일입니다.
#
# 실제 환경에서는 .env 파일을 통해 설정을 관리하며,
# 테스트 환경에서는 .env.test 파일을 통해 설정을 관리합니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from __future__ import annotations

import warnings

from typing import Any, Optional, Annotated, Literal
from typing_extensions import Self

from pydantic import (
    Field,
    AnyUrl,
    BeforeValidator,
    model_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    LOGGING_DEBUG_LEVEL: bool = Field(
        default=True,
        description="True: DEBUG mode, False:: INFO mode",
    )
    LOG_FILE_PATH: str = Field(
        default="../../logs/app.log",
        description="Log file path",
    )
    DEBUG_ALLOW_CORS_ALL_ORIGIN: bool = Field(
        default=True,
        description="If True, allow origins for CORS requests.",
    )
    DEBUG_ALLOW_NON_CERTIFICATED_USER_GET_TOKEN: bool = Field(
        default=True,
        description="If True, allow non-cerficiated users to get ESP token.",
    )
    BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = (
        []
    )

    THREAD_POOL_SIZE: Optional[int] = Field(
        default=10,
        description="Change the server's thread pool size to handle non-async function",
    )

    SECRET_KEY: str = Field(
        default="example_secret_key_WoW",
        description="Secret key to be used for issuing HMAC tokens.",
    )
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    SERVER_DOMAIN: str = Field(
        default="localhost",
        description="Domain of server",
    )
    SERVER_PORT: int = Field(
        default=9080,
        description="Server's port",
    )

    HASH_ALGORITHM: str = Field(default="HS256", description="Algorithm for Hashing")
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        if value == "example_secret_key_WoW":
            message = (
                f'The value of {var_name} is "example_secret_key_WoW", '
                "for security, please change it, at least for deployments."
            )
            if self.ENVIRONMENT == "local":
                warnings.warn(message, stacklevel=1)
            else:
                raise ValueError(message)

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        self._check_default_secret("SECRET_KEY", self.SECRET_KEY)

        return self


settings = AppSettings()
