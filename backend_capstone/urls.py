from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/users/", include("tasks.user_urls")),
    path("api/tasks/", include("tasks.urls")),
    path("api/kids/", include("kids_todo.urls")),
    path("api/library/", include("library.urls")),
]
