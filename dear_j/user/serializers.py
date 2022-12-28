from rest_framework import serializers as rest_serializers

import dj_rest_auth
from dj_rest_auth import serializers as dj_auth_serializers
from dj_rest_auth.registration import serializers as dj_regist_serializers
from user import adapter
from user import models


class CustomUserDetailSerializer(dj_auth_serializers.UserDetailsSerializer):
    def create(self, validated_data):
        user = models.User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get("email", instance.email)
        instance.username = validated_data.get("username", instance.username)
        instance.birthday = validated_data.get("birthday", instance.birthday)
        instance.save()
        return instance

    class Meta(dj_auth_serializers.UserDetailsSerializer.Meta):
        fields = dj_auth_serializers.UserDetailsSerializer.Meta.fields + (
            "email",
            "birthday",
            "username",
        )


class CustomRegisterSerializer(dj_regist_serializers.RegisterSerializer):
    email = rest_serializers.EmailField(max_length=255)
    username = rest_serializers.CharField(max_length=30)
    birthday = rest_serializers.DateField()

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict["email"] = self.validated_data.get("email", "null")
        data_dict["username"] = self.validated_data.get("username", "null")
        data_dict["birthday"] = self.validated_data.get("birthday", "null")
        return data_dict

    def create(self, validated_data):
        user = models.User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get("email", instance.email)
        instance.username = validated_data.get("username", instance.username)
        instance.birthday = validated_data.get("birthday", instance.birthday)
        instance.save()
        return instance

    class Meta:
        model = models.User
        fields = ["username", "email", "password1", "password2", "birthday"]
