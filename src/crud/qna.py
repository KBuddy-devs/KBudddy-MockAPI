# --------------------------------------------------------------------------
# QnA model의 CRUD를 담당하는 메서드를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from typing import Type

from src.helper.exceptions import InternalException, ErrorCode
from src.schemas.qna import QnASchema
from src.helper.global_data import mock_qna_data


def get_mock_qna_data(id: int, response_model: Type[QnASchema]):
    qna_data = next((qna for qna in mock_qna_data if qna["id"] == id), None)
    if qna_data is None:
        raise InternalException(
            message="해당 질문을 찾을 수 없습니다.", error_code=ErrorCode.NOT_FOUND
        )
    return response_model(**qna_data)
