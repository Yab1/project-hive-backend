from rest_framework import serializers
from rest_framework import status as http_status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.mixins import ApiAuthMixin

from .models import Member


class MemberListApi(ApiAuthMixin, APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        full_name = serializers.CharField()
        avatar = serializers.URLField()

    serializer_class = OutputSerializer

    def get(self, request):
        try:
            members = Member.objects.filter(is_active=True).all()

            output_serializer = self.OutputSerializer(members, many=True)

            response_data = {"members": output_serializer.data}

            return Response(data=response_data, status=http_status.HTTP_200_OK)

        except ValueError as e:
            raise ValidationError(e)

        except Exception as e:
            raise ValueError(e)
