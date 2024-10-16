from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "states",
        "priority",
        "stared_date",
        "end_date",
        "owner",
    ]
    search_fields = ["name", "description"]
    list_filter = ["states", "priority", "owner"]
    fieldsets = (
        (
            "Project Details",
            {
                "fields": (
                    "name",
                    "description",
                    "states",
                    "stared_date",
                    "end_date",
                    "priority",
                    "owner",
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
        return super().get_queryset(request).select_related("owner")
