from httpx import AsyncClient


async def test_root(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {}


async def test_user(client: AsyncClient):
    response = await client.post(
        "/users/alternative",
        json={"username": "e2e_test_user"},
    )
    assert response.status_code == 200
    assert isinstance(response.json().get("user_id"), int)
