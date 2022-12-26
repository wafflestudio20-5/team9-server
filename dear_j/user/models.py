from django.contrib.auth import models as auth_models
from django.db import models as db_models

from user import managers


class User(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    objects = managers.UserManager()
    email = db_models.EmailField(
        max_length=255,
        unique=True,
    )
    birthday = db_models.DateField()
    is_active = db_models.BooleanField(default=True)
    is_admin = db_models.BooleanField(default=False)
    is_superuser = db_models.BooleanField(default=False)
    is_staff = db_models.BooleanField(default=False)
    date_joined = db_models.DateTimeField(auto_now_add=True)
    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.email)
