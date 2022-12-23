from django import urls

app_name = 'user'

urlpatterns = [
    urls.path("", urls.include("dj_rest_auth.urls")),
    urls.path("registration/",
              urls.include("dj_rest_auth.registration.urls"),
              name='registration'),
]
