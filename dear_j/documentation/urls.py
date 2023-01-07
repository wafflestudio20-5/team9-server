from django import urls

from drf_spectacular import views

urlpatterns = [
    urls.path("json/", views.SpectacularJSONAPIView.as_view(), name="schema-json"),
    urls.path("schema/", views.SpectacularAPIView.as_view(), name="schema"),
    urls.path("swagger/", views.SpectacularSwaggerView.as_view(url_name="schema-json"), name="swagger-ui"),
]
