import logging
import pandas as pd
from django.core.management.base import BaseCommand
from weather.models import WeatherStats, YieldStats

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Find correlations between weather and yield statistics"

    def handle(self, *args, **options):
        weather_stats_queryset = WeatherStats.objects.all()
        yield_stats_queryset = YieldStats.objects.all()

        weather_stats_df = pd.DataFrame(list(weather_stats_queryset.values()))
        yield_stats_df = pd.DataFrame(list(yield_stats_queryset.values()))

        # Merge datasets on 'year'
        merged_data = pd.merge(weather_stats_df, yield_stats_df, on="year")

        # Calculate correlation matrix
        correlation_matrix = merged_data[
            ["avg_max_temp", "avg_min_temp", "total_precipitation", "yield_value"]
        ].corr()

        # Print correlation matrix
        print(correlation_matrix)
