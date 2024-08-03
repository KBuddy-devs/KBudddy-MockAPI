# --------------------------------------------------------------------------
# QnA의 testcase를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
import pytest
import pytest_asyncio

from src.helper.global_data import mock_qna_data

from test.conftest import BaseTestRouter


@pytest.mark.asyncio
class TestQnAAPI(BaseTestRouter):
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, client):
        mock_qna_data.clear()
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
                    "likes": 0,
                }
            ]
        )

    @pytest.mark.asyncio
    async def test_create_qna(self, client):
        # given
        data = {
            "writerId": "123e4567-e89b-12d3-a456-426614174001",
            "categoryId": 2,
            "title": "New QnA",
            "description": "New QnA Description",
            "file": [],
        }

        # when
        response = await client.post("/kbuddy/v1/qna/", json=data)

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

        # when
        response = await client.patch("/kbuddy/v1/qna/1", json=data)

        # then
        assert response.status_code == 200
        assert response.json()["message"]["title"] == data["title"]
        assert mock_qna_data[0]["title"] == data["title"]

    @pytest.mark.asyncio
    async def test_delete_qna(self, client):
        # given

        # when
        response = await client.delete("/kbuddy/v1/qna/1")

        # then
        assert response.status_code == 204
        assert len(mock_qna_data) == 0
