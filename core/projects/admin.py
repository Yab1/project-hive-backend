from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "status",
        "priority",
        "due_date",
        "started_date",
        "end_date",
        "owner",
        "workspace",
    ]

    search_fields = ["name", "description", "owner__username"]
    list_filter = ["status", "priority", "owner", "workspace"]

    fieldsets = (
        (
            "Project Details",
            {
                "fields": (
                    "name",
                    "description",
                    "status",
                    "priority",
                ),
            },
        ),
        (
            "Ownership",
            {
                "fields": (
                    "owner",
                    "workspace",
                ),
            },
        ),
        (
            "Timeline",
            {
                "fields": (
                    "started_date",
                    "due_date",
                    "end_date",
                ),
            },
        ),
        (
            "Metadata",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    readonly_fields = ["created_at", "updated_at"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("owner", "workspace")

    class Meta:
        ordering = ["started_date"]
