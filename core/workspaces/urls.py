from django.urls import path

from .apis import (
    WorkspaceCreateApi,
    WorkspaceDeleteApi,
    WorkspaceDetailApi,
    WorkspaceListApi,
    WorkspaceUpdateApi,
)

app_name = "workspaces"

urlpatterns = [
    path("", WorkspaceListApi.as_view(), name="workspace-list"),
    path("create/", WorkspaceCreateApi.as_view(), name="workspace-create"),
    path("<uuid:workspace_id>/", WorkspaceDetailApi.as_view(), name="workspace-detail"),
    path(
        "<uuid:workspace_id>/update/",
        WorkspaceUpdateApi.as_view(),
        name="workspace-update",
    ),
    path("<uuid:workspace_id>/delete/", WorkspaceDeleteApi.as_view(), name="workspace-delete"),
]
