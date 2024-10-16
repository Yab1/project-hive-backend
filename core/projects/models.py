from django.db import models
from core.common.models import BaseModel
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Project(BaseModel):
    class States(models.IntegerChoices):
        ACTIVE = 1, _("Active")
        COMPLETED = 2, _("Completed")
        ON_HOLD = 3, _("On Hold")
        CANCELLED = 4, _("Cancelled")

    class Priority(models.IntegerChoices):
        LOW = 1, _("Low")
        MEDIUM = 2, _("Medium")
        HIGH = 3, _("High")
        URGENT = 4, _("Urgent")

    name = models.CharField(max_length=255)
    description = models.TextField()
    states = models.IntegerField(choices=States.choices)
    stared_date = models.DateTimeField()
    end_date = models.DateTimeField()
    priority = models.IntegerField(choices=Priority.choices)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="projects",
    )

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
        ordering = ["stared_date"]

    def __str__(self):
        return self.name
