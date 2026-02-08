from django.contrib.auth import get_user_model

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, permissions

from .serializers import (
    UserCreateSerializer,
    BaseUserViewSerializer
)


User = get_user_model()


class UserViewSetAdmin(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser, ]
    queryset = User.objects.all()

    def get_permissions(self):
        return [ permission() for permission in self.permission_classes]

