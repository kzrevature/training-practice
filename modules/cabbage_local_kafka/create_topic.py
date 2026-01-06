from kafka import KafkaAdminClient
from kafka.admin import NewTopic

TOPIC_NAME = "cabbage-topic"

if __name__ == "__main__":
    print(f"Initializing local Kafka cluster with topic '{TOPIC_NAME}'.")

    topic = NewTopic(TOPIC_NAME)
    admin = KafkaAdminClient()

    if TOPIC_NAME in admin.list_topics():
        print(f"Topic '{TOPIC_NAME}' already exists, skipping.")
    else:
        admin.create_topics([topic])
        print(f"Created topic '{TOPIC_NAME}'.")
