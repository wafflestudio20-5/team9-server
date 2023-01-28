from dj_rest_auth import views as dj_auth_views
from dj_rest_auth.registration import views as dj_reg_views
from rest_framework import generics

from user import models
from user import permissions
from user import serializers


class UserRegistrationView(dj_reg_views.RegisterView):
    serializer_class = serializers.RegisterSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get("email")
        birthdate = request.data.get("birthdate")
        image = request.data.get("image")
        response = super().create(request, *args, **kwargs)
        user = models.User.objects.get(email=email)
        user.birthdate = birthdate
        if image is None:
            user.image = "https://dear-j-blog.s3.ap-northeast-2.amazonaws.com/user/user.png"
        else:
            user.image = image
        user.save()
        return response

class UserLoginView(dj_auth_views.LoginView):
    pass


class UserLogoutView(dj_auth_views.LogoutView):
    pass

class UserPasswordChangeView(dj_auth_views.PasswordChangeView):
    pass

class UserProfileView(dj_auth_views.UserDetailsView):
    serializer_class = serializers.UserDetailSerializer
    permission_classes = (permissions.UserIdentification,)

    def get_object(self) -> models.User:
        return self.request.user
