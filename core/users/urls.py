from django.urls import path

from .apis import MemberListApi

app_name = "members"

urlpatterns = [
    path("", MemberListApi.as_view(), name="members-list"),
]
