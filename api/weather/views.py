from rest_framework import viewsets, filters
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import WeatherData, WeatherStats, YieldStats
from .serializers import (
    WeatherDataSerializer,
    WeatherStatsSerializer,
    YieldStatsSerializer,
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class WeatherDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WeatherData.objects.all().order_by("date")
    serializer_class = WeatherDataSerializer
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = ["station_id", "date"]
    ordering_fields = ["date"]
    pagination_class = StandardResultsSetPagination

    def retrieve(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)


class WeatherStatsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WeatherStats.objects.all().order_by("year")
    serializer_class = WeatherStatsSerializer
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = ["station_id", "year"]
    ordering_fields = ["year"]
    pagination_class = StandardResultsSetPagination

    def retrieve(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)


class YieldStatsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = YieldStats.objects.all().order_by("year")
    serializer_class = YieldStatsSerializer
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = ["year"]
    ordering_fields = ["year"]
    pagination_class = StandardResultsSetPagination

    def retrieve(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)
