import datetime

from django.contrib.auth import base_user

from user import models


class UserManager(base_user.BaseUserManager):
    def create_user(self, email: str, password: str, birthdate: str, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        user = self.model(email=self.normalize_email(email), birthdate=birthdate)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, password: str, **extra_fields):
        birthdate_str = datetime.datetime.now().strftime("%Y-%m-%d")

        user = self.create_user(email=self.normalize_email(email), birthdate=birthdate_str, password=password)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
