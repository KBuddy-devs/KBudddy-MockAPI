# TODO : UUID 판별 로직 추가
# --------------------------------------------------------------------------
# 헤더 관련 로직을 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from logging import getLogger

from fastapi import Header

from src.helper.exceptions import InternalException, ErrorCode

log = getLogger(__name__)


async def check_user(
    user_pk: str = Header(
        None, description="사용자의 고유 식별자입니다.", convert_underscores=False
    ),
) -> str:
    if not user_pk:
        raise InternalException("사용자 정보가 없습니다.", ErrorCode.BAD_REQUEST)

    return user_pk
