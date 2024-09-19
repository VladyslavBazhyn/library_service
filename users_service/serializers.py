from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.hashers import make_password


class UserBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = (
            "id", "first_name", "last_name", "email", "nickname", "password"
        )


class UserRegisterSerializer(UserBaseSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "email", "password", "nickname"
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)


class UserProfileSerializer(UserBaseSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "email", "nickname", "first_name", "last_name"
        )


