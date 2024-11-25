from flask import Flask, jsonify, request, render_template, redirect, url_for
import requests
import os

app = Flask(__name__)

# Variables de configuración desde el entorno
WEATHER_SERVICE_URL = os.getenv('WEATHER_SERVICE_URL', 'http://localhost:5001')
AUTH_SERVICE_URL = os.getenv('AUTH_SERVICE_URL', 'http://localhost:5000')

# Ruta para redirigir al servicio de clima
@app.route('/api/weather', methods=['GET'])
def weather():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "El parámetro 'city' es obligatorio"}), 400

    try:
        # Hacer una solicitud al servicio de clima
        response = requests.get(f"{WEATHER_SERVICE_URL}/weather", params={"city": city})
        response.raise_for_status()  # Lanza un error si la respuesta no es 200 OK
        
        # Retorna la respuesta del microservicio como JSON
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


# Ruta para mostrar el formulario de registro
@app.route('/api/register', methods=['GET'])
def show_register():
    return render_template('register.html')

# Ruta para redirigir al servicio de autenticación (registro)
@app.route('/api/register', methods=['POST'])
def register():
    # Cambia a request.form para capturar los datos enviados por el formulario HTML
    user_data = {
        "name": request.form.get("name"),
        "email": request.form.get("email"),
        "password": request.form.get("password"),
        "phone_number": request.form.get("phone_number")
    }
    try:
        # Envía los datos como JSON al microservicio de autenticación
        response = requests.post(f"{AUTH_SERVICE_URL}/register", json=user_data)
        if response.status_code == 200:
           return redirect(url_for('login'))
        else:
            error_message = "Todos los campos son obligatorios."
            return render_template('register.html', error=error_message)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error en el servicio de autenticación: {str(e)}"}), 500


# Ruta para mostrar el formulario de login
@app.route('/api/login', methods=['GET'])
def show_login():
    return render_template('login.html')

# Ruta para redirigir al servicio de autenticación (login)
@app.route('/api/login', methods=['POST'])
def login():
    credentials = {
        'email': request.form['email'],
        'password': request.form['password']
    }
    try:
        response = requests.post(f"{AUTH_SERVICE_URL}/login", json=credentials)
        if response.status_code == 200:
            return redirect(url_for('index')) 
        else:
            error_message = "Credenciales invalidas."
            return render_template('login.html', error=error_message), 401
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error en el servicio de autenticación: {str(e)}"}), 500

@app.route('/api/index')
def index():
    return render_template('index.html')

# Inicia el API Gateway
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
