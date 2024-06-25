# Corteva Coding Challenge

## Setup

The application is fully containerized so we will want to first bring up the containers

```sh
docker compose up
```

Run the database migrations

```sh
docker exec -it corteva_code_challenge-api-1 python manage.py migrate
```

Import sample data and calculate the statistics

```sh
docker exec -it corteva_code_challenge-api-1 python manage.py ingest_weather_data
docker exec -it corteva_code_challenge-api-1 python manage.py ingest_yield_data
docker exec -it corteva_code_challenge-api-1 python manage.py calculate_weather_stats
docker exec -it corteva_code_challenge-api-1 python manage.py correlations_weather_yield # Optional
```

Note: Both of these processes may take a while as it is going through over a million records.

## API calls/docs
Once the containers come up, you can navigate to `http://localhost:8000/api/docs/` and see a full set of the APIs available and all their documentations

## Unit Tests

```sh
docker exec -it corteva_code_challenge-api-1 python manage.py test
```
