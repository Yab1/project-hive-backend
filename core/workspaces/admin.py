from django.contrib import admin

from .models import Workspace


@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "owner",
        "created_at",
        "updated_at",
        "emoji",
    ]
    search_fields = ["name", "description"]
    list_filter = ["owner", "created_at"]
    fieldsets = (
        (
            "Workspace Details",
            {
                "fields": (
                    "name",
                    "description",
                    "emoji",
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
