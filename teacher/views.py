from django.contrib.auth import get_user_model

from drf_spectacular.utils import extend_schema

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, permissions, parsers, status

from .models import (
    Batch,
    Teacher,
    Academic,
    ProfessionalExperience
)
from .serializers import (
    AcademicSerializer,
    BatchViewSerializer,
    BatchCreateSerializer,
    BatchDetailsSerializer,
    ProfileDetailsSerializer,
    ProfessionalExperienceSerializer,
)

from .utils import generate_class_link
from user.permissions import IsTeacher


User = get_user_model()


@extend_schema(
    tags=['teacher academics']
)
class AcademicViewSet(viewsets.ModelViewSet):
    permission_classes = [IsTeacher]
    serializer_class = AcademicSerializer
    queryset = Academic.objects.order_by("passing_year")

    def get_queryset(self):
        return self.queryset.filter(teacher=self.request.user.teacher_profile)

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user.teacher_profile)


@extend_schema(
    tags=['teacher experience']
)
class ProfessionalExperienceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsTeacher]
    serializer_class = ProfessionalExperienceSerializer
    queryset = ProfessionalExperience.objects.order_by("to_time")

    def get_queryset(self):
        return self.queryset.filter(teacher=self.request.user.teacher_profile)

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user.teacher_profile)


@extend_schema(tags=['teachers profile'])
class ProfileViewSet(viewsets.GenericViewSet):
    permission_classes = [IsTeacher, ]
    serializer_class = ProfileDetailsSerializer
    queryset = Teacher.objects.all()

    def get_queryset(self):
        qs = (
            self.queryset.select_related("user")
            .prefetch_related("academics", "professional_experiences")
            .get(user=self.request.user)
        )
        return qs

    @extend_schema(responses={200: ProfileDetailsSerializer})
    @action(
        detail=False,
        methods=['get'],
        serializer_class=ProfileDetailsSerializer,
        url_path="profile"
    )
    def profile(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset())
        return Response(serializer.data)

@extend_schema(tags=['teacher batches'])
class BatchViewSet(viewsets.ModelViewSet):
    permission_classes = [IsTeacher]
    serializer_class = BatchViewSerializer
    queryset = Batch.objects.all()

    def get_queryset(self):
        qs = (
            Batch.objects.filter(teacher=self.request.user)
            .select_related("subject")
            .prefetch_related("students")
        )
        return qs

    def get_serializer_class(self):
        if self.action in ("create", "update"):
            return BatchCreateSerializer
        elif self.action in ("list", ):
            return self.serializer_class
        elif self.action in ("retrieve", ):
            return BatchDetailsSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        response_serializer = BatchViewSerializer(instance)
        headers = self.get_success_headers(response_serializer.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer) -> Batch:
        return serializer.save(
            teacher=self.request.user,
            class_link=generate_class_link(self.request.user)
        )

    def destroy(self, request, *args, **kwargs):
        return Response({
            "details": ['Method not allowed'],
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)

