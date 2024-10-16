from django.urls import path
from .apis import (
    SubTaskCreateApi,
    SubTaskDeleteApi,
    SubTaskDetailApi,
    SubTaskListApi,
    SubTaskUpdateApi,
)

app_name = "subtasks"

urlpatterns = [
    path("", SubTaskListApi.as_view(), name="subtask-list"),
    path("create/", SubTaskCreateApi.as_view(), name="subtask-create"),
    path("<uuid:subtask_id>/", SubTaskDetailApi.as_view(), name="subtask-detail"),
    path(
        "<uuid:subtask_id>/update/",
        SubTaskUpdateApi.as_view(),
        name="subtask-update",
    ),
    path(
        "<uuid:subtask_id>/delete/",
        SubTaskDeleteApi.as_view(),
        name="subtask-delete",
    ),
]
