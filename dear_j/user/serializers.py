from typing import Dict

from allauth.socialaccount import models as allauth_models
from dj_rest_auth import serializers as dj_auth_serializers
from dj_rest_auth.registration import serializers as dj_reg_serializers
from rest_framework import serializers as rest_serializers

from user import models
from user.service.social_login.models import platforms


class UserDetailSerializer(dj_auth_serializers.UserDetailsSerializer):
    def create(self, validated_data):
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

    def save(self, request) -> models.User:
        user = super().save(request)
        user.birthdate = self.validated_data.get("birthdate")
        user.save()
        return user

    def update(self, instance, validated_data):
        raise NotImplementedError("`update()` must be implemented.")

    def create(self, validated_data):
        raise NotImplementedError("`create()` must be implemented.")

    class Meta:
        model = models.User
        fields = ["username", "email", "password1", "password2", "birthdate", "image"]


class SocialLoginSerializer(dj_reg_serializers.SocialLoginSerializer):
    platform: platforms.SocialPlatform = None

    def _get_request(self):
        return self.context.get("request")

    def get_social_login(self, adapter, app, token, response):
        social_login = super().get_social_login(adapter, app, token, response)
        for email in social_login.email_addresses:
            if models.User.objects.filter(email=email):
                user = models.User.objects.get(email=email)
                if not allauth_models.SocialAccount.objects.filter(user=user, provider=self.platform):
                    raise ValueError("Email is duplicated.")
        return social_login

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
