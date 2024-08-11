import pytest
from django.urls import reverse

from ...fixtures.api_fixtures import (
    api_client,
    common_user,
    todo,
    valid_payload,
    invalid_payload,
)


@pytest.mark.django_db
class TestTodoApiDelete:

    def test_todo_api_delete_common_user(self, api_client, common_user, todo):
        url = reverse("todo:api-v1:todo-detail", kwargs={"pk": todo.id})
        api_client.force_authenticate(user=common_user)
        response = api_client.delete(url)
        assert response.status_code == 204

    def test_todo_api_delete_anonymous_user(self, api_client, todo):
        url = reverse("todo:api-v1:todo-detail", kwargs={"pk": todo.id})
        response = api_client.delete(url)
        assert response.status_code == 401
