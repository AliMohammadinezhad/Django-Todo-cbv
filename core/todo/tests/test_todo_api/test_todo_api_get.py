import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from ...fixtures.api_fixtures import common_user, admin_user,todo, api_client
from ...models import Todo

@pytest.mark.django_db
class TestTodoApiGet:

    # detail view get requests
    def test_get_todo_by_id_logged_in(self, api_client: APIClient, common_user, todo):
        url = reverse("todo:api-v1:todo-detail", kwargs={"pk": todo.id})
        api_client.force_authenticate(user=common_user)
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data["user"] == todo.user.id
        assert response.data["name"] == todo.name
        assert response.data["status"] == todo.status
        assert response.data["relative_path"] is not None
        assert response.data["absolute_path"] is not None
        assert response.data["created_at"] is not None
        assert response.data["updated_at"] is not None
        

    def test_get_todo_by_id_anonymouse(self, api_client: APIClient, todo):
        url = reverse("todo:api-v1:todo-detail", kwargs={"pk": todo.id})
        response = api_client.get(url)
        assert response.status_code == 401

    # list view
    def test_get_todo_list_logged_in(self, api_client, common_user, todo):
        api_client.force_authenticate(user=common_user)
        url = reverse("todo:api-v1:todo-list")
        response = api_client.get(url)
        assert response.data[0]['id'] == todo.id
        assert response.data[0]['relative_path'] is not None
        assert response.data[0]['absolute_path'] is not None
        assert response.data[0]['user'] == common_user.id
        assert response.data[0]['name'] == todo.name
        assert response.data[0]['status'] == todo.status
        assert response.data[0]['created_at'] is not None
        assert response.data[0]['updated_at'] is not None
        assert response.status_code == 200
        

    def test_get_todo_list_anonymouse(self, api_client):
        url = reverse("todo:api-v1:todo-list")
        response = api_client.get(url)
        assert response.status_code == 401
        
    def test_get_does_not_exist_todo_detail(self, api_client, common_user, todo):
        url = reverse("todo:api-v1:todo-detail", kwargs={"pk":todo.id + 1})
        response = api_client.get(url)
        api_client.force_authenticate(user=common_user)
        response = api_client.get(url)
        assert response.status_code == 404
        
