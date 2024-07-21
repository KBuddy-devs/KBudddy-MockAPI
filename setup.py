# --------------------------------------------------------------------------
# Backend Application의 패키지 정보를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from setuptools import setup, find_packages

install_requires = [
    # Main Application Dependencies
    "fastapi==0.111.1",
    "uvicorn==0.30.1",
    "httpx==0.27.0",
    # ORM Dependencies
    "pydantic==2.8.2",
    "pydantic_core==2.20.1",
    "pydantic-settings==2.3.4",
    # Utility Dependencies
    "starlette==0.37.2",
    "typing_extensions==4.12.2",
    "watchfiles==0.22.0",
    "pytest==8.2.2",
    "pytest-asyncio==0.23.8",
]

# IDE will watch this setup config through your project src, and help you to set up your environment
setup(
    name="KBuddy-MockAPI",
    description="Mock API server for test",
    author="bnbong",
    author_email="bbbong9@gmail.com",
    packages=find_packages(where="src"),
    use_scm_version=True,
    requires=["python (>=3.11)"],
    install_requires=install_requires,
)
