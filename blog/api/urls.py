from django.contrib import admin
from django.urls import include, path
from rest_framework import views

from .views import (CategoryAPIView, TaskAPIDetailView, TaskAPIView,
                    TasksByCategoryView)

app_name = "blog-api"

urlpatterns = [
    path("task/", TaskAPIView.as_view(), name="task-api"),
    path("d/<int:id>/", TaskAPIDetailView.as_view(), name="task-detail-api"),
    path("category/", CategoryAPIView.as_view(), name="category-list-api"),
    path(
        "category/<slug:category_slug>/",
        TasksByCategoryView.as_view(),
        name="category-api",
    ),
]
