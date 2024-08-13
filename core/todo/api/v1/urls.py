from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import TodoViewSet,GetWeather


app_name = "api-v1"

router = DefaultRouter()
router.register("todo", TodoViewSet, basename="todo")


urlpatterns = router.urls

urlpatterns += [
    path("weather/", GetWeather.as_view(), name="weather"),
]