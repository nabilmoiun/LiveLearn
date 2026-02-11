from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from drf_spectacular.utils import extend_schema

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, permissions, mixins, status

from .serializers import (
    UserCreateSerializer,
    BaseUserViewSerializer
)


User = get_user_model()


class UserViewSetAdmin(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet

):
    model = User
    permission_classes = [permissions.IsAdminUser, ]
    queryset = User.objects.all()


@extend_schema(tags=["auth"])
class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny, ]

    @extend_schema(responses={201: BaseUserViewSerializer})
    @action(
        detail=False,
        methods=["post"],
        serializer_class=UserCreateSerializer,
        url_path="register"
    )
    def register(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        instance, _ = User.objects.update_or_create(
            email=serializer.validated_data['email'],
            defaults={
                "full_name": serializer.validated_data['full_name'],
                "password": make_password(serializer.validated_data['password'])
            }
        )
        return Response(BaseUserViewSerializer(instance).data, status=status.HTTP_201_CREATED)
    
