from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize the Flask app
app = Flask(__name__)

# MongoDB connection setup
app.config["MONGO_URI"] = "mongodb://localhost:27017/misinformation_db"
mongo = PyMongo(app)

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# Sign-up page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if username exists
        existing_user = mongo.db.users.find_one({'username': username})
        if existing_user:
            return "Username already exists. Try another one."

        # Insert new user into MongoDB
        hashed_password = generate_password_hash(password)
        mongo.db.users.insert_one({'username': username, 'password': hashed_password})

        return redirect(url_for('login'))

    return render_template('signup.html')

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Find the user in MongoDB
        user = mongo.db.users.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            return redirect(url_for('predictions'))

        return "Invalid credentials. Please try again."

    return render_template('login.html')

# Predictions page (Display fake news data from MongoDB)
@app.route('/predictions')
def predictions():
    predictions = mongo.db.news_feed.find().sort([("timestamp", -1)]).limit(5)  # Latest 5 predictions
    
    # Add trust level based on fake_percentage
    predictions_with_trust = []
    for prediction in predictions:
        fake_percentage = prediction.get('fake_percentage', 0)
        
        if fake_percentage > 70:
            trust_level = 'Misleading'
            trust_color = 'red'
        elif 40 <= fake_percentage <= 70:
            trust_level = 'Uncertain'
            trust_color = 'orange'
        else:
            trust_level = 'Trustworthy'
            trust_color = 'green'
        
        prediction['trust_level'] = trust_level
        prediction['trust_color'] = trust_color
        predictions_with_trust.append(prediction)

    return render_template('predictions.html', predictions=predictions_with_trust)

if __name__ == '__main__':
    app.run(debug=True)
