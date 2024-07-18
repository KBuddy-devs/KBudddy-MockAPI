# --------------------------------------------------------------------------
# pytest의 기본 configuration을 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
import asyncio
import pytest
import pytest_asyncio

from src.core.settings import AppSettings


app_settings = AppSettings(_env_file=".env.test")


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
