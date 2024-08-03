# --------------------------------------------------------------------------
# User model의 CRUD를 담당하는 메서드를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
import os
import json
from typing import Type
from uuid import UUID

from src.helper.exceptions import InternalException, ErrorCode
from src.schemas.user import UserSchema

from ._base import load_json


def get_mock_user_data(id: UUID, response_model: Type[UserSchema]):
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    file_path = os.path.join(base_path, "src", "mocks", "mock_users.json")
    users = load_json(file_path)
    user_data = next((user for user in users if user["id"] == str(id)), None)
    if user_data is None:
        raise InternalException(
            message="해당 유저를 찾을 수 없습니다.", error_code=ErrorCode.NOT_FOUND
        )
    return response_model(**user_data)
