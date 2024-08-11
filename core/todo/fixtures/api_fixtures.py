import pytest
from rest_framework.test import APIClient

from accounts.models import User
from ..models import Todo

@pytest.fixture
def api_client() -> APIClient:
    client = APIClient()
    return client


@pytest.fixture
def common_user():
    user = User.objects.create_user(
        username="username",
        password="password",
        email="email@example.com",
        is_active=True,
    )
    return user


@pytest.fixture
def admin_user():
    user = User.objects.create_superuser(
        username="username",
        password="password",
        email="email@example.com",
        is_active=True,
    )
    return user


@pytest.fixture
def todo(common_user):
    todo = Todo.objects.create(user=common_user, name="test todo", status=True)
    return todo


valid_payload = {
    "name": "test name",
    "status":True
}
invalid_payload = {
    "name": True
}
