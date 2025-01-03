from pymongo import MongoClient
import datetime

# Step 1: Connect to MongoDB
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["misinformation_db"]
collection = db["news_feed"]

# Step 2: Add a timestamp to each document
for doc in collection.find({"timestamp": {"$exists": False}}):
    collection.update_one(
        {"_id": doc["_id"]},
        {"$set": {"timestamp": datetime.datetime.now()}}
    )
    print(f"Updated document: {doc['_id']}")
