from django.urls import path
from .apis import (
    TaskCreateApi,
    TaskDeleteApi,
    TaskDetailApi,
    TaskListApi,
    TaskUpdateApi,
)

app_name = "tasks"

urlpatterns = [
    path("", TaskListApi.as_view(), name="task-list"),
    path("create/", TaskCreateApi.as_view(), name="task-create"),
    path("<uuid:task_id>/", TaskDetailApi.as_view(), name="task-detail"),
    path("<uuid:task_id>/update/", TaskUpdateApi.as_view(), name="task-update"),
    path("<uuid:task_id>/delete/", TaskDeleteApi.as_view(), name="task-delete"),
]
