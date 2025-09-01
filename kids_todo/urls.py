from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskTemplateViewSet, DailyTaskViewSet

router = DefaultRouter()
router.register(r"templates", TaskTemplateViewSet, basename="kids-template")
router.register(r"daily", DailyTaskViewSet, basename="kids-daily")

urlpatterns = [
    path("", include(router.urls)),
]
