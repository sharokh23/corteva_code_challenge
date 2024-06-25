from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from weather.models import WeatherData, WeatherStats


class WeatherDataAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.weather_data = WeatherData.objects.create(
            station_id="USC00338822",
            date="2024-01-01",
            max_temp=25,
            min_temp=15,
            precipitation=10,
        )
        self.weather_data = WeatherData.objects.create(
            station_id="USC00338822",
            date="2024-01-02",
            max_temp=27,
            min_temp=17,
            precipitation=12,
        )
        self.weather_data = WeatherData.objects.create(
            station_id="USC00253035",
            date="2024-01-01",
            max_temp=24,
            min_temp=12,
            precipitation=11,
        )

        self.weather_data = WeatherStats.objects.create(
            station_id="USC00338822",
            year="2024",
            avg_max_temp=25.5,
            avg_min_temp=14.5,
            total_precipitation=22,
        )
        self.weather_data = WeatherStats.objects.create(
            station_id="USC00253035",
            year="2024",
            avg_max_temp=24,
            avg_min_temp=12,
            total_precipitation=11,
        )

    def test_get_weather_data_list(self):
        url = reverse("weather-data")
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )  # Check if status code is correct
        self.assertEqual(
            response.data["count"], 3
        )  # Check if correct number of objects are returned

    def test_get_weather_data_station(self):
        url = reverse("weather-data")
        response = self.client.get(url, {"station_id": "USC00253035"})
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )  # Check if status code is correct
        self.assertEqual(
            response.data["count"], 1
        )  # Check if correct number of objects are returned
        self.assertEqual(
            response.data["results"][0]["station_id"], "USC00253035"
        )  # Check if station ID is correct

    def test_get_weather_data_fake_station(self):
        url = reverse("weather-data")
        response = self.client.get(url, {"station_id": "FAKE STATION"})
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )  # Check if status code is correct
        self.assertEqual(
            response.data["count"], 0
        )  # Check if correct number of objects are returned

    def test_get_weather_data_date(self):
        url = reverse("weather-data")
        response = self.client.get(url, {"date": "2024-01-01"})
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )  # Check if status code is correct
        self.assertEqual(
            response.data["count"], 2
        )  # Check if correct number of objects are returned
        self.assertEqual(
            response.data["results"][0]["date"], "2024-01-01"
        )  # Check if date is correct

    def test_get_weather_data_station_date(self):
        url = reverse("weather-data")
        response = self.client.get(
            url, {"station_id": "USC00338822", "date": "2024-01-02"}
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )  # Check if status code is correct
        self.assertEqual(
            response.data["count"], 1
        )  # Check if correct number of objects are returned
        self.assertEqual(
            response.data["results"][0]["station_id"], "USC00338822"
        )  # Check if station ID is correct
        self.assertEqual(
            response.data["results"][0]["date"], "2024-01-02"
        )  # Check if date is correct

    def test_get_weather_stats_list(self):
        url = reverse("weather-stats")
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )  # Check if status code is correct
        self.assertEqual(
            response.data["count"], 2
        )  # Check if correct number of objects are returned

    def test_get_weather_stats_station(self):
        url = reverse("weather-stats")
        response = self.client.get(url, {"station_id": "USC00253035"})
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )  # Check if status code is correct
        self.assertEqual(
            response.data["count"], 1
        )  # Check if correct number of objects are returned
        self.assertEqual(
            response.data["results"][0]["station_id"], "USC00253035"
        )  # Check if station ID is correct

    def test_get_weather_stats_fake_station(self):
        url = reverse("weather-stats")
        response = self.client.get(url, {"station_id": "FAKE STATION"})
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )  # Check if status code is correct
        self.assertEqual(
            response.data["count"], 0
        )  # Check if correct number of objects are returned

    def test_get_weather_stats_year(self):
        url = reverse("weather-stats")
        response = self.client.get(url, {"year": "2024"})
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )  # Check if status code is correct
        self.assertEqual(
            response.data["count"], 2
        )  # Check if correct number of objects are returned
        self.assertEqual(
            response.data["results"][0]["year"], 2024
        )  # Check if date is correct

    def test_get_weather_stats_station_date(self):
        url = reverse("weather-stats")
        response = self.client.get(url, {"station_id": "USC00338822", "year": "2024"})
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )  # Check if status code is correct
        self.assertEqual(
            response.data["count"], 1
        )  # Check if correct number of objects are returned
        self.assertEqual(
            response.data["results"][0]["station_id"], "USC00338822"
        )  # Check if station ID is correct
        self.assertEqual(
            response.data["results"][0]["year"], 2024
        )  # Check if date is correct

    # Testing Errors

    def test_invalid_weather_data_http_method(self):
        url = reverse("weather-data")
        response = self.client.post(
            url,
            {
                "station_id": "USC00338822",
                "date": "2024-01-02",
                "max_temp": 27,
                "min_temp": 12,
                "precipitation": 8,
            },
        )
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )  # Check if status code is correct

    def test_invalid_weather_data_date(self):
        url = reverse("weather-data")
        response = self.client.get(url, {"date": "NOT A DATE"})
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )  # Check if status code is correct

    def test_invalid_weather_stats_http_method(self):
        url = reverse("weather-stats")
        response = self.client.post(
            url,
            {
                "station_id": "USC00338822",
                "date": "2024-01-02",
                "max_temp": 27,
                "min_temp": 12,
                "precipitation": 8,
            },
        )
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )  # Check if status code is correct

    def test_invalid_weather_stats_date(self):
        url = reverse("weather-stats")
        response = self.client.get(url, {"year": "NOT A YEAR"})
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )  # Check if status code is correct
