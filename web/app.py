from flask import Flask, render_template
import requests

app = Flask(__name__)

# Endpoint of the plant-watering-app
PLANT_WATERING_APP_URL = "http://plant-feeder:5000/weather"

@app.route("/")
def index():
    # Make a request to the plant-watering-app to get weather data
    response = requests.get(PLANT_WATERING_APP_URL)
    if response.status_code == 200:
        weather_data = response.json()
        # Pass weather data to the template
        return render_template("index.html", weather=weather_data)
    else:
        return "Failed to fetch weather data"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)  # Run the app on port 80
