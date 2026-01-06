from create_topic import TOPIC_NAME
from kafka import KafkaProducer

if __name__ == "__main__":
    producer = KafkaProducer(bootstrap_servers="localhost:9092")
    print("Created producer on local Kafka.")
    print(f"Publish messages on topic '{TOPIC_NAME}':")

    while True:
        message = input("> ")
        producer.send(TOPIC_NAME, bytes(message, "utf-8"))
        producer.flush()
