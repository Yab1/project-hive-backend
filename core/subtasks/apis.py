from django.db import IntegrityError
from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.mixins import ApiAuthMixin
from core.common.utils import get_object

from .models import SubTask
from .services import subtask_create, subtask_update


class SubTaskListApi(ApiAuthMixin, APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        title = serializers.CharField()
        description = serializers.CharField()
        status = serializers.ChoiceField(choices=SubTask.Status.choices)
        task = serializers.UUIDField()
        assignee = serializers.ListField(child=serializers.UUIDField())

    serializer_class = OutputSerializer

    def get(self, request):
        try:
            subtasks = SubTask.objects.all()

            output_serializer = self.OutputSerializer(subtasks, many=True)

            response_data = {"subtasks": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValueError(e)


class SubTaskDetailApi(ApiAuthMixin, APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        title = serializers.CharField()
        description = serializers.CharField()
        status = serializers.ChoiceField(choices=SubTask.Status.choices)
        task = serializers.UUIDField()
        assignee = serializers.ListField(child=serializers.UUIDField())

    serializer_class = OutputSerializer

    def get(self, request, subtask_id):
        subtask_instance = get_object(SubTask, id=subtask_id)

        try:
            output_serializer = self.OutputSerializer(subtask_instance)

            response_data = {"subtask": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValueError(e)


class SubTaskCreateApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=255)
        description = serializers.CharField()
        status = serializers.ChoiceField(
            choices=SubTask.Status.choices, default=SubTask.Status.TO_DO
        )
        task = serializers.UUIDField()
        assignee = serializers.ListField(child=serializers.UUIDField())

    serializer_class = InputSerializer

    def post(self, request):
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        try:
            subtask_instance = subtask_create(**input_serializer.validated_data)

            output_serializer = SubTaskDetailApi.OutputSerializer(subtask_instance)

            response_data = {"subtask": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_201_CREATED)

        except IntegrityError as e:
            raise ValidationError(e)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValueError(e)


class SubTaskUpdateApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=255, required=False)
        description = serializers.CharField(required=False)
        status = serializers.ChoiceField(choices=SubTask.Status.choices, required=False)
        task = serializers.UUIDField(required=False)
        assignee = serializers.ListField(child=serializers.UUIDField(), required=False)

    serializer_class = InputSerializer

    def put(self, request, subtask_id):
        subtask_instance = get_object(SubTask, id=subtask_id)
        input_serializer = self.InputSerializer(data=request.data, partial=True)
        input_serializer.is_valid(raise_exception=True)

        try:
            subtask_instance = subtask_update(
                subtask_instance=subtask_instance,
                **input_serializer.validated_data,
            )

            output_serializer = SubTaskDetailApi.OutputSerializer(subtask_instance)

            response_data = {"subtask": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except IntegrityError as e:
            raise ValidationError(e)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValueError(e)


class SubTaskDeleteApi(ApiAuthMixin, APIView):
    def delete(self, request, subtask_id):
        subtask_instance = get_object(SubTask, id=subtask_id)

        try:
            subtask_instance.delete()

            response_data = {"message": "Subtask removed from your list successfully."}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValueError(e)
