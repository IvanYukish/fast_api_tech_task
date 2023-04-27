import pytest
from fastapi.testclient import TestClient
from mongomock_motor import AsyncMongoMockClient

from app.core.db import get_db
from main import app

test_client = TestClient(app)


async def get_test_db():
    return AsyncMongoMockClient().get_database("mongo_tech")


app.dependency_overrides[get_db] = get_test_db


def test_get_users_is_empty():
    response = test_client.get("api/v1/users")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.parametrize(
    "test_input,expected", [
        (
                {
                    "first_name": "John",
                    "last_name": "Doe",
                    "role": "simple mortal",
                    "is_active": "false",
                    "created_at": "datetime",
                    "last_login": "datetime",
                    "password": "fakehashedsecret",
                },
                {
                    "first_name": "John",
                    "last_name": "Doe",
                    "role": "simple mortal",
                    "is_active": "false",
                    "created_at": "datetime",
                    "last_login": "datetime",
                }
        )
    ]
)
@pytest.mark.asyncio
async def test_create_user(test_input, expected):
    fake_db = await get_test_db()
    collection = fake_db["users"]

    response = test_client.post("api/v1/users", json=test_input)
    assert response.status_code == 201
    assert response.json()["first_name"] == expected["first_name"]
    assert response.json()["last_name"] == expected["last_name"]
    assert response.json()["hashed_pass"]
    assert not response.json().get("password")

    result = await collection.insert_one(test_input)
    assert result.inserted_id
    response = test_client.get("api/v1/users")
    assert response.status_code == 200
    assert len(await collection.find({}).to_list(None)) == 1
