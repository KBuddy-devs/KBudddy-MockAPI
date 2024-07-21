# TODO : QnA 스키마 필드 정의
# --------------------------------------------------------------------------
# QnA schemas를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from datetime import datetime, date
from uuid import UUID
from enum import Enum

from pydantic import field_serializer
from typing import Optional, List
