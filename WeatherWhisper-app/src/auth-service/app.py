from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from auth_db import register_user, validate_user
from flask_cors import CORS  

app = Flask(__name__)
CORS(app)
app.secret_key = '\x9d\x988\x0b\xb3=\xe8\xb7\x1c\n{:\xe0\x12\xb7\x83\xc1\x96AJ\x0c\xad\xefE'
# Ruta para el registro de usuarios
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        user_data = request.get_json()  # Obtener los datos como JSON
        name = user_data.get('name')
        email = user_data.get('email')
        password = user_data.get('password')
        phone_number = user_data.get('phone_number')

        if not name or not email or not password or not phone_number:
            error_message = "Todos los campos son obligatorios."
            return jsonify({"error": error_message}), 400  # Responder en JSON

        try:
            register_user(name, email, password, phone_number)  # Guardar el nuevo usuario en la base de datos
            return jsonify({"message": "Registro completado, redirigiendo al login..."}), 200
        except Exception as e:
            return jsonify({"error": f"Error al registrar el usuario: {str(e)}"}), 500  # Enviar error en JSON


# Ruta para iniciar sesión (validar usuario)
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        credentials = request.get_json()
        email = credentials.get('email')
        password = credentials.get('password')

        if not email or not password:
            error_message = "Todos los campos son obligatorios."
            return jsonify({"error": error_message}), 400  # Responder en JSON

        if validate_user(email, password):  
            session['user'] = email
            flash('Inicio de sesión exitoso.')
            return jsonify({"message": "Inicio de sesión completado, redirigiendo al ..."}), 200
        else:
            error_message = "Credenciales incorrectas. Intenta nuevamente."
            return jsonify({"message": "Credenciales invalidas"}), 400


@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
