# --------------------------------------------------------------------------
# QnA router을 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from fastapi import Query, Depends

from . import *

from src.schemas import ResponseSchema

from src import mock_qna_data, mock_comment_data
from src.crud.qna import get_mock_qna_data_schema, get_mock_qna_data
from src.schemas.qna import (
    QnASchema,
    QnACreate,
    QnAUpdate,
    CommentUpdate,
    CommentCreate,
)
from src.helper.pagination import PaginatedResponse, paginate
from src.helper.exceptions import ErrorCode
from ._check import check_user


router = APIRouter(
    prefix="/qna",
)


def generate_new_qna_id():
    if mock_qna_data:
        return max(_qna["id"] for _qna in mock_qna_data) + 1
    return 1


def generate_new_comment_id():
    if mock_comment_data:
        return max(_comment["id"] for _comment in mock_comment_data) + 1
    return 1


@router.post(
    "/",
    summary="단일 질문 등록",
    description="특정 질문을 생성합니다.",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseSchema[QnASchema],
)
async def create_qna_route(
    data: QnACreate, request: Request, request_user: str = Depends(check_user)
):
    new_qna = {
        "id": generate_new_qna_id(),
        "writerId": request_user,
        "categoryId": data.categoryId,
        "title": data.title,
        "description": data.description,
        "viewCount": 0,
        "createdAt": datetime.utcnow().isoformat() + "Z",
        "modifiedAt": datetime.utcnow().isoformat() + "Z",
        "remove": False,
        "file": data.file,
        "comments": [],
        "likeCount": 0,
        "likes": [],
    }
    mock_qna_data.append(new_qna)
    response = ResponseSchema(
        timestamp=datetime.utcnow().isoformat() + "Z",
        status=201,
        code="KB-HTTP-201",
        path=str(request.url),
        message=QnASchema(**new_qna),
    )
    return response


@router.get(
    "/",
    summary="다수 질문 조회",
    description="여러 개의 질문 리스트를 조회합니다.",
    status_code=status.HTTP_200_OK,
    response_model=ResponseSchema[PaginatedResponse[QnASchema]],
)
async def list_qna_route(
    request: Request,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
):
    paginated_response = paginate(mock_qna_data, page, page_size, request)
    response = ResponseSchema(
        timestamp=datetime.utcnow().isoformat() + "Z",
        status=200,
        code="KB-HTTP-200",
        path=str(request.url),
        message=paginated_response,
    )
    return response


@router.get(
    "/{id}",
    summary="단일 질문 조회",
    description="특정 질문에 대한 정보를 조회합니다.",
    status_code=status.HTTP_200_OK,
    response_model=ResponseSchema[QnASchema],
)
async def get_qna_route(id: int, request: Request):
    try:
        user_message = get_mock_qna_data_schema(id, QnASchema)
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
            status_code=e.status,
            content=e.to_response(path=str(request.url)).model_dump(),
        )


@router.patch(
    "/{id}",
    summary="단일 질문 정보 수정",
    description="특정 질문에 대한 정보를 수정합니다.",
    status_code=status.HTTP_200_OK,
    response_model=ResponseSchema[QnASchema],
)
async def update_qna_route(
    id: int, data: QnAUpdate, request: Request, request_user: str = Depends(check_user)
):
    try:
        qna = get_mock_qna_data(id)
        if qna["writerId"] != request_user:
            raise InternalException(
                message="수정 권한이 없습니다.", error_code=ErrorCode.UNAUTHORIZED
            )
        qna.update(data.dict(exclude_unset=True))
        qna["modifiedAt"] = datetime.utcnow().isoformat() + "Z"
        mock_qna_data[mock_qna_data.index(qna)] = qna
        response = ResponseSchema(
            timestamp=datetime.utcnow().isoformat() + "Z",
            status=200,
            code="KB-HTTP-200",
            path=str(request.url),
            message=QnASchema(**qna),
        )
        return response
    except InternalException as e:
        return JSONResponse(
            status_code=e.status,
            content=e.to_response(path=str(request.url)).model_dump(),
        )


@router.delete(
    "/{id}",
    summary="단일 질문 삭제",
    description="특정 질문을 삭제합니다.",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_qna_route(
    id: int, request: Request, request_user: str = Depends(check_user)
):
    try:
        qna = get_mock_qna_data(id)
        if qna["writerId"] != request_user:
            raise InternalException(
                message="삭제 권한이 없습니다.", error_code=ErrorCode.UNAUTHORIZED
            )
        mock_qna_data.remove(qna)
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content="")
    except InternalException as e:
        return JSONResponse(
            status_code=e.status,
            content=e.to_response(path=str(request.url)).model_dump(),
        )


