from user.service.social_login import platforms


class SocialLoginExceptionMessageMixin:
    platform: platforms.SocialPlatform

    @property
    def invalid_token(self) -> str:
        return f"Invalid {self.platform} token."

    @property
    def invalid_access_token(self) -> str:
        return f"Invalid {self.platform} access_token to get user profile."

    @property
    def invalid_social_user(self) -> str:
        return f"Invalid email. Your email is not registered as {self.platform} social user in our service."

    @property
    def fail_to_sign_up(self) -> str:
        return "Fail to sign up. Pleas retry."

    @property
    def fail_to_login(self) -> str:
        return "Fail to login. Please retry."
