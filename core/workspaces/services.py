from django.db import transaction

from .models import Workspace


@transaction.atomic
def workspace_create(
    *,
    name: str,
    description: str = "",
    emoji: str = None,
    owner: str,
):
    if emoji is None:
        emoji = Workspace.emoji.field.default

    return Workspace.objects.create(
        name=name,
        description=description,
        emoji=emoji,
        owner=owner,
    )


@transaction.atomic
def workspace_update(
    *,
    workspace_instance: Workspace,
    name: str = None,
    description: str = None,
    emoji: str = None,
):
    if name is not None:
        workspace_instance.name = str(name)

    if description is not None:
        workspace_instance.description = str(description)

    if emoji is not None:
        workspace_instance.emoji = str(emoji)

    workspace_instance.save()
    return workspace_instance
