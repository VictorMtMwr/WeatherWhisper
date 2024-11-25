from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from recommendations import recommendation
import requests
import os

app = Flask(__name__)
CORS(app)

# Claves de API desde variables de entorno
API_KEY_TOMORROW = os.getenv("API_KEY_TOMORROW", "gcRChK23DGmoCYen6tVm3XX73Jxfuwh9")
API_KEY_OPENCAGE = os.getenv("API_KEY_OPENCAGE", "097aba7edfda4d57b2810b642abd29f1")

def get_coordinates(city_name):
    """Obtiene las coordenadas de una ciudad utilizando la API de OpenCage."""
    url = f"https://api.opencagedata.com/geocode/v1/json?q={city_name}&key={API_KEY_OPENCAGE}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            coordinates = data['results'][0]['geometry']
            return (coordinates['lat'], coordinates['lng'])
    return None

def get_weather(latitude, longitude):
    """Obtiene datos de clima en tiempo real utilizando la API de Tomorrow.io."""
    url = f"https://api.tomorrow.io/v4/weather/realtime?location={latitude},{longitude}&apikey={API_KEY_TOMORROW}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None


@app.route('/weather', methods=['GET'])
def weather():
    """Endpoint único para obtener clima en tiempo real de una ciudad."""
    city_name = request.args.get('city')
    if not city_name:
        return jsonify({"error": "El parámetro 'city' es obligatorio"}), 400

    # Obtener las coordenadas de la ciudad
    location = get_coordinates(city_name)
    if not location:
        return jsonify({"error": "No se encontraron coordenadas para la ciudad proporcionada"}), 404

    # Obtener datos del clima usando las coordenadas
    weather_data = get_weather(location[0], location[1])
    if not weather_data:
        return jsonify({"error": "No se encontraron datos del clima"}), 404

    # Extraer información clave del clima
    values = weather_data['data']['values']
    temperature = values.get('temperature', "No disponible")
    description = values.get('weatherCode', "No disponible")
    humidity = values.get('humidity', "No disponible")
    precipitation_probability = values.get('precipitationProbability', "No disponible")
    wind_speed = values.get('windSpeed', "No disponible")
    cloud_cover = values.get('cloudCover', "No disponible")
    visibility = values.get('visibility', "No disponible")
    uv_index = values.get('uvIndex', "No disponible")
    rainIntensity = values.get('rainIntensity', "No disponible")

    # Obtener recomendación de vestimenta
    dress_recommendation = recommendation(temperature, precipitation_probability, wind_speed, uv_index, rainIntensity)


    return jsonify({
        "city": city_name,
        "coordinates": location,
        "temperature": temperature,
        "description": description,
        "humidity": humidity,
        "precipitation_probability": precipitation_probability,
        "wind_speed": wind_speed,
        "cloud_cover": cloud_cover,
        "visibility": visibility,
        "uv_index": uv_index,
        "recommendation": dress_recommendation,
        "rainIntensity": rainIntensity
        })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
