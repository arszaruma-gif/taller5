import os
from flask import Flask, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Configuración de conexión leyendo las variables de Docker Compose
def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST', 'db'),
        database=os.environ.get('DB_NAME', 'empresa'),
        user=os.environ.get('DB_USER', 'admin'),
        password=os.environ.get('DB_PASSWORD', 'admin123'),
        port=os.environ.get('DB_PORT', '5432')
    )
    return conn

@app.route('/')
def home():
    # Actividad 2: Verificar la conexión básica
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({"status": "Conexión exitosa a PostgreSQL"}), 200
    except Exception as e:
        return jsonify({"error": f"Error de conexión: {str(e)}"}), 500

@app.route('/clientes')
def listar_clientes():
    # Actividad 5: Listar los clientes registrados
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT id, nombre FROM clientes;')
        clientes = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(clientes), 200
    except Exception as e:
        return jsonify({"error": f"No se pudo consultar la tabla: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)