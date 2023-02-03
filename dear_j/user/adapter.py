from allauth.account import adapter

from user import models


class AccountAdapter(adapter.DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True) -> models.User:
        user: models.User = super().save_user(request, user, form, commit)
        data = form.cleaned_data
        user.birthdate = data.get("birthdate")
        if commit:
            user.save()
        return user
