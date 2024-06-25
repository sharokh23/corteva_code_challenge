import os
import glob
import logging
import time
from django.core.management.base import BaseCommand
from weather.models import WeatherData

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Ingest weather data from text files into the database"

    def handle(self, *args, **options):
        start_time = time.time()
        logger.info("Starting data ingestion")
        self.stdout.write("Starting data ingestion")
        data_path = "weather/management/commands/wx_data"
        files = glob.glob(os.path.join(data_path, "*.txt"))

        # Prepare a list to hold WeatherData instances to be created
        weather_data_list = []

        total_files = len(files)
        record_count = 0

        for file_count, file_path in enumerate(files, start=1):
            self.stdout.write(
                f"Processing file {file_count}/{total_files}", ending="\r"
            )

            weather_data_list = []

            with open(file_path, "r") as file:
                while True:
                    lines = file.readlines(
                        10000
                    )  # Read 10,000 lines at a time for efficiency
                    if not lines:
                        break

                    for line in lines:
                        station_id = os.path.basename(file_path).split(".")[0]
                        date, max_temp, min_temp, precipitation = line.strip().split(
                            "\t"
                        )

                        # Replace missing values with None
                        max_temp = int(max_temp) if max_temp != "-9999" else None
                        min_temp = int(min_temp) if min_temp != "-9999" else None
                        precipitation = (
                            int(precipitation) if precipitation != "-9999" else None
                        )

                        weather_data_list.append(
                            WeatherData(
                                station_id=station_id,
                                date=date,
                                max_temp=max_temp,
                                min_temp=min_temp,
                                precipitation=precipitation,
                            )
                        )

                    # Bulk create WeatherData instances in batches of 1,000 for efficiency
                    if weather_data_list:
                        WeatherData.objects.bulk_create(
                            weather_data_list, batch_size=1000, ignore_conflicts=True
                        )
                        record_count += len(weather_data_list)
                        weather_data_list = []

        end_time = time.time()
        duration = end_time - start_time
        logger.info(f"Successfully ingested {record_count:,} records of weather data")
        logger.info(f"Data ingestion start time: {start_time} | end time: {end_time}")
        logger.info(f"Data ingestion completed in {duration:.2f} seconds")
        self.stdout.write(
            f"Data ingestion start time: {start_time} | end time: {end_time}"
        )
        self.stdout.write(f"Data ingestion completed in {duration:.2f} seconds")
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully ingested {record_count:,} records of weather data"
            )
        )
