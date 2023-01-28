from typing import Dict

from dj_rest_auth import serializers as dj_auth_serializers
from dj_rest_auth.registration import serializers as dj_reg_serializers
from rest_framework import serializers as rest_serializers

from user import models


class UserDetailSerializer(dj_auth_serializers.UserDetailsSerializer):
    def create(self, validated_data: Dict) -> models.User:
        user = models.User.objects.create_user(**validated_data)
        return user

    def update(self, instance: models.User, validated_data: Dict) -> models.User:
        instance.email = validated_data.get("email", instance.email)
        instance.username = validated_data.get("username", instance.username)
        instance.birthdate = validated_data.get("birthdate", instance.birthdate)
        instance.save()
        return instance

    class Meta(dj_auth_serializers.UserDetailsSerializer.Meta):
        fields = dj_auth_serializers.UserDetailsSerializer.Meta.fields + (
            "birthdate",
            "username",
        )


class RegisterSerializer(dj_reg_serializers.RegisterSerializer):
    birthdate = rest_serializers.DateField()

    def get_cleaned_data(self) -> Dict:
        data_dict = super().get_cleaned_data()
        data_dict["birthdate"] = self.validated_data.get("birthdate", "")
        return data_dict

    def create(self, validated_data: Dict) -> models.User:
        user = models.User.objects.create_user(**validated_data)
        return user

    def update(self, instance: models.User, validated_data: Dict) -> models.User:
        instance.email = validated_data.get("email", instance.email)
        instance.username = validated_data.get("username", instance.username)
        instance.birthdate = validated_data.get("birthdate", instance.birthdate)
        instance.save()
        return instance

    class Meta:
        model = models.User
        fields = ["username", "email", "password1", "password2", "birthdate"]


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
