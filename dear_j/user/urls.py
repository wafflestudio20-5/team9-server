from django import urls

urlpatterns = [
    urls.path("", urls.include("dj_rest_auth.urls")),
    urls.path("registration/",
              urls.include("dj_rest_auth.registration.urls")),
]
