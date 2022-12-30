"""dear_j URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import urls
from django.contrib import admin

from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularJSONAPIView
from drf_spectacular.views import SpectacularRedocView
from drf_spectacular.views import SpectacularSwaggerView

urlpatterns = [
    urls.path("docs/json/", SpectacularJSONAPIView.as_view(), name="schema-json"),
    urls.path("schema/", SpectacularAPIView.as_view(), name="schema"),
    urls.path(
        "docs/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema-json"),
        name="swagger-ui",
    ),
    urls.path("admin/", admin.site.urls),
    urls.path("api/v1/user/", urls.include("user.urls")),
]
