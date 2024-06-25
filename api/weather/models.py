from django.db import models


class WeatherData(models.Model):
    station_id = models.CharField(max_length=12)
    date = models.DateField()
    max_temp = models.IntegerField(null=True)
    min_temp = models.IntegerField(null=True)
    precipitation = models.IntegerField(null=True)

    class Meta:
        # unique_together is used to ensure that each weather data record is unique
        # for a given station and date. This prevents duplicate records for the
        # same station and date from being entered into the database.
        unique_together = ("station_id", "date")


class WeatherStats(models.Model):
    station_id = models.CharField(max_length=12)
    year = models.IntegerField()
    avg_max_temp = models.FloatField(null=True)
    avg_min_temp = models.FloatField(null=True)
    total_precipitation = models.FloatField(null=True)

    class Meta:
        # unique_together is used to ensure that each weather data record is unique
        # for a given station and date. This prevents duplicate records for the
        # same station and date from being entered into the database.
        unique_together = ("station_id", "year")


class YieldStats(models.Model):
    year = models.IntegerField(unique=True)
    yield_value = models.IntegerField()
