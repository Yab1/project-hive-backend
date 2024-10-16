from django.db import transaction

from .models import Project


@transaction.atomic
def project_create(
    *,
    name: str,
    description: str,
    states: int,
    stared_date: str,
    end_date: str,
    priority: int,
    owner_id: str,
):
    return Project.objects.create(
        name=name,
        description=description,
        states=states,
        stared_date=stared_date,
        end_date=end_date,
        priority=priority,
        owner_id=owner_id,
    )


@transaction.atomic
def project_update(
    *,
    project_instance: Project,
    name: str = None,
    description: str = None,
    states: int = None,
    stared_date: str = None,
    end_date: str = None,
    priority: int = None,
):
    if name is not None:
        project_instance.name = str(name)

    if description is not None:
        project_instance.description = str(description)

    if states is not None:
        project_instance.states = int(states)

    if stared_date is not None:
        project_instance.stared_date = stared_date

    if end_date is not None:
        project_instance.end_date = end_date

    if priority is not None:
        project_instance.priority = int(priority)

    project_instance.save()
    return project_instance
