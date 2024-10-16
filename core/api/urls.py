from django.urls import include, path
from django.urls.resolvers import URLResolver

urlpatterns: list[URLResolver] = [
    path(
        "auth/",
        include(
            ("core.authentication.urls", "authentication"), namespace="authentication"
        ),
    ),
    path(
        "projects/", include(("core.projects.urls", "projects"), namespace="projects")
    ),
    path(
        "tasks/",
        include(("core.tasks.urls", "tasks"), namespace="tasks"),
    ),
    path(
        "auth/",
        include(("core.subtasks.urls", "subtasks"), namespace="subtasks"),
    ),
]
