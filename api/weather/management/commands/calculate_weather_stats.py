import logging
import time
from django.core.management.base import BaseCommand
from django.db.models import Avg, Sum
from weather.models import WeatherData, WeatherStats

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Calculate weather statistics"

    def handle(self, *args, **options):
        start_time = time.time()
        logger.info("Starting weather analysis")
        self.stdout.write("Starting weather analysis")

        stations = WeatherData.objects.values_list("station_id", flat=True).distinct()

        for station_count, station in enumerate(stations, start=1):
            self.stdout.write(
                f"Processing station {station_count:,}/{len(stations):,}", ending="\r"
            )

            for year in range(1985, 2015):
                yearly_data = WeatherData.objects.filter(
                    station_id=station, date__year=year
                )
                avg_max_temp = yearly_data.aggregate(Avg("max_temp"))["max_temp__avg"]
                avg_max_temp = (
                    avg_max_temp / 10.0 if avg_max_temp is not None else None
                )  # Needs to be converted Celsius
                avg_min_temp = yearly_data.aggregate(Avg("min_temp"))["min_temp__avg"]
                avg_min_temp = (
                    avg_min_temp / 10.0 if avg_min_temp is not None else None
                )  # Needs to be converted Celsius
                total_precipitation = yearly_data.aggregate(Sum("precipitation"))[
                    "precipitation__sum"
                ]
                total_precipitation = (
                    total_precipitation / 100.0
                    if total_precipitation is not None
                    else None
                )  # Needs to be converted from millimeters to centimeters

                WeatherStats.objects.update_or_create(
                    station_id=station,
                    year=year,
                    defaults={
                        "avg_max_temp": avg_max_temp,
                        "avg_min_temp": avg_min_temp,
                        "total_precipitation": total_precipitation,
                    },
                )

        end_time = time.time()
        duration = end_time - start_time
        logger.info("Successfully calculated weather statistics")
        logger.info(f"Data analysis completed in {duration:.2f} seconds")
        logger.info(f"Data analysis start time: {start_time} | end time: {end_time}")
        self.stdout.write(
            self.style.SUCCESS("Successfully calculated weather statistics")
        )
        self.stdout.write(
            f"Data analysis start time: {start_time} | end time: {end_time}"
        )
        self.stdout.write(f"Data analysis completed in {duration:.2f} seconds")
