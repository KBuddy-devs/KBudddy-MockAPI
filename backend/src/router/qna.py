# TODO : pydantic 스키마 정의 후 수정
# --------------------------------------------------------------------------
# QnA router을 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from uuid import UUID

from fastapi import APIRouter, status

# from src.crud._base import DeleteResponse
# from src.schemas.qna import QnaResponse, QnaCreate, QnaUpdate

router = APIRouter(
    prefix="/qna",
)


@router.post(
    "/",
    summary="Create a new qna content.",
    status_code=status.HTTP_201_CREATED,
    # response_model=QnaResponse,
)
async def create_qna_route(
    # data: QnaCreate,
):
    pass


@router.get(
    "/{id}",
    summary="Get a qna content.",
    status_code=status.HTTP_200_OK,
    # response_model=QnaResponse,
)
async def get_qna_route(id: UUID):
    pass


@router.patch(
    "/{id}",
    summary="Update a qna content.",
    status_code=status.HTTP_200_OK,
    # response_model=QnaResponse,
)
async def update_qna_route(
    id: UUID,
    # data: QnaUpdate,
):
    pass


@router.delete(
    "/{id}",
    summary="Delete a qna content.",
    status_code=status.HTTP_200_OK,
    # response_model=DeleteResponse,
)
async def delete_qna_route(id: UUID):
    pass
