from django.db import transaction

from .models import Task


@transaction.atomic
def task_create(
    *,
    title: str,
    description: str,
    status: int,
    priority: int,
    due_date: str,
    task_id: str,
    assignee_ids: list,
):
    task_instance = Task.objects.create(
        title=title,
        description=description,
        status=status,
        priority=priority,
        due_date=due_date,
        task_id=task_id,
    )
    task_instance.assignee.set(assignee_ids)
    return task_instance


@transaction.atomic
def task_update(
    *,
    task_instance: Task,
    title: str = None,
    description: str = None,
    status: int = None,
    priority: int = None,
    due_date: str = None,
    assignee_ids: list = None,
):
    if title is not None:
        task_instance.title = str(title)

    if description is not None:
        task_instance.description = str(description)

    if status is not None:
        task_instance.status = int(status)

    if priority is not None:
        task_instance.priority = int(priority)

    if due_date is not None:
        task_instance.due_date = due_date

    if assignee_ids is not None:
        task_instance.assignee.set(assignee_ids)

    task_instance.save()
    return task_instance
