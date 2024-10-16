from django.contrib import admin
from .models import SubTask


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "task",
        "status",
        "created_at",
        "updated_at",
    ]
    search_fields = ["title", "task__title"]
    list_filter = ["status", "task"]
    fieldsets = (
        (
            "General Info",
            {
                "fields": ("title", "description", "task", "status", "assignee"),
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
