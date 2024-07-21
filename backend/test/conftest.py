# --------------------------------------------------------------------------
# pytest의 기본 configuration을 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
import pytest_asyncio

from httpx import AsyncClient, ASGITransport

from src import create_app
from src.core.settings import AppSettings


app_settings = AppSettings(_env_file=".env.test")


class BaseTestRouter:
    @pytest_asyncio.fixture(scope="function")
    async def client(self):
        app = create_app(app_settings)
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
            yield c