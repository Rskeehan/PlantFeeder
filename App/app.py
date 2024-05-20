import requests
import time
import logging
import schedule
from flask import Flask, jsonify
import threading
import os

# Setup logging
logging.basicConfig(level=logging.INFO)

# Import GPIO library as a mock for development
try:
    import RPi.GPIO as GPIO
except (ImportError, RuntimeError):
    from unittest.mock import MagicMock
    GPIO = MagicMock()

# Setup GPIO
valve_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(valve_pin, GPIO.OUT)

app = Flask(__name__)
weather_data = {}

# Function to check weather
def check_weather():
    api_key = os.getenv("API_KEY")
    city_id = os.getenv("CITY_ID")
    url = f"http://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()
        logging.info(f"API response: {data}")
        return data
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching weather data: {e}")
        return None

# Function to control valve
def water_plants():
    logging.info("Watering the plants")
    GPIO.output(valve_pin, GPIO.HIGH)
    time.sleep(10)  # Water for 10 seconds
    GPIO.output(valve_pin, GPIO.LOW)
    logging.info("Watering completed")

# Function to run check_weather once a day
def run_check_weather():
    global weather_data
    logging.info("Running check_weather")
    weather_data = check_weather()
    if weather_data:
        main_weather = weather_data.get('weather', [{}])[0].get('main')
        if main_weather:
            logging.info(f"Weather: {main_weather}")
            if main_weather != "Rain":
                water_plants()
            else:
                logging.info("It has rained today, no need to water the plants")
        else:
            logging.error("Main weather information not found in API response")
    else:
        logging.error("Failed to retrieve weather information")

# Flask route to expose weather information
@app.route('/weather')
def get_weather():
    if weather_data:
        main_weather = weather_data.get('weather', [{}])[0].get('main')
        temperature = weather_data.get('main', {}).get('temp')
        humidity = weather_data.get('main', {}).get('humidity')
        condition = main_weather if main_weather else "Unknown"
        
        weather_info = {
            "temperature": f"{temperature}K",  # Temperature in Kelvin
            "humidity": f"{humidity}%",        # Humidity percentage
            "condition": condition             # Weather condition
        }
        return jsonify(weather_info)
    else:
        return jsonify({"error": "Failed to retrieve weather information"})

# Schedule check_weather to run once a day at a specific time (e.g., 8:00 AM)
schedule.every().day.at("14:00").do(run_check_weather)

if __name__ == "__main__":
    # Run check_weather immediately
    run_check_weather()

    # Start a separate thread for the Flask app
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000)).start()

    # Keep the program running to allow scheduled tasks to execute
    while True:
        schedule.run_pending()
        time.sleep(1)  # Sleep for 1 second to prevent CPU usage
