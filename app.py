import os
import sqlite3
import requests
from flask import Flask, render_template, request, jsonify, redirect, url_for
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Load the API key from the environment
API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

# Initialize SQLite database
DATABASE = "favorites.db"

# Function to connect to the SQLite database
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Route to get weather data for a city
@app.route("/weather", methods=["GET"])
def get_weather():
    city_name = request.args.get("city")
    if not city_name:
        return jsonify({"error": "City name is required"}), 400

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            return jsonify({"error": "City not found"}), 404
        
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": f"Error fetching weather data: {str(e)}"}), 500

# Route to save a favorite city
@app.route("/favorites", methods=["POST"])
def save_favorite():
    city_name = request.json.get("city")
    if not city_name:
        return jsonify({"error": "City name is required"}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO favorites (name) VALUES (?)", (city_name,))
    conn.commit()
    conn.close()

    return jsonify({"message": f"{city_name} added to favorites."}), 201

# Route to get all favorite cities
@app.route("/favorites", methods=["GET"])
def get_favorites():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM favorites")
    rows = cursor.fetchall()
    conn.close()

    favorites = [{"id": row["id"], "name": row["name"]} for row in rows]
    return jsonify(favorites)

# Route to display the front-end page
@app.route("/")
def index():
    return render_template("index.html")

# Function to initialize the database
def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
    """)
    conn.commit()
    conn.close()

# Initialize the database when the app starts
init_db()

if __name__ == "__main__":
    app.run(debug=True)






from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/weather')
def weather():
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'City parameter is missing.'}), 400
    weather_data = get_weather_data(city)
    if weather_data:
        return jsonify(weather_data)
    else:
        return jsonify({'error': 'Weather data could not be retrieved.'}), 500

def get_weather_data(city):
    # Replace with your actual weather API URL and key
    api_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=YOUR_API_KEY&units=metric'
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        return {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'condition': data['weather'][0]['description'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed']
        }
    else:
        return None
