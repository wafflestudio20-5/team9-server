from typing import Dict

from dj_rest_auth import serializers as dj_auth_serializers
from dj_rest_auth.registration import serializers as dj_reg_serializers
from rest_framework import serializers as rest_serializers

from user import models

class UserSerializer(rest_serializers.ModelSerializer):
    class Meta(dj_auth_serializers.UserDetailsSerializer.Meta):
        model = models.User
        fields = ["id", "email", "username", "birthdate", "image"]
        read_only_fields = (
            "id",
            "email",
            "username",
        )


class UserDetailSerializer(dj_auth_serializers.UserDetailsSerializer):
    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError

    class Meta(dj_auth_serializers.UserDetailsSerializer.Meta):
        fields = dj_auth_serializers.UserDetailsSerializer.Meta.fields + (
            "birthdate",
            "username",
            "image",
        )


class RegisterSerializer(dj_reg_serializers.RegisterSerializer):
    birthdate = rest_serializers.DateField()

    def get_cleaned_data(self) -> Dict:
        data_dict = super().get_cleaned_data()
        data_dict["birthdate"] = self.validated_data.get("birthdate", "")
        return data_dict

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError


    class Meta:
        model = models.User
        fields = ["username", "email", "password1", "password2", "birthdate", "image"]


class SocialLoginSerializer(dj_reg_serializers.SocialLoginSerializer):
    def _get_request(self):
        return self.context.get("request")

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError


class EssentialUserInfoFromPKSerializer(rest_serializers.ModelSerializer):
    pk = rest_serializers.IntegerField()

    class Meta:
        model = models.User
        fields = ["pk", "username", "email"]
        read_only_fields = ["username", "email"]

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError
