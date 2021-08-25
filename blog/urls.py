from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.IndexView.as_view(), name="home"),
    path("deposit", views.DepositView.as_view(), name="deposit"),
    path("category/add", views.CategoryCreationView.as_view(), name="category-add"),
    path(
        "category/<slug:category_slug>/",
        views.CategoryElementsListView.as_view(),
        name="category-elements",
    ),
    path("add-element", views.TaskCreationView.as_view(), name="add-task"),
    path("edit-element/<int:id>/", views.TaskEditView.as_view(), name="edit-task"),
    path("export_excel/", views.ExportExcel.as_view(), name="export-excel"),
]
