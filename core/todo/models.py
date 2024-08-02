
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model() 

class Todo(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    name = models.CharField(max_length=512)
    status = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_api_url(self):
        return reverse("todo:api-v1:todo-detail", kwargs={"pk": self.pk})
    
    