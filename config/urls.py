from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.views.generic import RedirectView
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView


def health_check(request):
    """Simple health check endpoint for monitoring"""
    return JsonResponse({"status": "ok", "message": "Estate Management API is running"})


urlpatterns = [
    path("", RedirectView.as_view(url="/api/health/", permanent=False)),
    path("api/health/", health_check, name="health-check"),
    path(
        "redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="schema-redoc",
    ),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/v1/auth/", include("djoser.urls")),
    path("api/v1/auth/", include("core_apps.users.urls")),
    path("api/v1/profiles/", include("core_apps.profiles.urls")),
    path("api/v1/apartments/", include("core_apps.apartments.urls")),
    path("api/v1/issues/", include("core_apps.issues.urls")),
    path("api/v1/reports/", include("core_apps.reports.urls")),
    path("api/v1/ratings/", include("core_apps.ratings.urls")),
    path("api/v1/posts/", include("core_apps.posts.urls")),
]

admin.site.site_header = "Alpha Apartments Admin"
admin.site.site_title = "Alpha Apartments Admin Portal"
admin.site.index_title = "Welcome to Alpha Apartments Admin Portal"
