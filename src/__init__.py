# --------------------------------------------------------------------------
# FastAPI Application을 생성하는 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from __future__ import annotations

import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from setuptools_scm import get_version

from src.core.settings import settings
from src.helper.exceptions import InternalException
from src.helper.logging import init_logger as _init_logger
from src.router import router
from src.core.settings import AppSettings
from src.utils.documents import add_description_at_api_tags

__version__ = get_version(
    root="../", relative_to=__file__
)  # .git이 있는 폴더를 가리켜야함.


logger = logging.getLogger(__name__)


def init_logger(app_settings: AppSettings) -> None:
    _init_logger(f"fastapi-backend@{__version__}", app_settings)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Application startup")
        yield
    finally:
        logger.info("Application shutdown")


def create_app(app_settings: AppSettings) -> FastAPI:
    app = FastAPI(
        title="KBuddy Mock API",
        description="KBuddy의 Mock 데이터 API 서버 입니다.",
        version=__version__,
        lifespan=lifespan,
        openapi_url="/openapi.json",
        redoc_url="/redoc",
    )

    # Apply Middlewares
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[
                str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
            ],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Apply Custom Exception Handler
    @app.exception_handler(InternalException)
    async def internal_exception_handler(request: Request, exc: InternalException):
        return JSONResponse(
            status_code=exc.status,
            content=exc.to_response(path=str(request.url)).model_dump(),
        )

    app.include_router(router)

    add_description_at_api_tags(app)

    return app
