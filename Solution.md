# Corteva Coding Challenge Solution

## Problem 1 - Data Modeling

When considering the requirements and constraints of this coding exercise, I chose Postgres as the most suitable database choice. One reason was becausePostgreSQL offers advanced features such as transactional support and extensive indexing capabilities. These features really help when dealing with the large volumes of weather data.

Another reason why I chose Postgres was because as the project grows and more weather data is ingested, the database's ability to scale becomes important. Postgres supports both vertical and horizontal scaling, making it a no-brainer for handling increasing data volumes and user load.

Lastly, Postgres is well-supported by Django's ORM. It has seamless integration and makes it easier to define and interact with the data model. This compatibility simplifies development and ensures that we can leverage Django features for data manipulation and querying.

### Data Model Design

For this project I used Django's native ORM and the data model for representing the weather data records is as follows:

#### Weather Data:

```python
class WeatherData(models.Model):
    station_id = models.CharField(max_length=12)
    date = models.DateField()
    max_temp = models.IntegerField(null=True)
    min_temp = models.IntegerField(null=True)
    precipitation = models.IntegerField(null=True)

    class Meta:
        ordering = ["date"]
        # unique_together is used to ensure that each weather data record is unique
        # for a given station and date. This prevents duplicate records for the
        # same station and date from being entered into the database.
        unique_together = ("station_id", "date")
```

#### Weather Stats:

````python
class WeatherStats(models.Model):
    station_id = models.CharField(max_length=12)
    year = models.IntegerField()
    avg_max_temp = models.FloatField(null=True)
    avg_min_temp = models.FloatField(null=True)
    total_precipitation = models.FloatField(null=True)

    class Meta:
        ordering = ["year"]
        # unique_together is used to ensure that each weather data record is unique
        # for a given station and date. This prevents duplicate records for the
        # same station and date from being entered into the database.
        unique_together = ("station_id", "year")
    ```
````

## Problem 2 - Ingestion

I chose to use Django commands to handle the ingestion of weather data because there is ease of management with it being in the same project. This made it so that I could leverage the Django ORM to ensure data integrity and avoid duplication by using methods such as `update_or_create`. Additionally, I could use any Django feature within the command making it a seamless integration with the rest of the app/API.

The approach that I took to ingest the data was relatively simple and ensures efficient and reliable data ingestion while handling potential duplicates gracefully. First, the command locates all text files in a specified directory and reads each file line by line in batches of 10,000 for efficiency purposes. For each line, it extracts the weather data (date, maximum temperature, minimum temperature, and precipitation), replacing missing values with `None`. It then creates WeatherData objects and stores them in a list. To optimize performance, the command uses `bulk_create` with a `batch_size=1000` and `ignore_conflicts=True` to insert all records at once, ignoring duplicates, so as not overload the database with too many queries. Finally, it logs the successful completion of the process and outputs a success message to the console.

The full code can be found in `/api/weather/management/commands/ingest_weather_data.py`

## Problem 3 - Data Analysis

For the data analysis step I used Django commands as well for the same reasoning as the ingestion.

The approach that I chose begins by retrieving a list of unique station IDs from the WeatherData model and iterates through each station. For each station, it further iterates through each year within the specified range. It filters the weather data for the given station and year, calculates the average maximum temperature, average minimum temperature, and total precipitation for that year using Django's ORM. Whilst it is calculating that data, I also account for the unit difference as per the `Overview.md`. Finally, the calculated statistics are then stored in the WeatherStats model using `update_or_create`, ensuring that existing records are updated while avoiding duplicates.

Another part of the challenge was to find correlations between yield_data and the weather. Using pandas I simply made a correlation table based off the year.

|                     | avg_max_temp    | avg_min_temp    | total_precipitation | yield_value|
|---------------------|-----------------|-----------------|---------------------|------------|
| avg_max_temp        | 1.000000        | 0.685938        | 0.035642            | -0.084553  |
| avg_min_temp        | 0.685938        | 1.000000        | 0.499862            | -0.048002  |
| total_precipitation | 0.035642        | 0.499862        | 1.000000            | 0.091397   |
| yield_value         | -0.084553       | -0.048002       | 0.091397            | 1.000000   |

The results can be interpreted as follows
* `avg_max_temp` and `yield_value` have a weak negative correlation of -0.084553. This suggests that higher average maximum temperatures might be slightly associated with lower crop yields.
* `avg_min_temp` and `yield_value` also show a weak negative correlation of -0.048002, indicating a similar trend where higher average minimum temperatures might be associated with lower crop yields.
* `total_precipitation` and `yield_value` have a positive correlation of 0.091397. This suggests that higher total precipitation may be associated with slightly higher crop yields, though the correlation is relatively weak.

The full code can be found in `/api/weather/management/commands/calculate_weather_stats.py` and `/api/weather/management/commands/correlations_weather_yield.py`

## Problem 4 - REST API

For this project, I chose Django because of it's "batteries-included" framework that makes my life so much easier. Given the time frame as well, there were many things that I didn't have to develop like Django's ORM which significantly simplifies database interactions. Though I am comfortable writing raw SQL, the ORM makes it easy to get the data using regular Python.

For creating RESTful APIs, I utilized the Django REST Framework because it seamlessly integrates with Django. I was able to save countless hours by using serializers and viewsets. Viewsets in DRF enable quick creation and management endpoints for the models which didn't require me to manually code those endpoints/methods and ensured consistent and maintainable API design.

This combination of Docker, Django, and DRF really allows for rapid development and deployment of a scalable and maintainable API so it made sense for me to utilize it in this project.

To see more info of how to run the application and test, please go to the `README.md`.

## Extra Credit - Deployment

### Database

For the database I would utilize Amazon Relational Database Service wherein I would simply create a PostgresSQL database instance. Then I would ensure the RDS instance is secured with appropriate network and database security groups to control access.

I would use RDS because it can scale horizontally and vertically based on demand. It is also a managed service which means that Amazon manages infrastructure, ensuring high availability and reliability. Lastly, there are a lot of security concerns with data and RDS provides those out of the box (ie. VPC, security groups, IAM roles, and encryption options).

### API

Because the application is fully Dockerized I would use Amazon Elastic Container Service, potentially with Fargate to manage scaling. Additionally, I would like to have a CI/CD pipeline for this so I would create a new CodePipeline wherein upon a code change the images would be built and pushed to ECR and then deployed.

I chose ECS because it can scale horizontally and vertically based on demand. If Fargate is enabled, it is also a managed service which means that Amazon manages infrastructure, ensuring high availability and reliability. Lastly, ECS provides security features such as VPC, security groups, IAM roles, and SSL.

### Data Ingestion

Data ingestion is a more complex topic. If the ingestion was continuously happening then I would consider something like scheduling jobs wherein I would define scheduled tasks in ECS using Scheduled Tasks or CloudWatch Events to trigger ECS tasks at specified intervals. The exact same result can be achieved using Amazon Lambda functions with scheduled triggers to execute the data ingestion code periodically.

If the data needs to simply be ingested once, then I would consider just SSH'ing into the API container and running the Django commands that are in the repo. If I was trying to impress someone or just use Amazon, I would consider uploading all the files to S3 and running a Amazon Glue job to populate the database.

### MISC

I always like to be able to get the latest updates for the apps I deploy and even potentially receive alarms. As such, I would also include monitoring and Logging using Amazon CloudWatch. This would enable monitoring of container logs, metrics, and alarms.