from datetime import datetime

from django.db import transaction

from core.workspaces.models import Workspace

from .models import Project


@transaction.atomic
def project_create(
    *,
    name: str,
    description: str = None,
    status: str,
    priority: str,
    time_frame: dict = None,
    workspace: Workspace,
    owner: str,
):
    stared_date_dt = datetime.fromisoformat(time_frame.get("from")) if time_frame.get("from") else None
    end_date_dt = datetime.fromisoformat(time_frame.get("to")) if time_frame.get("to") else None

    return Project.objects.create(
        name=name,
        description=description,
        status=status,
        started_date=stared_date_dt,
        end_date=end_date_dt,
        due_date=end_date_dt,
        priority=priority,
        owner=owner,
        workspace=workspace,
    )


@transaction.atomic
def project_update(
    *,
    project_instance: Project,
    name: str = None,
    description: str = None,
    status: int = None,
    started_date: str = None,
    end_date: str = None,
    priority: int = None,
):
    if name is not None:
        project_instance.name = str(name)

    if description is not None:
        project_instance.description = str(description)

    if status is not None:
        project_instance.status = int(status)

    if started_date is not None:
        project_instance.started_date = started_date

    if end_date is not None:
        project_instance.end_date = end_date

    if priority is not None:
        project_instance.priority = int(priority)

    project_instance.save()
    return project_instance
