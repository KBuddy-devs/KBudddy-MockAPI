# --------------------------------------------------------------------------
# QnA router을 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from fastapi import Query

from . import *

from src.schemas import ResponseSchema

from src import mock_qna_data
from src.crud.qna import get_mock_qna_data_schema, get_mock_qna_data
from src.schemas.qna import QnASchema, QnACreate, QnAUpdate
from src.helper.pagination import PaginatedResponse, paginate

router = APIRouter(
    prefix="/qna",
)


def generate_new_id():
    if mock_qna_data:
        return max(_qna['id'] for _qna in mock_qna_data) + 1
    return 1


@router.post(
    "/",
    summary="단일 질문 등록",
    description="특정 질문을 생성합니다.",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseSchema[QnASchema],
)
async def create_qna_route(data: QnACreate, request: Request):
    new_qna = {
        "id": generate_new_id(),
        "writerId": data.writerId,
        "categoryId": data.categoryId,
        "title": data.title,
        "description": data.description,
        "viewCount": 0,
        "createdAt": datetime.utcnow().isoformat() + "Z",
        "modifiedAt": datetime.utcnow().isoformat() + "Z",
        "remove": False,
        "file": data.file,
        "comments": [],
        "likes": 0
    }
    mock_qna_data.append(new_qna)
    response = ResponseSchema(
        timestamp=datetime.utcnow().isoformat() + "Z",
        status=201,
        code="KB-HTTP-201",
        path=str(request.url),
        message=QnASchema(**new_qna)
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
        message=paginated_response
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
    response_model=ResponseSchema[QnASchema]
)
async def update_qna_route(id: int, data: QnAUpdate, request: Request):
    try:
        qna = get_mock_qna_data(id)
        qna.update(data.dict(exclude_unset=True))
        qna["modifiedAt"] = datetime.utcnow().isoformat() + "Z"
        mock_qna_data[mock_qna_data.index(qna)] = qna
        response = ResponseSchema(
            timestamp=datetime.utcnow().isoformat() + "Z",
            status=200,
            code="KB-HTTP-200",
            path=str(request.url),
            message=QnASchema(**qna)
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
async def delete_qna_route(id: int, request: Request):
    try:
        qna = get_mock_qna_data(id)
        mock_qna_data.remove(qna)
        response = ResponseSchema(
            timestamp=datetime.utcnow().isoformat() + "Z",
            status=204,
            code="KB-HTTP-204",
            path=str(request.url),
            message={"detail": "QnA deleted successfully"}
        )
        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content=response.dict()
        )
    except InternalException as e:
        return JSONResponse(
            status_code=e.status,
            content=e.to_response(path=str(request.url)).model_dump(),
        )
