from django import urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from drf_spectacular import views

urlpatterns = [
    urls.path("admin/", admin.site.urls),
    urls.path("api/v1/user/", urls.include("user.urls")),
    urls.path("api/v1/calendar/", urls.include("calendar_j.urls")),
    urls.path("api/v1/social/", urls.include("social.urls")),
    urls.path("docs/", urls.include("documentation.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
