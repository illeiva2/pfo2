"""
PFO 2: Sistema de Gestión de Tareas con API y Base de Datos
Servidor Flask + SQLite con autenticación y contraseñas hasheadas.
"""

import sqlite3
from flask import Flask, request, jsonify, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
DB_FILE = "tareas.db"


# ---------- BASE DE DATOS ----------

def conectar_db():
    """Devuelve una conexión a la base SQLite."""
    return sqlite3.connect(DB_FILE)


def inicializar_db():
    """Crea la tabla de usuarios si no existe."""
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                contrasena_hash TEXT NOT NULL
            )
        ''')
        conn.commit()


# ---------- ENDPOINTS ----------

@app.route('/registro', methods=['POST'])
def registro():
    """
    Registra un usuario nuevo.
    Espera JSON: {"usuario": "nombre", "contraseña": "1234"}
    """
    datos = request.get_json()

    if not datos:
        return jsonify({"error": "Se esperaba JSON"}), 400

    usuario = datos.get("usuario")
    # Aceptamos tanto "contraseña" como "contrasena" por las dudas
    contrasena = datos.get("contraseña") or datos.get("contrasena")

    if not usuario or not contrasena:
        return jsonify({"error": "Faltan usuario o contraseña"}), 400

    # Hasheamos la contraseña antes de guardarla
    contrasena_hash = generate_password_hash(contrasena)

    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO usuarios (usuario, contrasena_hash) VALUES (?, ?)",
                (usuario, contrasena_hash)
            )
            conn.commit()
        return jsonify({"mensaje": f"Usuario '{usuario}' registrado correctamente"}), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": "El usuario ya existe"}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/login', methods=['POST'])
def login():
    """
    Verifica credenciales del usuario.
    Espera JSON: {"usuario": "nombre", "contraseña": "1234"}
    """
    datos = request.get_json()

    if not datos:
        return jsonify({"error": "Se esperaba JSON"}), 400

    usuario = datos.get("usuario")
    contrasena = datos.get("contraseña") or datos.get("contrasena")

    if not usuario or not contrasena:
        return jsonify({"error": "Faltan usuario o contraseña"}), 400

    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT contrasena_hash FROM usuarios WHERE usuario = ?",
            (usuario,)
        )
        fila = cursor.fetchone()

    if fila is None:
        return jsonify({"error": "Usuario o contraseña incorrectos"}), 401

    contrasena_hash_guardado = fila[0]

    # Comparamos el hash de la contraseña ingresada con el almacenado
    if check_password_hash(contrasena_hash_guardado, contrasena):
        return jsonify({"mensaje": f"Bienvenido {usuario}, login exitoso"}), 200
    else:
        return jsonify({"error": "Usuario o contraseña incorrectos"}), 401


@app.route('/tareas', methods=['GET'])
def tareas():
    """Muestra un HTML de bienvenida."""
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Sistema de Gestión de Tareas</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f6f9;
                margin: 0;
                padding: 40px;
                color: #333;
            }
            .contenedor {
                max-width: 720px;
                margin: 0 auto;
                background: white;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            }
            h1 { color: #2c3e50; }
            .endpoint {
                background: #ecf0f1;
                padding: 10px 14px;
                margin: 8px 0;
                border-left: 4px solid #3498db;
                font-family: monospace;
            }
        </style>
    </head>
    <body>
        <div class="contenedor">
            <h1>Sistema de Gestión de Tareas</h1>
            <p>Bienvenido a la API. Endpoints disponibles:</p>
            <div class="endpoint"><b>POST</b> /registro &mdash; Registrar un nuevo usuario</div>
            <div class="endpoint"><b>POST</b> /login &mdash; Iniciar sesión</div>
            <div class="endpoint"><b>GET</b> /tareas &mdash; Esta página</div>
            <p style="margin-top: 30px; color: #7f8c8d;">
                PFO 2 &mdash; Programación sobre Redes &mdash; IFTS N°29
            </p>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)


# ---------- MAIN ----------

if __name__ == "__main__":
    inicializar_db()
    print("Servidor corriendo en http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
