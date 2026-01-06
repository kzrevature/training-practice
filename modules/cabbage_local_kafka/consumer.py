from create_topic import TOPIC_NAME
from kafka import KafkaConsumer

if __name__ == "__main__":
    consumer = KafkaConsumer(TOPIC_NAME)
    print(f"Subscribed to local Kafka on topic '{TOPIC_NAME}'.")
    for msg in consumer:
        contents = msg.value.decode("utf-8")
        print(f"Receieved: {contents}")
