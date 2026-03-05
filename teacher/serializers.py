from django.contrib.auth import get_user_model

from rest_framework import serializers

from subject.models import Subject
from .models import (
    Batch,
    Academic,
    ExtraInformation,
    ProfessionalExperience, Teacher
)


User = get_user_model()


class AcademicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Academic
        exclude = ("teacher", )


class ExtraInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraInformation
        exclude = ("teacher", )


class ProfessionalExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalExperience
        exclude = ("teacher", )


class TeacherUserInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "full_name",
            "email",
            "phone_number",
            "avatar"
        )

class ProfileDetailsSerializer(serializers.ModelSerializer):
    user = TeacherUserInformationSerializer(read_only=True)
    academics = AcademicSerializer(many=True, read_only=True)
    professional_experiences = ProfessionalExperienceSerializer(many=True, read_only=True)

    class Meta:
        model = Teacher
        fields = "__all__"


class TeacherSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"


class BatchCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        exclude = ("teacher", "students", "class_link", )


class BatchViewSerializer(serializers.ModelSerializer):
    subject = TeacherSubjectSerializer(read_only=True)

    class Meta:
        model = Batch
        exclude = ("teacher", "students", )


class BatchDetailsSerializer(serializers.ModelSerializer):
    students = TeacherUserInformationSerializer(many=True, read_only=True)

    class Meta:
        model = Batch
        exclude = ("teacher", )
