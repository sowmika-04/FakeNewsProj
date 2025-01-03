import time
import requests
from kafka import KafkaProducer
from newspaper import Article, Config
from langdetect import detect
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import json

# Function to fetch the latest articles from NewsAPI
def fetch_latest_articles():
    url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=920dcb8e299d479fb97bb3322bfc2dd6"
    response = requests.get(url)
    print(f"API Response Status Code: {response.status_code}")  # Debugging the response status
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        urls = [article['url'] for article in articles]
        print(f"Fetched {len(urls)} URLs from the API.")  # Debugging number of URLs fetched
        return urls
    else:
        print("Error fetching articles")
        return []

# Initialize the Kafka producer
def kafka_producer():
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize as JSON
    )
    topic = 'news-feed'

    # Load the models for misinformation detection
    model_path = r"C:\fake_news\model"  # Update the path if needed
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForSequenceClassification.from_pretrained(model_path)
        print("Model and tokenizer loaded successfully")  # Debugging model load
    except Exception as e:
        print(f"Error loading model or tokenizer: {e}")
        return  # Exit if model loading fails

    # Fetch the latest articles dynamically
    urls = fetch_latest_articles()

    if not urls:
        print("No URLs fetched. Exiting...")  # Debugging if no URLs were fetched
        return

    for url in urls:
        try:
            print(f"Processing URL: {url}")

            # Set custom timeout for the newspaper3k library
            config = Config()
            config.REQUEST_TIMEOUT = 10  # Set a custom timeout value in seconds

            # Download and parse the article using the config
            article = Article(url, config=config)
            article.download()
            article.parse()

            # Concatenate title and content for language detection
            content = article.title + '. ' + article.text
            lang = detect(content)  # Detect language of the article
            print(f"Detected language: {lang}")  # Debugging detected language

            # Analyze the content for misinformation using the pre-trained model
            tokens_info = tokenizer(content, truncation=True, return_tensors="pt", max_length=512)
            with torch.no_grad():
                raw_predictions = model(**tokens_info)

            # Get the fake news percentage (confidence score)
            fake_percentage = int(torch.nn.functional.softmax(raw_predictions.logits[0], dim=0)[1] * 100)
            print(f"Fake percentage: {fake_percentage}%")  # Debugging fake percentage

            # Determine the trust level based on fake percentage
            if fake_percentage <= 40:
                trust_level = "Trustworthy"
            elif fake_percentage > 70:
                trust_level = "Misleading"
            else:
                trust_level = "Uncertain"

            # Prepare the message for Kafka
            message = {
                "url": url,
                "fake_percentage": fake_percentage,
                "trust_level": trust_level,
                "language": lang,
                "content": content[:500]  # Just a snippet of the content for context
            }

            # Send to Kafka
            try:
                producer.send(topic, value=message)
                print(f"Message sent: {message}")  # Debugging message sent to Kafka
            except Exception as e:
                print(f"Error sending message to Kafka: {e}")

            time.sleep(2)

        except Exception as e:
            print(f"Error processing URL {url}: {e}")
            continue

    # Close the producer once all messages are sent
    producer.close()
    print("Producer finished sending messages.")

if __name__ == '__main__':
    kafka_producer()
