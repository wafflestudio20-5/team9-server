from django import urls
from django.contrib import admin

from drf_spectacular import views

urlpatterns = [
    urls.path("docs/json/", views.SpectacularJSONAPIView.as_view(), name="schema-json"),
    urls.path("schema/", views.SpectacularAPIView.as_view(), name="schema"),
    urls.path(
        "docs/swagger/",
        views.SpectacularSwaggerView.as_view(url_name="schema-json"),
        name="swagger-ui",
    ),
    urls.path("admin/", admin.site.urls),
    urls.path("api/v1/user/", urls.include("user.urls")),
    urls.path("api/v1/calendar/", urls.include("calendar_j.urls")),
]
