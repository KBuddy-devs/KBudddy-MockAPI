# --------------------------------------------------------------------------
# Backend Application의 Exception class를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from enum import Enum
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from src.schemas import ResponseSchema


class ErrorCode(Enum):
    # HTTP
    BAD_REQUEST = ("BAD_REQUEST", "KB-HTTP-001", 400)
    NOT_FOUND = ("NOT_FOUND", "KB-HTTP-002", 404)
    METHOD_NOT_ALLOWED = ("METHOD_NOT_ALLOWED", "KB-HTTP-003", 405)
    NOT_ACCESSABLE = ("NOT_ACCESSABLE", "KB-HTTP-004", 406)
    TIMEOUT = ("TIMEOUT", "KB-HTTP-005", 408)
    UNPROCESSABLE = ("UNPROCESSABLE", "KB-HTTP-006", 422)
    TOO_MANY_REQUEST = ("TOO_MANY_REQUEST", "KB-HTTP-007", 429)

    # DATA
    CONFLICT = ("CONFLICT", "KB-DATA-001", 409)

    # AUTH
    UNAUTHORIZED = ("UNAUTHORIZED", "KB-AUTH-001", 401)
    FORBIDDEN = ("FORBIDDEN", "KB-AUTH-002", 403)

    # SERVER
    UNKNOWN_ERROR = ("UNKNOWN_ERROR", "KB-SEVR-001", 500)
    BAD_GATEWAY = ("BAD_GATEWAY", "KB-SEVR-002", 502)
    SERVICE_UNAVAILABLE = ("SERVICE_UNAVAILABLE", "KB-SEVR-003", 503)
    GATEWAY_TIMEOUT = ("GATEWAY_TIMEOUT", "KB-SEVR-004", 504)

    def __init__(self, error: str, code: str, status_code: int):
        self.error = error
        self.code = code
        self.status_code = status_code


class ExceptionSchema(BaseModel):
    timestamp: str = Field(
        ...,
        description="에러가 발생한 시간입니다.",
    )
    status: int = Field(..., description="에러의 HTTP status code 입니다.")
    code: str = Field(
        ...,
        description="에러의 서버 식별 코드입니다.",
    )
    message: str = Field(
        ...,
        description="에러의 메시지 내용입니다.",
    )
    path: str = Field(
        ...,
        description="에러가 발생한 경로입니다.",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "timestamp": "2023-02-10T01:00:00.000Z",
                    "status": 500,
                    "code": "KB-SEVR-000",
                    "path": "/v1/<some/endpoint>",
                    "message": "ERROR : 서버 로직에 알 수 없는 오류가 발생했습니다.",
                },
                {
                    "timestamp": "2023-02-10T01:00:00.000Z",
                    "status": 400,
                    "code": "KB-HTTP-001",
                    "path": "/v1/<some/endpoint>",
                    "message": "ERROR : 잘못된 요청입니다.",
                },
                {
                    "timestamp": "2023-02-10T01:00:00.000Z",
                    "status": 401,
                    "code": "KB-AUTH-001",
                    "path": "/v1/<some/endpoint>",
                    "message": "ERROR : 헤더에서 유저 정보를 찾을 수 없습니다.",
                },
                {
                    "timestamp": "2023-02-10T01:00:00.000Z",
                    "status": 403,
                    "code": "KB-AUTH-002",
                    "path": "/v1/<some/endpoint>",
                    "message": "ERROR : 권한이 없는 헤더 유저입니다.",
                },
                {
                    "timestamp": "2023-02-10T01:00:00.000Z",
                    "status": 404,
                    "code": "KB-HTTP-002",
                    "path": "/v1/<some/endpoint>",
                    "message": "ERROR : 해당 리소스를 찾을 수 없습니다.",
                },
            ]
        }
    )


class InternalException(Exception):
    def __init__(self, message: str, error_code: ErrorCode):
        self.timestamp = datetime.utcnow().isoformat() + "Z"
        self.status = error_code.status_code
        self.error_code = error_code.code
        self.message = f"ERROR : {message}"

    def to_response(self, path: str) -> ResponseSchema[str]:
        return ResponseSchema(
            timestamp=self.timestamp,
            status=self.status,
            code=self.error_code,
            path=path,
            message=self.message,
        )
