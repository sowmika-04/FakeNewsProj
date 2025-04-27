# Fake News Detection in Python

This project uses various Natural Language Processing (NLP) techniques and machine learning algorithms to classify news articles as fake or real. We leverage **scikit-learn** for building the models and **Apache Kafka** for real-time data streaming.

## Project Overview

The goal of this project is to detect fake news by processing news headlines using machine learning models. The project includes data pre-processing, feature extraction, classifier building, model evaluation, and real-time fake news detection via Kafka.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Dataset](#dataset)
3. [Project Structure](#project-structure)
4. [Kafka Integration](#kafka-integration)
5. [Steps to Run the Project](#steps-to-run-the-project)
6. [Performance Evaluation](#performance-evaluation)
7. [Next Steps](#next-steps)

## Prerequisites

Before running the project, make sure you have the following installed:

1. **Python 3.6+**  
   You can download Python from the official website: [Python Downloads](https://www.python.org/downloads/). Follow the instructions to set up Python on your machine.

2. **Anaconda (Optional)**  
   If you prefer Anaconda for managing environments, download and install it from [Anaconda Downloads](https://www.anaconda.com/download/).

3. **Required Libraries**  
   Install the following Python libraries using `pip` or `conda`:
   ```bash
   pip install -U scikit-learn numpy scipy


