from django.contrib.auth import get_user_model

from rest_framework import serializers


User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = get_user_model()
        fields = (
            "full_name",
            "email",
            "role",
            "password",
        )
        read_only_fields = ("role", )

    def validate(self, attrs):
        email = attrs['email']
        if User.objects.filter(email=email, is_active=True).exists():
            raise serializers.ValidationError({
                "email": ["User with the email already exists"]
            })
        return attrs


class BaseUserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "full_name",
            "phone_number",
            "email",
            "role",
            "avatar",
            "is_active",
        )
