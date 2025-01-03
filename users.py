from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Create database and collections
db = client["misinformation_db"]
user_collection = db["users"]
content_collection = db["news_feed"]

# Add initial users to the users collection
user_collection.insert_many([
    {"username": "user1", "password": "password1"},
    {"username": "user2", "password": "password2"}
])

print("Database and collections initialized with user data.")
