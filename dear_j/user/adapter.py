from allauth.account import adapter
from user import models


class AccountAdapter(adapter.DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=False):
        user = super().save_user(request, user, form, commit)
        data = form.cleaned_data
        user.email = data.get("email")
        user.birthday = data.get("birthday")
        user.username = data.get("username")
        user.save()
        return user
