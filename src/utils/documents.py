# --------------------------------------------------------------------------
# OpenAPI generator가 읽을 API 문서 내용을 정의하는 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from typing import Callable

from fastapi import FastAPI


responses = {
    400: {
        "description": "Bad Request",
        "content": {
            "application/json": {"example": {"id": "bar", "value": "The bar tenders"}}
        },
    },
    401: {
        "description": "Unauthorized",
        "content": {
            "application/json": {"example": {"id": "bar", "value": "The bar tenders"}}
        },
    },
    403: {
        "description": "Forbidden",
        "content": {
            "application/json": {"example": {"id": "bar", "value": "The bar tenders"}}
        },
    },
    404: {
        "description": "Not Found",
        "content": {
            "application/json": {"example": {"id": "bar", "value": "The bar tenders"}}
        },
    },
}


def customize_openapi(func: Callable[..., dict]) -> Callable[..., dict]:
    """Customize OpenAPI schema for remove 422 status OpenAPI docs object"""

    def wrapper(*args, **kwargs) -> dict:
        """Wrapper."""
        res = func(*args, **kwargs)
        for _, method_item in res.get("paths", {}).items():
            for _, param in method_item.items():
                responses = param.get("responses")
                # remove default 422 schema - HTTPValidationError
                if "422" in responses and responses["422"]["content"][
                    "application/json"
                ]["schema"]["$ref"].endswith("HTTPValidationError"):
                    del responses["422"]
        return res

    return wrapper


def add_description_at_api_tags(app: FastAPI):
    tag_descriptions = {
        "user": "(유지보수 작업중, 사용 X) User API. 회원 로그인, 로그아웃, 정보 조회 및 수정 등을 수행합니다.",
        "qna": "QnA API. 질문 및 댓글 컨텐츠를 생성, 수정, 조회, 삭제할 수 있으며 좋아요 동작을 수행합니다.",
    }

    # OpenAPI 태그별 description 생성
    openapi_tags = [
        {"name": tag, "description": desc} for tag, desc in tag_descriptions.items()
    ]

    if app.openapi_tags:
        app.openapi_tags.extend(openapi_tags)
    else:
        app.openapi_tags = openapi_tags
