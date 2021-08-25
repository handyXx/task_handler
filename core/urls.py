from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from blog.api.views import TaskViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register("task", TaskViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(r"silk/", include("silk.urls", namespace="silk")),
    path("", include("blog.urls", namespace="blog")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/", include("blog.api.urls")),
    path("api-viewset/", include((router.urls, "api-viewset"))),
    path("account/", include("accounts.urls")),
]
