# TODO : pydantic 파싱 공통 로직 정의
# --------------------------------------------------------------------------
# 기본 Model CRUD 메서드를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from __future__ import annotations

import json

from typing import Any, Type, List, Optional

from pydantic import BaseModel


def load_json(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
