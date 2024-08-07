FROM python:3.11.1
LABEL authors="bnbong"

# Setup working directory
WORKDIR /src
COPY . /src

# Setup Virtual ENV
RUN pip install poetry
COPY pyproject.toml poetry.lock ./

# Runners
RUN poetry install --no-root
ENV TZ=Asia/Seoul

EXPOSE 9080

ENTRYPOINT poetry run uvicorn main:app --host=0.0.0.0 --port=9080 --reload