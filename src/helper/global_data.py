# TODO : User router도 동일하게 적용, QnA 나머지 router에도 적용
# --------------------------------------------------------------------------
# FastAPI coroutine에 Mocking Data storage로 사용할
# 전역 리스트를 선언, 할당하는 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
import os
import json

# Global Mock Data storage (Stores : FastAPI app coroutine - In FastAPI thread memory)
mock_qna_data = []
mock_user_data = []


def initialize_mock_qna_data():
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    file_path = os.path.join(base_path, "src", "mocks", "mock_qnas.json")
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    mock_qna_data.extend(data)
