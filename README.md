# Kafka Spark Flink Container

This is an example project setup with Kafka, Spark and Flink. It contains:
* A Kafka producer sending data over a topic,
* A consumer processing the data stream using Spark with Structured Streaming,
* A consumer processing the data stream using Flink with the Table API,
* A docker-compose file to start up and shut down all containers.

In this example, the data is sent in JSON format containing names and ages of users. Both consumers compute and print the average age of the users over a sliding time window. 
The Python APIs of all frameworks are used.

This setup can be used for easily developing and testing your own Spark or Flink jobs that need a data stream.

## Requirements
* Docker
* Docker Compose

## How to run
To build and start:

```
docker-compose up --build
```
Add the `-d` flag to hide the output. To view the output of a specific container, check the names of running containers with `docker ps` and then use `docker logs -f <container_name>`.

To shut down:

```
docker-compose down -v
```

To restart only one container after making any changes:

```
docker-compose up --build <container_name>
```
For example, `docker-compose up --build consumer_spark`.

## How to use
In the docker-compose, you can specify the following variables:
* Name of the data source that should be sent over the Kafka topic. You can replace this by any CSV file with headers.
* Name of the Kafka topic.
* The time interval that the Kafka producer uses to send data.

You can write your Spark or Flink jobs in the respective scripts and run the corresponding Docker container to start the job.

The Spark UI is accessible through http://localhost:4040.

### Adding new data
To add new data, add a CSV file with headers to the data/ directory, put the filename in the 'DATA' environment variable in docker-compose.yml, and rebuild the container `producer`. You can then adjust the schemas and jobs of the consumer(s).
