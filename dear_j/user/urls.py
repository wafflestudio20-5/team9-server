from django import urls

from user import views

urlpatterns = [
    urls.path("registration/", views.UserRegistrationView.as_view()),
    urls.path("login/", views.UserLoginView.as_view()),
    urls.path("logout/", views.UserLogoutView.as_view()),
]
