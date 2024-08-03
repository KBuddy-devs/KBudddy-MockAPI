# TODO : pydantic 스키마 정의 후 수정
# --------------------------------------------------------------------------
# QnA router을 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from . import *

from src.schemas import ResponseSchema

# from src.crud._base import DeleteResponse
from src import mock_qna_data
from src.crud.qna import get_mock_qna_data
from src.schemas.qna import QnASchema, QnACreate, QnAUpdate

router = APIRouter(
    prefix="/qna",
)


def generate_new_id():
    if mock_qna_data:
        return max(_qna['id'] for _qna in mock_qna_data) + 1
    return 1


@router.post(
    "/",
    summary="Create a new qna content.",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseSchema[QnASchema],
)
async def create_qna_route(data: QnACreate, request: Request):
    # TODO : 임시방편 - new_qna Payload를 QnASchema로 파싱하도록 로직 개선
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
        message=new_qna
    )
    return response


@router.get(
    "/{id}",
    summary="Get a qna content.",
    status_code=status.HTTP_200_OK,
    response_model=ResponseSchema[QnASchema],
)
async def get_qna_route(id: int, request: Request):
    try:
        user_message = get_mock_qna_data(id, QnASchema)
        response = ResponseSchema(
            timestamp=datetime.utcnow().isoformat() + "Z",
            status=200,
            code="KB-HTTP-200",
            path=str(request.url),
            message=user_message,
        )
        print(mock_qna_data)  # for debugging
        return response
    except InternalException as e:
        return JSONResponse(
            status_code=e.status,
            content=e.to_response(path=str(request.url)).model_dump(),
        )


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
