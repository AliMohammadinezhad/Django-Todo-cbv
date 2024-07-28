from rest_framework import serializers
from django.contrib.auth import get_user_model

from ...models import Todo



class TodoSerializer(serializers.ModelSerializer):
    relative_path = serializers.URLField(source="get_absolute_api_url", read_only=True)
    absolute_path = serializers.HyperlinkedIdentityField(
        view_name="todo:api-v1:todo-detail", read_only=True
    )

    class Meta:
        model = Todo
        fields = [
            "id",
            "relative_path",
            "absolute_path",
            "user",
            "name",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["user", "created_at", "updated_at"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
