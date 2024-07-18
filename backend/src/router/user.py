# TODO : pydantic 스키마 정의 후 수정
# --------------------------------------------------------------------------
# User router을 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from uuid import UUID

from fastapi import APIRouter, status, Depends

# from src.crud._base import DeleteResponse
# from src.schemas.user import UserResponse, UserCreate, UserUpdate

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
    summary="Get a user.",
    status_code=status.HTTP_200_OK,
    # response_model=UserResponse,
)
async def get_user_route(id: UUID):
    pass


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