@router.post(
    "/{id}/like",
    summary="단일 질문 좋아요",
    description="특정 질문에 좋아요를 표시합니다.",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=ResponseSchema[QnASchema],
)
async def like_qna_route(
    id: int, request: Request, request_user: str = Depends(check_user)
):
    try:
        qna = get_mock_qna_data(id)
        if not any(like["userId"] == request_user for like in qna["likes"]):
            qna["likes"].append({"userId": request_user})
            qna["likeCount"] += 1
        mock_qna_data[mock_qna_data.index(qna)] = qna
        response = ResponseSchema(
            timestamp=datetime.utcnow().isoformat() + "Z",
            status=202,
            code="KB-HTTP-202",
            path=str(request.url),
            message=QnASchema(**qna),
        )
        return response
    except InternalException as e:
        return JSONResponse(
            status_code=e.status,
            content=e.to_response(path=str(request.url)).model_dump(),
        )


@router.delete(
    "/{id}/like",
    summary="단일 질문 좋아요 취소",
    description="특정 질문에 대한 좋아요를 취소합니다.",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=ResponseSchema[QnASchema],
)
async def unlike_qna_route(
    id: int, request: Request, request_user: str = Depends(check_user)
):
    try:
        qna = get_mock_qna_data(id)
        if any(like["userId"] == request_user for like in qna["likes"]):
            qna["likes"] = [
                like for like in qna["likes"] if like["userId"] != request_user
            ]
            qna["likeCount"] -= 1
        mock_qna_data[mock_qna_data.index(qna)] = qna
        response = ResponseSchema(
            timestamp=datetime.utcnow().isoformat() + "Z",
            status=202,
            code="KB-HTTP-202",
            path=str(request.url),
            message=QnASchema(**qna),
        )
        return response
    except InternalException as e:
        return JSONResponse(
            status_code=e.status,
            content=e.to_response(path=str(request.url)).model_dump(),
        )


@router.post(
    "/{id}/comment",
    summary="단일 질문에 댓글 추가",
    description="특정 질문에 댓글을 추가합니다.",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseSchema[QnASchema],
)
async def add_comment_route(
    id: int,
    data: CommentCreate,
    request: Request,
    request_user: str = Depends(check_user),
):
    try:
        qna = get_mock_qna_data(id)
        new_comment = {
            "id": generate_new_comment_id(),
            "userId": request_user,
            "qnaId": id,
            "description": data.description,
            "remove": False,
            "createdAt": datetime.utcnow().isoformat() + "Z",
        }
        qna["comments"].append(new_comment)
        mock_comment_data.append(new_comment)
        mock_qna_data[mock_qna_data.index(qna)] = qna
        response = ResponseSchema(
            timestamp=datetime.utcnow().isoformat() + "Z",
            status=201,
            code="KB-HTTP-201",
            path=str(request.url),
            message=QnASchema(**qna),
        )
        return response
    except InternalException as e:
        return JSONResponse(
            status_code=e.status,
            content=e.to_response(path=str(request.url)).model_dump(),
        )


@router.patch(
    "/{qna_id}/comment/{comment_id}",
    summary="단일 댓글 수정",
    description="특정 질문에 대한 댓글을 수정합니다.",
    status_code=status.HTTP_200_OK,
    response_model=ResponseSchema[QnASchema],
)
async def update_comment_route(
    qna_id: int,
    comment_id: int,
    data: CommentUpdate,
    request: Request,
    request_user: str = Depends(check_user),
):
    try:
        qna = get_mock_qna_data(qna_id)
        comment = next((c for c in qna["comments"] if c["id"] == comment_id), None)
        if comment is None or comment["userId"] != request_user:
            raise InternalException(
                message="해당 댓글을 찾을 수 없거나 권한이 없습니다.",
                error_code=ErrorCode.NOT_FOUND,
            )
        comment.update(data.dict(exclude_unset=True))
        mock_comment_data[mock_comment_data.index(comment)] = comment
        mock_qna_data[mock_qna_data.index(qna)] = qna
        response = ResponseSchema(
            timestamp=datetime.utcnow().isoformat() + "Z",
            status=200,
            code="KB-HTTP-200",
            path=str(request.url),
            message=QnASchema(**qna),
        )
        return response
    except InternalException as e:
        return JSONResponse(
            status_code=e.status,
            content=e.to_response(path=str(request.url)).model_dump(),
        )


@router.delete(
    "/{qna_id}/comment/{comment_id}",
    summary="단일 댓글 삭제",
    description="특정 질문에 대한 댓글을 삭제합니다.",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_comment_route(
    qna_id: int,
    comment_id: int,
    request: Request,
    request_user: str = Depends(check_user),
):
    try:
        qna = get_mock_qna_data(qna_id)
        comment = next((c for c in qna["comments"] if c["id"] == comment_id), None)
        if comment is None or comment["userId"] != request_user:
            raise InternalException(
                message="해당 댓글을 찾을 수 없거나 권한이 없습니다.",
                error_code=ErrorCode.NOT_FOUND,
            )
        qna["comments"] = [c for c in qna["comments"] if c["id"] != comment_id]
        mock_comment_data.remove(comment)
        mock_qna_data[mock_qna_data.index(qna)] = qna
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content="")
    except InternalException as e:
        return JSONResponse(
            status_code=e.status,
            content=e.to_response(path=str(request.url)).model_dump(),
        )
