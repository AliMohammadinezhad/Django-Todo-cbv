import pytest
from django.urls import reverse

from ...fixtures.api_fixtures import (
    api_client,
    common_user,
    valid_payload,
    invalid_payload,
)


@pytest.mark.django_db
class TestTodoApiPost:

    def test_post_todo_with_valid_data_common_user(self, api_client, common_user):
        api_client.force_authenticate(user=common_user)
        url = reverse("todo:api-v1:todo-list")
        response = api_client.post(url, data=valid_payload)
        assert response.data["user"] == common_user.id
        assert response.data["name"] == valid_payload["name"]
        assert response.status_code == 201

    def test_post_todo_with_invalid_data_common_user(self, api_client, common_user):
        api_client.force_authenticate(user=common_user)
        url = reverse("todo:api-v1:todo-list")
        response = api_client.post(url, data=invalid_payload)
        assert response.status_code == 400

    def test_post_todo_anonymouse_user(self, api_client):
        url = reverse("todo:api-v1:todo-list")
        response_valid_data = api_client.post(url, data=valid_payload)
        response_invalid_data = api_client.post(url, data=invalid_payload)
        assert response_valid_data.status_code == 401
        assert response_invalid_data.status_code == 401
