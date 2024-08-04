# --------------------------------------------------------------------------
# QnA의 testcase를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
import pytest
import pytest_asyncio

from src.helper.global_data import mock_qna_data, mock_comment_data

from test.conftest import BaseTestRouter


@pytest.mark.asyncio
class TestQnAAPI(BaseTestRouter):
    @pytest_asyncio.fixture(autouse=True, scope="function")
    async def setup(self, client):
        mock_qna_data.clear()
        mock_comment_data.clear()
        mock_qna_data.extend(
            [
                {
                    "id": 1,
                    "writerId": "123e4567-e89b-12d3-a456-426614174000",
                    "categoryId": 1,
                    "title": "Test QnA",
                    "description": "Test QnA Description",
                    "viewCount": 0,
                    "createdAt": "2024-07-21T00:00:00.000Z",
                    "modifiedAt": "2024-07-21T00:00:00.000Z",
                    "remove": False,
                    "file": [],
                    "comments": [],
                    "likeCount": 0,
                    "likes": [],
                }
            ]
        )
        mock_comment_data.extend(
            [
                {
                    "id": 1,
                    "userId": "123e4567-e89b-12d3-a456-426614174001",
                    "qnaId": 1,
                    "description": "Test Comment 1",
                    "createdAt": "2024-07-21T01:00:00.000Z",
                },
                {
                    "id": 2,
                    "userId": "123e4567-e89b-12d3-a456-426614174002",
                    "qnaId": 1,
                    "description": "Test Comment 2",
                    "createdAt": "2024-07-21T02:00:00.000Z",
                }
            ]
        )
        mock_qna_data[0]["comments"].extend(mock_comment_data)

    @pytest.mark.asyncio
    async def test_create_qna(self, client):
        # given
        data = {
            "categoryId": 2,
            "title": "New QnA",
            "description": "New QnA Description",
            "file": [],
        }
        headers = {"user_pk": "123e4567-e89b-12d3-a456-426614174001"}

        # when
        response = await client.post("/kbuddy/v1/qna/", json=data, headers=headers)

        # then
        assert response.status_code == 201
        assert response.json()["message"]["title"] == data["title"]
        assert len(mock_qna_data) == 2

    @pytest.mark.asyncio
    async def test_list_qna(self, client):
        # given

        # when
        response = await client.get("/kbuddy/v1/qna/")

        # then
        print(response.json())
        assert response.status_code == 200
        assert response.json()["message"]["count"] == 1

    @pytest.mark.asyncio
    async def test_get_qna(self, client):
        # given

        # when
        response = await client.get("/kbuddy/v1/qna/1")

        # then
        assert response.status_code == 200
        assert response.json()["message"]["title"] == "Test QnA"

    @pytest.mark.asyncio
    async def test_update_qna(self, client):
        # given
        data = {"title": "Updated QnA Title"}
        headers = {"user_pk": "123e4567-e89b-12d3-a456-426614174000"}

        # when
        response = await client.patch("/kbuddy/v1/qna/1", json=data, headers=headers)

        # then
        assert response.status_code == 200
        assert response.json()["message"]["title"] == data["title"]
        assert mock_qna_data[0]["title"] == data["title"]

    @pytest.mark.asyncio
    async def test_delete_qna(self, client):
        # given
        headers = {"user_pk": "123e4567-e89b-12d3-a456-426614174000"}

        # when
        response = await client.delete("/kbuddy/v1/qna/1", headers=headers)

        # then
        assert response.status_code == 204
        assert len(mock_qna_data) == 0

    @pytest.mark.asyncio
    async def test_like_qna(self, client):
        # given
        headers = {"user_pk": "123e4567-e89b-12d3-a456-426614174009"}

        # when
        response = await client.post("/kbuddy/v1/qna/1/like", headers=headers)

        # then
        assert response.status_code == 202
        assert response.json()["message"]["likeCount"] == 1

    @pytest.mark.asyncio
    async def test_unlike_qna(self, client):
        # given
        headers = {"user_pk": "123e4567-e89b-12d3-a456-426614174009"}
        await client.post("/kbuddy/v1/qna/1/like", headers=headers)

        # when
        response = await client.delete("/kbuddy/v1/qna/1/like", headers=headers)

        # then
        assert response.status_code == 202
        assert response.json()["message"]["likeCount"] == 0

    @pytest.mark.asyncio
    async def test_list_comments(self, client):
        # given
        headers = {"user_pk": "123e4567-e89b-12d3-a456-426614174000"}

        # when
        response = await client.get("/kbuddy/v1/qna/1/comment/list?page=1&page_size=10", headers=headers)

        # then
        assert response.status_code == 200
        assert response.json()["message"]["count"] == 2
        assert len(response.json()["message"]["results"]) == 2

    @pytest.mark.asyncio
    async def test_add_comment(self, client):
        # given
        data = {"description": "New Comment"}
        headers = {"user_pk": "123e4567-e89b-12d3-a456-426614174009"}

        # when
        response = await client.post(
            "/kbuddy/v1/qna/1/comment", json=data, headers=headers
        )

        # then
        assert response.status_code == 201
        assert response.json()["message"]["comments"][2]["description"] == data["description"]
        assert len(mock_comment_data) == 3

    @pytest.mark.asyncio
    async def test_update_comment(self, client):
        # given
        mock_comment_data.append({
            "id": 3,
            "userId": "123e4567-e89b-12d3-a456-426614174001",
            "qnaId": 1,
            "description": "Test Comment",
            "remove": False,
            "createdAt": "2024-07-21T00:00:00.000Z",
        })
        mock_qna_data[0]["comments"].append(mock_comment_data[2])
        data = {"description": "Updated Comment"}
        headers = {"user_pk": "123e4567-e89b-12d3-a456-426614174001"}

        # when
        response = await client.patch(f"/kbuddy/v1/qna/1/comment/3", json=data, headers=headers)

        # then
        assert response.status_code == 200
        assert response.json()["message"]["comments"][2]["description"] == data["description"]
        assert mock_comment_data[2]["description"] == data["description"]

    @pytest.mark.asyncio
    async def test_delete_comment(self, client):
        # given
        mock_comment_data.append({
            "id": 3,
            "userId": "123e4567-e89b-12d3-a456-426614174001",
            "qnaId": 1,
            "description": "Test Comment",
            "remove": False,
            "createdAt": "2024-07-21T00:00:00.000Z",
        })
        mock_qna_data[0]["comments"].append(mock_comment_data[2])
        headers = {"user_pk": "123e4567-e89b-12d3-a456-426614174001"}

        # when
        response = await client.delete(f"/kbuddy/v1/qna/1/comment/3", headers=headers)

        # then
        assert response.status_code == 204
        assert len(mock_qna_data[0]["comments"]) == 2
        assert len(mock_comment_data) == 2
