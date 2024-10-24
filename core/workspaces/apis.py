from django.db import IntegrityError
from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.mixins import ApiAuthMixin
from core.common.utils import get_object, inline_serializer
from core.projects.models import Project
from core.users.models import Member
from core.workspaces.models import Workspace

from .services import workspace_create, workspace_update


class WorkspaceListApi(ApiAuthMixin, APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        name = serializers.CharField()
        emoji = serializers.CharField()
        projects = inline_serializer(
            many=True,
            fields={
                "id": serializers.UUIDField(),
                "name": serializers.CharField(),
                "description": serializers.CharField(),
                "emoji": serializers.CharField(),
                "status": serializers.ChoiceField(choices=Project.Status.choices),
                "priority": serializers.ChoiceField(choices=Project.Priority.choices),
                "started_date": serializers.DateTimeField(),
                "end_date": serializers.DateTimeField(),
                "owner": inline_serializer(
                    fields={
                        "id": serializers.UUIDField(),
                        "full_name": serializers.CharField(),
                        "avatar": serializers.ImageField(),
                    },
                ),
            },
        )

    serializer_class = OutputSerializer

    def get(self, request):
        try:
            workspaces = Workspace.objects.prefetch_related("projects").all()

            output_serializer = self.OutputSerializer(
                workspaces,
                # context={"projects": [workspace.projects.all() for workspace in workspaces]},
                many=True,
            )

            response_data = {"workspaces": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValueError(e)


class WorkspaceDetailApi(ApiAuthMixin, APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        name = serializers.CharField()
        description = serializers.CharField()
        emoji = serializers.CharField()
        owner = inline_serializer(
            fields={
                "id": serializers.UUIDField(),
                "full_name": serializers.CharField(),
                "avatar": serializers.ImageField(),
            },
        )

    serializer_class = OutputSerializer

    def get(self, request, workspace_id):
        workspace_instance = Workspace.objects.get(id=workspace_id)

        try:
            output_serializer = self.OutputSerializer(workspace_instance)

            response_data = {"workspace": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValueError(e)


class WorkspaceCreateApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=255)
        description = serializers.CharField(required=False)
        emoji = serializers.CharField(max_length=10, required=False)

    serializer_class = InputSerializer

    def post(self, request):
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        owner = Member.objects.get(email="david.wilson@example.com")

        try:
            workspace_instance = workspace_create(
                **input_serializer.validated_data,
                # owner=request.user,
                owner=owner,
            )

            output_serializer = WorkspaceDetailApi.OutputSerializer(workspace_instance)

            response_data = {"workspace": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_201_CREATED)

        except IntegrityError as e:
            raise ValidationError(e)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class WorkspaceUpdateApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=255, required=False)
        description = serializers.CharField(required=False)
        emoji = serializers.CharField(max_length=10, required=False)

    serializer_class = InputSerializer

    def put(self, request, workspace_id):
        workspace_instance = get_object(Workspace, id=workspace_id)
        input_serializer = self.InputSerializer(data=request.data, partial=True)
        input_serializer.is_valid(raise_exception=True)

        try:
            workspace_instance = workspace_update(
                workspace_instance=workspace_instance,
                **input_serializer.validated_data,
            )

            output_serializer = WorkspaceDetailApi.OutputSerializer(workspace_instance)

            response_data = {"workspace": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except IntegrityError as e:
            raise ValidationError(e)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValidationError(e)


class WorkspaceDeleteApi(ApiAuthMixin, APIView):
    def delete(self, request, workspace_id):
        workspace_instance = get_object(Workspace, id=workspace_id)

        try:
            workspace_instance.delete()

            response_data = {"message": "Workspace removed successfully."}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValueError(e)
