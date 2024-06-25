from rest_framework import serializers
from .models import WeatherData, WeatherStats, YieldStats


class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = "__all__"


class WeatherStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherStats
        fields = "__all__"


class YieldStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = YieldStats
        fields = "__all__"
