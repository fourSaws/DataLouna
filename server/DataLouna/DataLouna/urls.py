from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from .yasg import urlpatterns as doc_urls

schema_view_private = get_schema_view(
    openapi.Info(
        title="DataLouna",
        default_version="v1",
        description="Doc API",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    urlconf="LounaAdmin.private_urls",
)
schema_view = get_schema_view(
    openapi.Info(
        title="DataLouna",
        default_version="v1",
        description="Doc API",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    urlconf="DataLounaNotifications.public_urls",
)
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("LounaAdmin.private_urls")),
    path("", include("DataLounaNotifications.public_urls")),
    path(
        "swagger(^?P<format>\.json|\.yaml$)",
        schema_view_private.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "private_swagger/",
        schema_view_private.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "private_swagger/",
        schema_view_private.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    path(
        "swagger(^?P<format>\.json|\.yaml$)",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "public_swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "public_redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    path(
        "private_redoc/",
        schema_view_private.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += doc_urls
