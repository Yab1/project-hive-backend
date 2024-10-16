from django.db import IntegrityError
from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.mixins import ApiAuthMixin
from core.common.utils import get_object

from .models import Project
from .services import project_create, project_update


class ProjectListApi(ApiAuthMixin, APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        name = serializers.CharField()
        description = serializers.CharField()
        states = serializers.ChoiceField(choices=Project.States.choices)
        stared_date = serializers.DateTimeField()
        end_date = serializers.DateTimeField()
        priority = serializers.ChoiceField(choices=Project.Priority.choices)
        owner = serializers.UUIDField()

    serializer_class = OutputSerializer

    def get(self, request):
        try:
            projects = Project.objects.all()

            output_serializer = self.OutputSerializer(projects, many=True)

            response_data = {"projects": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValueError(e)


class ProjectDetailApi(ApiAuthMixin, APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        name = serializers.CharField()
        description = serializers.CharField()
        states = serializers.ChoiceField(choices=Project.States.choices)
        stared_date = serializers.DateTimeField()
        end_date = serializers.DateTimeField()
        priority = serializers.ChoiceField(choices=Project.Priority.choices)
        owner = serializers.UUIDField()

    serializer_class = OutputSerializer

    def get(self, request, project_id):
        project_instance = get_object(Project, id=project_id)

        try:
            output_serializer = self.OutputSerializer(project_instance)

            response_data = {"project": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValueError(e)


class ProjectCreateApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=255)
        description = serializers.CharField()
        states = serializers.ChoiceField(choices=Project.States.choices)
        stared_date = serializers.DateTimeField()
        end_date = serializers.DateTimeField()
        priority = serializers.ChoiceField(choices=Project.Priority.choices)

    serializer_class = InputSerializer

    def post(self, request):
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        try:
            project_instance = project_create(
                **input_serializer.validated_data,
                owner=request.user,
            )

            output_serializer = ProjectDetailApi.OutputSerializer(project_instance)

            response_data = {"project": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_201_CREATED)

        except IntegrityError as e:
            raise ValidationError(e)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValueError(e)


class ProjectUpdateApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=255, required=False)
        description = serializers.CharField(required=False)
        states = serializers.ChoiceField(choices=Project.States.choices, required=False)
        stared_date = serializers.DateTimeField(required=False)
        end_date = serializers.DateTimeField(required=False)
        priority = serializers.ChoiceField(
            choices=Project.Priority.choices,
            required=False,
        )

    serializer_class = InputSerializer

    def put(self, request, project_id):
        project_instance = get_object(Project, id=project_id)
        input_serializer = self.ProjectUpdateApi(data=request.data, partial=True)
        input_serializer.is_valid(raise_exception=True)

        try:
            project_instance = project_update(
                project_instance=project_instance,
                **input_serializer.validated_data,
            )

            output_serializer = ProjectDetailApi.OutputSerializer(project_instance)

            response_data = {"project": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except IntegrityError as e:
            raise ValidationError(e)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValueError(e)


class ProjectDeleteApi(ApiAuthMixin, APIView):
    def delete(self, request, project_id):
        project_instance = get_object(Project, id=project_id)

        try:
            project_instance.delete()

            response_data = {"message": "Project removed from your list successfully."}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValueError(e)
