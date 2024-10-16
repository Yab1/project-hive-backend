from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "project",
        "status",
        "priority",
        "due_date",
        "started_date",
        "end_date",
    ]
    search_fields = ["title", "description"]
    list_filter = ["status", "priority", "project"]
    fieldsets = (
        (
            "Task Details",
            {
                "fields": (
                    "project",
                    "title",
                    "description",
                    "status",
                    "priority",
                    "assignee",
                    "due_date",
                    "started_date",
                    "end_date",
                ),
            },
        ),
        (
            "Important Dates",
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )
    readonly_fields = ["created_at", "updated_at"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("project")
