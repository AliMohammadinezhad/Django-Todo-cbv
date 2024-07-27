from rest_framework.routers import DefaultRouter

from .views import TodoViewSet


app_name = 'api-v1'

router = DefaultRouter()
router.register('todo', TodoViewSet, basename='todo')


urlpatterns = router.urls
