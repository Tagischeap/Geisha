from flask import Flask

# Initialize Flask app
app = Flask(__name__)

# Define a basic route
@app.route("/")
def index():
    return "<h1>Welcome to the Discord Bot Webpage</h1>"

# Function to run the Flask app
def start_server():
    app.run(host="0.0.0.0", port=5000)
