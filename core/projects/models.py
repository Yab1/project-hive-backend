from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import BaseModel


class Project(BaseModel):
    class Status(models.TextChoices):
        TO_DO = "to_do", _("To Do")
        IN_PROGRESS = "in_progress", _("In Progress")
        ON_HOLD = "on_hold", _("On Hold")
        COMPLETED = "completed", _("Completed")
        CANCELLED = "cancelled", _("Cancelled")

    class Priority(models.TextChoices):
        HIGHEST = "highest", _("Highest")
        HIGH = "high", _("High")
        MEDIUM = "medium", _("Medium")
        LOW = "low", _("Low")
        LOWEST = "lowest", _("Lowest")

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(choices=Status.choices, max_length=20, default=Status.TO_DO)
    due_date = models.DateField(blank=True, null=True)
    started_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    priority = models.CharField(choices=Priority.choices, max_length=20, default=Priority.MEDIUM)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="projects_owned",
    )
    workspace = models.ForeignKey(
        "workspaces.Workspace",
        on_delete=models.CASCADE,
        related_name="projects",
    )
    emoji = models.CharField(max_length=10, blank=True, default="📑")

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
        ordering = ["started_date"]

    def __str__(self):
        return self.name
