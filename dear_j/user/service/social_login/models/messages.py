from user.service.social_login.models import platforms


class SocialLoginExceptionMessageMixin:
    platform: platforms.SocialPlatform

    @property
    def invalid_token(self) -> str:
        return f"Invalid {self.platform} token."

    @property
    def invalid_email_error(self) -> str:
        return f"Invalid Social Login. Your email is already registered, but not as {self.platform}."
