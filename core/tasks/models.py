from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import BaseModel


class Task(BaseModel):
    class Status(models.IntegerChoices):
        TO_DO = 1, _("To Do")
        IN_PROGRESS = 2, _("In Progress")
        COMPLETED = 3, _("Completed")
        ON_HOLD = 4, _("On Hold")

    class Priority(models.IntegerChoices):
        LOW = 1, _("Low")
        MEDIUM = 2, _("Medium")
        HIGH = 3, _("High")

    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.IntegerField(choices=Status.choices, default=Status.TO_DO)
    priority = models.IntegerField(choices=Priority.choices, default=Priority.LOW)
    assignee = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="tasks_assigned",
    )
    due_date = models.DateField()
    started_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")
        ordering = ["due_date"]

    def __str__(self):
        return self.title
