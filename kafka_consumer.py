from kafka import KafkaConsumer
from pymongo import MongoClient
import json

def kafka_consumer():
    # Step 1: Connect to MongoDB
    mongo_client = MongoClient("mongodb://localhost:27017/")  # Default MongoDB connection
    db = mongo_client["misinformation_db"]  # Database name
    collection = db["news_feed"]  # Collection name

    # Step 2: Connect to Kafka
    consumer = KafkaConsumer(
        'news-feed',
        bootstrap_servers='localhost:9092',
        group_id='misinformation-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))  # Deserialize JSON
    )

    print("Consumer is running and listening for messages...")

    for message in consumer:
        try:
            # The message is already deserialized into a dictionary
            message_dict = message.value

            # Step 3: Insert the message into MongoDB
            collection.insert_one(message_dict)
            print(f"Message inserted into MongoDB: {message_dict}")

        except Exception as e:
            print(f"Error processing message: {e}")

if __name__ == '__main__':
    kafka_consumer()
