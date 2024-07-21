# TODO : qna 라우터 완성 후 연결
# --------------------------------------------------------------------------
# Backend Application과 router을 연결하는 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
import json

from fastapi import APIRouter

from .user import router as user_router

router = APIRouter(prefix="/kbuddy/v1")

router.include_router(user_router, tags=["user"])


@router.get(
    "/ping",
    summary="Server health check",
    description="FastAPI 서버가 정상적으로 동작하는지 확인합니다.",
    response_model=dict,
    responses={
        200: {
            "description": "Ping Success",
            "content": {"application/json": {"example": {"ping": "pong"}}},
        },
    },
)
async def ping():
    return {"ping": "pong"}


def load_json(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
