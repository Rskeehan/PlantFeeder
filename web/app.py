from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# URL for the Plant Feeder's weather API
PLANT_FEEDER_URL = "http://plant-feeder:5000/weather"

# Route to display weather information
@app.route('/')
def index():
    try:
        response = requests.get(PLANT_FEEDER_URL)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        weather_data = response.json()

        # Convert temperature from Kelvin to Celsius and Fahrenheit
        if 'temperature' in weather_data:
            kelvin_temp = float(weather_data['temperature'].replace('K', ''))
            celsius_temp = kelvin_temp - 273.15
            fahrenheit_temp = (kelvin_temp - 273.15) * 9/5 + 32

            weather_data['temperature_celsius'] = f"{celsius_temp:.2f} °C"
            weather_data['temperature_fahrenheit'] = f"{fahrenheit_temp:.2f} °F"

        if 'error' in weather_data:
            return render_template('error.html', message=weather_data['error'])
        return render_template('weather.html', weather=weather_data)
    except requests.exceptions.RequestException as e:
        return render_template('error.html', message=str(e))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
