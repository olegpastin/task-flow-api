from .models import User

from rest_framework import serializers


class CreateUserSerializer(serializers.ModelSerializer):
    """Serializes user data for registration with write-only password."""
    password = serializers.CharField(write_only=True, min_length=8)
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class DetailAuthorizedUserSerializer(serializers.ModelSerializer):
    """Serializes detailed user data without exposing password."""
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'date_joined'
        )
        read_only_fields = fields