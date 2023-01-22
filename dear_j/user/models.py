from django.contrib.auth import models as auth_models
from django.db import models as db_models

from user import managers


class User(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    objects = managers.UserManager()
    email = db_models.EmailField(
        max_length=255,
        unique=True,
    )
    username = db_models.CharField(max_length=30)
    birthdate = db_models.DateField(null=True)
    birthyear = db_models.IntegerField(null=True)
    birthday = db_models.IntegerField(null=True)
    is_active = db_models.BooleanField(default=True)
    is_admin = db_models.BooleanField(default=False)
    is_superuser = db_models.BooleanField(default=False)
    is_staff = db_models.BooleanField(default=False)
    created_at = db_models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.email)
