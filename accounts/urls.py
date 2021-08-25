from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import UserLoginForm

app_name = "account"

urlpatterns = [
    path(
        "login/",
        views.LogInView.as_view(),
        name="login",
    ),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="/account/login/"),
        name="logout",
    ),
]
