from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Verbumdei Management System (VMS) API",
        default_version='v1',
        description="API documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="mail@verbumdeiacademy.com"),
        license=openapi.License(name="Verbumdei Academy"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(
        r"^$", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
    path("staff/", include("staff.urls")),
    path("student/", include("student.urls")),
    path("program/", include("program.urls")),
    path("inventory/", include("inventory.urls")),
    path("parent/", include("parent.urls")),
    path("class/", include("grade.urls")),
    path("payment/", include("payment.urls")),
    path("sub-admin/", include("subadmins.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
