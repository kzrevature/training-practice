from kafka import KafkaAdminClient, KafkaProducer
from kafka.admin import NewTopic


def create_topic_if_not_exists(topic_name: str):
    client = KafkaAdminClient()
    if topic_name not in client.list_topics():
        client.create_topics([NewTopic(topic_name)])
        print(f"Created topic '{topic_name}'")
    else:
        print(f"Using existing topic '{topic_name}'")


def start_producer_on_topic(topic_name: str):
    producer = KafkaProducer()
    print(f"Started Kafka producer on topic {topic_name}.")
    print("Ready to send messages (send empty line to terminate).")
    while True:
        msg = input("> ")
        if msg == "":
            break
        producer.send(topic_name, msg.encode("utf-8"))
        producer.flush()

    print("Stopping Kafka producer.")
    producer.close()


if __name__ == "__main__":
    topic_name = "elysium-topic"
    create_topic_if_not_exists(topic_name)
    start_producer_on_topic(topic_name)
