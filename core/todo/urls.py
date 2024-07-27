from django.urls import path, include

from . import views

app_name = "todo"

urlpatterns = [
    path("", views.TodoListView.as_view(), name="todo-list"),
    path("create/", views.TodoCreateView.as_view(), name="todo-create"),
    path("update/<int:pk>/", views.TodoUpdateView.as_view(), name="todo-update"),
    path("complete/<int:pk>/", views.TodoCompleteView.as_view(), name="todo-complete"),
    path("delete/<int:pk>/", views.TodoDeleteView.as_view(), name="todo-delete"),
    path("api/v1/", include("todo.api.v1.urls")),
]
