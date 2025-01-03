import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt

# Step 1: Connect to MongoDB
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["misinformation_db"]
collection = db["news_feed"]

# Step 2: Load data into a DataFrame
data = pd.DataFrame(list(collection.find()))
data["fake_percentage"] = data["fake_percentage"].astype(int)

# Step 3: Plot Trust Level Distribution
trust_level_counts = data["trust_level"].value_counts()
trust_level_counts.plot(kind="bar", title="Trust Level Distribution")
plt.xlabel("Trust Level")
plt.ylabel("Count")
plt.show()

# Step 4: Plot Fake Percentage Histogram
data["fake_percentage"].plot(kind="hist", bins=20, title="Fake Percentage Histogram")
plt.xlabel("Fake Percentage")
plt.show()
