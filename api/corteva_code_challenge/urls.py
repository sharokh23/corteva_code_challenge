from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from weather.views import WeatherDataViewSet, WeatherStatsViewSet, YieldStatsViewSet

# Django REST Framework router
router = routers.DefaultRouter()
router.register(r"weather-data", WeatherDataViewSet)
router.register(r"weather-stats", WeatherStatsViewSet)
router.register(r"yield-stats", YieldStatsViewSet)

# Swagger/OpenAPI documentation view configuration
schema_view = get_schema_view(
    openapi.Info(
        title="Weather and Yield API",
        default_version="v1",
        description="API for managing weather and yield statistics",
        terms_of_service="",
        contact=openapi.Contact(email=""),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
)

urlpatterns = [
    path("admin/", admin.site.urls),  # Django admin URLs
    path("api/", include(router.urls)),  # Correct usage of router.urls
    path(
        "api/docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),  # Swagger documentation
]
