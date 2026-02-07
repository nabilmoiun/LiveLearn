from django.contrib.auth import get_user_model

from rest_framework import serializers


User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "full_name",
            "email",
            "role",
            "password",
        )
        read_only_fields = ("id", )

    def validate(self, attrs):
        email = attrs['email']
        if User.objects.filter(email=email, is_active=True).exists():
            raise serializers.ValidationError({
                "email": ["User with the email already exists"]
            })
        return attrs

    def create(self, validated_data):
        email = validated_data.pop("email")
        password = validated_data.pop("password")
        instance, _ = User.objects.update_or_create(
            email=email,
            defaults={**validated_data}
        )
        instance.set_password(password)
        instance.save()
        return instance


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
