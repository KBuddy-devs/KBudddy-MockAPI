# --------------------------------------------------------------------------
# User의 testcase를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
import pytest
import pytest_asyncio

from test.conftest import BaseTestRouter


@pytest.mark.asyncio
class TestUserAPI(BaseTestRouter):
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, client):
        from uuid import UUID

        self.MOCK_USER_ID = UUID("123e4567-e89b-12d3-a456-426614174000")
        self.INVALID_USER_ID = UUID("123e4567-e89b-12d3-a456-426614174999")

    async def test_get_user(self, client):
        # given
        user_id = self.MOCK_USER_ID

        # when
        response = await client.get(f"/kbuddy/v1/user/{user_id}")

        # then
        assert response.status_code == 200
        json_response = response.json()
        assert json_response["status"] == 200
        assert json_response["code"] == "KB-HTTP-200"
        assert json_response["message"]["id"] == str(user_id)

    async def test_get_user_not_found(self, client):
        # given
        user_id = self.INVALID_USER_ID

        # when
        response = await client.get(f"/kbuddy/v1/user/{user_id}")

        # then
        assert response.status_code == 404
        json_response = response.json()
        assert json_response["status"] == 404
        assert json_response["code"] == "KB-HTTP-002"
        assert "ERROR : 해당 유저를 찾을 수 없습니다." in json_response["message"]


#     async def test_create_user(self, client):
#         # given
#         data = {"email": "test@example.com", "password": "password"}
#
#         # when
#         response = await client.post("/users/", json=data)
#
#         # then
#         assert response.status_code == 201
#         assert response.json()["email"] == data["email"]
