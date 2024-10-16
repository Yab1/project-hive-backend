from django.db import transaction

from .models import SubTask


@transaction.atomic
def subtask_create(
    *,
    title: str,
    description: str,
    status: int,
    task_id: str,
    assignee_ids: list,
):
    subtask_instance = SubTask.objects.create(
        title=title,
        description=description,
        status=status,
        task_id=task_id,
    )
    subtask_instance.assignee.set(assignee_ids)
    return subtask_instance


@transaction.atomic
def subtask_update(
    *,
    subtask_instance: SubTask,
    title: str = None,
    description: str = None,
    status: int = None,
    assignee_ids: list = None,
):
    if title is not None:
        subtask_instance.title = str(title)

    if description is not None:
        subtask_instance.description = str(description)

    if status is not None:
        subtask_instance.status = int(status)

    if assignee_ids is not None:
        subtask_instance.assignee.set(assignee_ids)

    subtask_instance.save()
    return subtask_instance
