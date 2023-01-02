import jwt
from allauth.account import adapter
from allauth.socialaccount.providers.oauth2 import client

from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.google import provider


class CustomAccountAdapter(adapter.DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=False):
        user = super().save_user(request, user, form, commit)
        data = form.cleaned_data
        user.email = data.get("email")
        user.birthday = data.get("birthday")
        user.username = data.get("username")
        user.save()
        return user


class CustomGoogleAdapter(google_view.GoogleOAuth2Adapter):
    provider_id = provider.GoogleProvider.id
    access_token_url = "https://oauth2.googleapis.com/token"
    authorize_url = "https://accounts.google.com/o/oauth2/v2/auth"
    id_token_issuer = "https://accounts.google.com"

    def complete_login(self, request, app, token, response, **kwargs):
        print(response)
        print(type(response))
        try:
            identity_data = jwt.decode(
                response,  # response["id_token"],
                options={
                    "verify_signature": False,
                    "verify_iss": True,
                    "verify_aud": True,
                    "verify_exp": True,
                },
                issuer=self.id_token_issuer,
                audience=app.client_id,
            )
        except jwt.PyJWTError as e:
            raise client.OAuth2Error("Invalid id_token") from e
        login = self.get_provider().sociallogin_from_response(request, identity_data)
        print(login)
        return login
