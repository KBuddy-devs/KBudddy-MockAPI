# --------------------------------------------------------------------------
# Base response schemas를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from pydantic import BaseModel, Field
from typing import Generic, TypeVar

T = TypeVar("T")


class ResponseSchema(BaseModel, Generic[T]):
    timestamp: str = Field(
        ...,
        description="응답이 생성된 시간입니다.",
    )
    status: int = Field(..., description="HTTP 상태 코드입니다.")
    code: str = Field(
        ...,
        description="서버 식별 코드입니다.",
    )
    path: str = Field(
        ...,
        description="요청 경로입니다.",
    )
    message: T = Field(
        ...,
        description="요청한 데이터 상세 혹은 에러 메시지입니다.",
    )

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "timestamp": "2023-02-10T01:00:00.000Z",
                "status": 200,
                "code": "KB-HTTP-200",
                "path": "/v1/<some/endpoint>",
                "message": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "email": "example@example.com",
                    "password": "secret",
                    "nickname": "example_nick",
                    "create_at": "2023-02-10T01:00:00.000Z",
                    "bio": "example bio",
                    "point": 100,
                    "profile_img": "https://example.com/profile.jpg",
                    "first_name": "John",
                    "last_name": "Doe",
                },
            }
        }
