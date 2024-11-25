import mysql.connector

# Conexión a la base de datos MySQL
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            database="weatherwhisper",
            user="root",
            password="victormt26.2024"
        )
        return connection
    except mysql.connector.Error as e:
        print("Error al conectarse a la base de datos:", e)
        return None

# Registro de usuario en la base de datos
def register_user(name, email, password, phone_number):
    conn = get_db_connection()
    if conn is None:
        return False

    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (name, email, password, phone_number) VALUES (%s, %s, %s, %s)", 
            (name, email, password, phone_number)  # Almacena la contraseña en texto plano
        )
        conn.commit()
        return True
    except mysql.connector.Error as e:
        print("Error al registrar el usuario:", e)
        return False
    finally:
        cursor.close()
        conn.close()

# Validación de usuario al iniciar sesión
def validate_user(email, password):
    conn = get_db_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
       

        if user and user[0].decode('utf-8') == password:
            return True
        return False
    except mysql.connector.Error as e:
        print("Error al validar el usuario:", e)
        return False
    finally:
        cursor.close()
        conn.close()

