# Consume Local Kafka with Spark Structured Streaming - 'Elysium'

Very simple Spark Structured Streaming demo which consumes from a Kafka cluster.

'Elysium' is a placeholder name to avoid confusion with other projects.

### Instructions

Set up the local development environment.

```
py -3.11.9 venv .venv
./activate.sh
pip install -r requirements.txt
```

Boot up the Kafka instance.

```
docker run -d -p 9092:9092 --name elysium-container apache/kafka:3.9.1-rc0
```

Run the producer script.
This runs a simple producer that publishes stdin to Kafka on `elysium-topic`
(creating the topic if it doesn't yet exist).
Leave this script running to keep sending messages through Kafka.

```
python run_producer.py
```

Run the consumer script.
This runs a simple consumer which subscribes to `elysium-topic`
and prints messages to the console.

```
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.13:4.0.1 run_consumer.py
```

## Misc

The consumer script appears to print one new entry for each message,
but the streamed data is actually handled in *mini-batches*.
If you spam the producer fast enough you can get multiple messages at once.

The Spark/Kafka connector passed to `spark-submit` via `--packages`
will install it locally. It needs to match the version of your Kafka instance.

The `SPARK_LOCAL_HOSTNAME=localhost` environment variable in `activate.sh`
stops the "idWithoutTopologyInfo is null" error as per
[this stackoverflow answer](https://stackoverflow.com/a/79137761/17792618).

The `JAVA_HOME` environment variable is set to the location of my Java 17 installation.
This may vary depending on your operating system, etc.
