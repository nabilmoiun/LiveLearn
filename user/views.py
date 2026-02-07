from django.contrib.auth import get_user_model

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, permissions

from .serializers import (
    UserCreateSerializer,
    BaseUserViewSerializer
)


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return BaseUserViewSerializer
        return UserCreateSerializer

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            self.permission_classes = [permissions.IsAdminUser, ]
        elif self.action in ("update", "destroy"):
            self.permission_classes = [permissions.IsAuthenticated, ]
        return [ permission() for permission in self.permission_classes]

    @action(
        methods=["get"],
        detail = False,
        url_path="me",
        permission_classes=[permissions.IsAuthenticated, ]
    )
    def me(self, *args, **kwargs):
        instance = User.objects.get(id=self.request.user.id)
        serializer = BaseUserViewSerializer(instance)
        return Response(serializer.data)


