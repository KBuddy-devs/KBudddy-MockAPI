# TODO : User router도 동일하게 적용
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
mock_comment_data = []


def initialize_mock_qna_data():
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    qna_file_path = os.path.join(base_path, "src", "mocks", "mock_qnas.json")
    comment_file_path = os.path.join(base_path, "src", "mocks", "mock_comments.json")
    like_file_path = os.path.join(base_path, "src", "mocks", "mock_likes.json")

    with open(qna_file_path, "r", encoding="utf-8") as f:
        qna_data = json.load(f)

    with open(comment_file_path, "r", encoding="utf-8") as f:
        comment_data = json.load(f)

    with open(like_file_path, "r", encoding="utf-8") as f:
        like_data = json.load(f)

    # Map comments to their respective QnA
    comment_map = {}
    for comment in comment_data:
        qna_id = comment["qnaId"]
        if qna_id not in comment_map:
            comment_map[qna_id] = []
        comment_map[qna_id].append(comment)

    # Map likes to their respective QnA
    like_map = {}
    for like in like_data:
        qna_id = like["qnaId"]
        if qna_id not in like_map:
            like_map[qna_id] = []
        like_map[qna_id].append(like)

    for qna in qna_data:
        qna_id = qna["id"]
        qna["comments"] = comment_map.get(qna_id, [])
        qna["likes"] = like_map.get(qna_id, [])
        qna["likeCount"] = len(qna["likes"])

    mock_qna_data.extend(qna_data)
