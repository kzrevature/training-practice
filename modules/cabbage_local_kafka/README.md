# Local Kafka Setup - 'Cabbage'

Basic instructions for how to run a local Kafka broker using Docker
and test it against Python.

### Prerequisites

Docker 28.5.1, Python 3.11.9

### Running Kafka

Create a container from the `apache/kafka` image on dockerhub.
Note that port 9092 (used by Kafka) is mapped between host and container.

```docker run -d --name cabbage_broker -p 9092:9092 apache/kafka:3.9.1-rc0```

The broker is now running.

### Producer/Consumer Setup (Python)

Refer to `consumer.py`, `producer.py`, and `create_topic.py`.
They should be pretty self-explanatory.

### Misc

The [docker quickstart](https://hub.docker.com/r/apache/kafka)
and [pypi project page](https://pypi.org/project/kafka-python/#description)
were very helpful.
Everything works out of the box.
