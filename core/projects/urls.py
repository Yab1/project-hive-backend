from django.urls import path

from .apis import (
    ProjectCreateApi,
    ProjectDeleteApi,
    ProjectDetailApi,
    ProjectListApi,
    ProjectUpdateApi,
)

app_name = "projects"

urlpatterns = [
    path("", ProjectListApi.as_view(), name="project-list"),
    path("create/", ProjectCreateApi.as_view(), name="project-create"),
    path("<uuid:project_id>/", ProjectDetailApi.as_view(), name="project-detail"),
    path(
        "<uuid:project_id>/update/",
        ProjectUpdateApi.as_view(),
        name="project-update",
    ),
    path(
        "<uuid:project_id>/delete/",
        ProjectDeleteApi.as_view(),
        name="project-delete",
    ),
]
