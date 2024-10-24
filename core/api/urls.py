from django.urls import include, path
from django.urls.resolvers import URLResolver

urlpatterns: list[URLResolver] = [
    path(
        "auth/",
        include(
            ("core.authentication.urls", "authentication"),
            namespace="authentication",
        ),
    ),
    path(
        "members/",
        include(("core.users.urls", "members"), namespace="members"),
    ),
    path(
        "projects/",
        include(("core.projects.urls", "projects"), namespace="projects"),
    ),
    path(
        "tasks/",
        include(("core.tasks.urls", "tasks"), namespace="tasks"),
    ),
    path(
        "subtasks/",
        include(("core.subtasks.urls", "subtasks"), namespace="subtasks"),
    ),
    path(
        "workspaces/",
        include(("core.workspaces.urls", "workspaces"), namespace="workspaces"),
    ),
]
