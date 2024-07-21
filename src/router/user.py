# --------------------------------------------------------------------------
# User router을 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse

from src.crud.user import get_mock_user_data
from src.helper.exceptions import InternalException
from src.schemas import ResponseSchema
from src.schemas.user import UserSchema


router = APIRouter(
    prefix="/user",
)


@router.post(
    "/",
    summary="Create a new user.",
    status_code=status.HTTP_201_CREATED,
    # response_model=UserResponse,
)
async def create_user_route(
    # data: UserCreate,
):
    pass


@router.get(
    "/{id}",
    summary="단일 유저 정보 조회",
    description="특정 유저에 대한 정보를 조회합니다.",
    response_model=ResponseSchema[UserSchema],
)
async def get_user_route(id: UUID, request: Request):
    try:
        user_message = get_mock_user_data(id, UserSchema)
        response = ResponseSchema(
            timestamp=datetime.utcnow().isoformat() + "Z",
            status=200,
            code="KB-HTTP-200",
            path=str(request.url),
            message=user_message,
        )
        return response
    except InternalException as e:
        return JSONResponse(
            status_code=e.status, content=e.to_response(path=str(request.url)).model_dump()
        )


@router.patch(
    "/{id}",
    summary="Update a user.",
    status_code=status.HTTP_200_OK,
    # response_model=UserResponse,
)
async def update_user_route(
    id: UUID,
    # data: UserUpdate,
):
    pass


@router.delete(
    "/{id}",
    summary="Delete a user.",
    status_code=status.HTTP_200_OK,
    # response_model=DeleteResponse,
)
async def delete_user_route(id: UUID):
    pass
