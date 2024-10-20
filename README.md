# Kafka-FastAPI Application

This project demonstrates a Kafka producer and consumer implementation using FastAPI. The application consists of two main components: a producer service and a consumer service, both built with FastAPI and interacting with Apache Kafka.

## Project Structure

The project is organized into two main directories:

- `producer/`: Contains the Kafka producer service
- `consumer/`: Contains the Kafka consumer service

Each service has its own Dockerfile, requirements.txt, and application code.

## Prerequisites

- Docker and Docker Compose
- Apache Kafka
- Python 3.9+

## Setup

1. Clone this repository:
   ```
   git clone git@github.com:matheusses/kafka-demo.git
   cd kafka-app
   ```

2. Create `.env` files in both `producer/app/` and `consumer/app/` directories with the necessary configuration. Example:

   ```
   KAFKA_BOOTSTRAP_SERVERS=kafka:9092
   TOPIC=my-topic
   CLIENT_ID=my-client
   GROUP_ID=my-group
   AUTO_OFFSET_RESET=earliest
   ```

   Adjust the values according to your Kafka setup.

3. Build and run the Docker containers:
   ```
   docker-compose up --build
   ```

## Usage

### Producer

- http://localhost:8000/docs

### Consumer

- http://localhost:8001/docs

Show consumer logs:
```
docker logs  python-app-consumer
```
