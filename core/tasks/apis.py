from django.db import IntegrityError
from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.mixins import ApiAuthMixin
from core.common.utils import get_object

from .models import Task
from .services import task_create, task_update


class TaskListApi(ApiAuthMixin, APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        title = serializers.CharField()
        description = serializers.CharField()
        status = serializers.ChoiceField(choices=Task.Status.choices)
        priority = serializers.ChoiceField(choices=Task.Priority.choices)
        due_date = serializers.DateField()
        started_date = serializers.DateField(allow_null=True, required=False)
        end_date = serializers.DateField(allow_null=True, required=False)
        project = serializers.UUIDField()
        assignee = serializers.ListField(child=serializers.UUIDField())

    serializer_class = OutputSerializer

    def get(self, request):
        try:
            tasks = Task.objects.all()

            output_serializer = self.OutputSerializer(tasks, many=True)

            response_data = {"tasks": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValueError(e)


class TaskDetailApi(ApiAuthMixin, APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        title = serializers.CharField()
        description = serializers.CharField()
        status = serializers.ChoiceField(choices=Task.Status.choices)
        priority = serializers.ChoiceField(choices=Task.Priority.choices)
        due_date = serializers.DateField()
        started_date = serializers.DateField(allow_null=True, required=False)
        end_date = serializers.DateField(allow_null=True, required=False)
        project = serializers.UUIDField()
        assignee = serializers.ListField(child=serializers.UUIDField())

    serializer_class = OutputSerializer

    def get(self, request, task_id):
        task_instance = get_object(Task, id=task_id)

        try:
            output_serializer = self.OutputSerializer(task_instance)

            response_data = {"task": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValueError(e)


class TaskCreateApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=255)
        description = serializers.CharField()
        status = serializers.ChoiceField(
            choices=Task.Status.choices,
            default=Task.Status.TO_DO,
        )
        priority = serializers.ChoiceField(
            choices=Task.Priority.choices,
            default=Task.Priority.LOW,
        )
        due_date = serializers.DateField()
        started_date = serializers.DateField(required=False, allow_null=True)
        end_date = serializers.DateField(required=False, allow_null=True)
        project = serializers.UUIDField()
        assignee = serializers.ListField(child=serializers.UUIDField())

    serializer_class = InputSerializer

    def post(self, request):
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        try:
            task_instance = task_create(**input_serializer.validated_data)

            output_serializer = TaskDetailApi.OutputSerializer(task_instance)

            response_data = {"task": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_201_CREATED)

        except IntegrityError as e:
            raise ValidationError(e)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValueError(e)


class TaskUpdateApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=255, required=False)
        description = serializers.CharField(required=False)
        status = serializers.ChoiceField(choices=Task.Status.choices, required=False)
        priority = serializers.ChoiceField(
            choices=Task.Priority.choices,
            required=False,
        )
        due_date = serializers.DateField(required=False)
        started_date = serializers.DateField(required=False, allow_null=True)
        end_date = serializers.DateField(required=False, allow_null=True)
        project = serializers.UUIDField(required=False)
        assignee = serializers.ListField(child=serializers.UUIDField(), required=False)

    serializer_class = InputSerializer

    def put(self, request, task_id):
        task_instance = get_object(Task, id=task_id)
        input_serializer = self.InputSerializer(data=request.data, partial=True)
        input_serializer.is_valid(raise_exception=True)

        try:
            task_instance = task_update(
                task_instance=task_instance,
                **input_serializer.validated_data,
            )

            output_serializer = TaskDetailApi.OutputSerializer(task_instance)

            response_data = {"task": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except IntegrityError as e:
            raise ValidationError(e)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValueError(e)


class TaskDeleteApi(ApiAuthMixin, APIView):
    def delete(self, request, task_id):
        task_instance = get_object(Task, id=task_id)

        try:
            task_instance.delete()

            response_data = {"message": "Task removed from your list successfully."}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValueError(e)
