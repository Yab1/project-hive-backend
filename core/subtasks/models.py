from django.db import models
from core.common.models import BaseModel
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class SubTask(BaseModel):
    class Status(models.IntegerChoices):
        TO_DO = 1, _("To Do")
        IN_PROGRESS = 2, _("In Progress")
        COMPLETED = 3, _("Completed")
        ON_HOLD = 4, _("On Hold")

    task = models.ForeignKey(
        "tasks.Task",
        on_delete=models.CASCADE,
        related_name="subtasks",
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.IntegerField(choices=Status.choices, default=Status.TO_DO)
    assignee = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="subtasks_assigned"
    )

    class Meta:
        verbose_name = _("SubTask")
        verbose_name_plural = _("SubTasks")
        ordering = ["status"]

    def __str__(self):
        return self.title
