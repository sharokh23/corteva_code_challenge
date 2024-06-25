from django.urls import path
from .views import WeatherDataViewSet, WeatherStatsViewSet, YieldStatsViewSet


urlpatterns = [
    path("", WeatherDataViewSet.as_view({"get": "list"}), name="weather-data"),
    path("stats/", WeatherStatsViewSet.as_view({"get": "list"}), name="weather-stats"),
    path("yields/", YieldStatsViewSet.as_view({"get": "list"}), name="yield-stats"),
]
