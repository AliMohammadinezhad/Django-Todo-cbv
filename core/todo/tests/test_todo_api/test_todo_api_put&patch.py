import pytest
from django.urls import reverse

from ...fixtures.api_fixtures import api_client,common_user, todo,valid_payload, invalid_payload

@pytest.mark.django_db
class TestTodoApiPutAndPatch:
    """Put and Patch API"""
    
    def test_put_todo_with_valid_payload_common_user(self, api_client, common_user, todo):
        api_client.force_authenticate(user=common_user)
        url = reverse("todo:api-v1:todo-detail", kwargs={"pk": todo.id})
        response = api_client.put(url, data=valid_payload)
        assert response.status_code == 200
        assert response.data['name'] == valid_payload['name']
        
    def test_put_todo_with_invalid_payload_common_user(self, api_client, common_user, todo):
        api_client.force_authenticate(user=common_user)
        url = reverse("todo:api-v1:todo-detail", kwargs={"pk": todo.id})
        response = api_client.put(url, data=invalid_payload)
        assert response.status_code == 400
        
    def test_patch_todo_with_valid_payload_common_user(self, api_client, common_user, todo):
        api_client.force_authenticate(user=common_user)
        url = reverse("todo:api-v1:todo-detail", kwargs={"pk": todo.id})
        response = api_client.patch(url, data=valid_payload)
        assert response.status_code == 200
        assert response.data['name'] == valid_payload['name']
    
    def test_patch_todo_with_invalid_payload_common_user(self, api_client, common_user, todo):
        api_client.force_authenticate(user=common_user)
        url = reverse("todo:api-v1:todo-detail", kwargs={"pk": todo.id})
        response = api_client.patch(url, data=invalid_payload)
        assert response.status_code == 400
        
    def test_patch_and_put_todo_with_invalid_payload_anonymous_user(self, api_client,todo):
        url = reverse("todo:api-v1:todo-detail", kwargs={"pk": todo.id})
        response_patch = api_client.patch(url, data=invalid_payload)
        response_put = api_client.put(url, data=invalid_payload)
        assert response_patch.status_code == 401
        assert response_put.status_code == 401
    
    def test_patch_and_put_todo_with_valid_payload_anonymous_user(self, api_client,todo):
        url = reverse("todo:api-v1:todo-detail", kwargs={"pk": todo.id})
        response_patch = api_client.patch(url, data=valid_payload)
        response_put = api_client.put(url, data=valid_payload)
        assert response_patch.status_code == 401
        assert response_put.status_code == 401   
    