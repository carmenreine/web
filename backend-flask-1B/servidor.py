'''
servidor.py

Autoras: Leire Bernárdez Vázquez y Carmen Reiné Rueda

Descripción:
    API REST desarrollada con Flask para la gestión de un portal de videojuegos. Incluye autenticación,
    roles de usuario, y operaciones CRUD sobre una base de datos PostgreSQL.

Estructura principal:
    - Clase Database: Maneja la conexión y el esquema de la BD.
    - Clase UserService: Registra, autentica y gestiona usuarios.
    - Clase GameService: CRUD de videojuegos.
    - Clase AppServer: Configura Flask, CORS, rutas y ejecución.

Endpoints principales:
    - POST/register         Registro de nuevos usuarios
    - POST/login            Autenticación y creación de cookie de sesión
    - GET/auth/status       Verifica autenticación
    - GET/juegos            Listado de juegos (requiere login)
    - POST/juegos           Crear nuevo juego (solo admin)
    - PUT/juegos/<id>       Editar juego existente (solo admin)
    - DELETE/juegos/<id>    Eliminar juego (solo admin)
    - POST/logout           Cerrar sesión
    
Notas:
    - Asegurarse de tener la base de datos de PostgreSQL con el nombre "portaljuegosdb".
    - La base de datos no se crea desde 0 cada vez que ejecutas este script (si se desea empezarla de 0, hay que
        hacerlo manualmente desde la terminal de PostgreSQL).
    - Cambiar los parámetros de user y password para poder conectarse a la base de datos.
    
'''
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import psycopg2
import psycopg2.extras
import secrets
import os
import urllib.parse as up


user = "leire"
password = "leire"

# ============================================================
# === CLASE DE CONEXIÓN A BASE DE DATOS ======================
# ============================================================

class Database:
    """
    Clase encargada de gestionar la conexión y estructura de la base de datos.
    """
    def __init__(self, host, db, user, password):
        self.host = host
        self.db = db
        self.user = user
        self.password = password

    def connect(self):
        """
        Devuelve una conexión activa a PostgreSQL.
        """
        return psycopg2.connect(
            host=self.host,
            database=self.db,
            user=self.user,
            password=self.password,
            sslmode="require"
        )

    def init_schema(self):
        """
        Crea las tablas necesarias y el superusuario por defecto.
        """
        conn = self.connect()
        cur = conn.cursor()

        # --------------------------------------------------------
        # TABLA DE JUEGOS
        # --------------------------------------------------------
        cur.execute("""
            CREATE TABLE IF NOT EXISTS juegos (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                genero VARCHAR(50),
                plataforma VARCHAR(50),
                anio INT,
                descripcion TEXT,
                imagen_ruta TEXT,
                wikipedia_url TEXT
            );
        """)

        # --------------------------------------------------------
        # TABLA DE USUARIOS
        # --------------------------------------------------------
        cur.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(100) NOT NULL,
                es_admin BOOLEAN DEFAULT FALSE
            );
        """)

        # --------------------------------------------------------
        # CREAR SUPERUSUARIO (si no existe)
        # --------------------------------------------------------
        cur.execute("SELECT * FROM usuarios WHERE username='admin';")
        admin = cur.fetchone()
        if not admin:
            cur.execute("""
                INSERT INTO usuarios (username, email, password, es_admin)
                VALUES ('admin', 'admin@portal.com', 'admin123', TRUE);
            """)
            print("Superusuario creado (admin / admin123)")

        # --------------------------------------------------------
        # INSERTAR JUEGOS INICIALES (solo si la tabla está vacía)
        # --------------------------------------------------------
        cur.execute("SELECT COUNT(*) FROM juegos;")
        count = cur.fetchone()[0]
        if count == 0:
            juegos_iniciales = [
                ("Hangman", "Puzzle", "Web", 2024,
                "Juego clásico del ahorcado implementado por el equipo.",
                "../assets/hangman.png", None),

                ("LEGO Star Wars: The Skywalker Saga", "Acción", "PC/Consola", 2022,
                "Revive las 9 películas de la saga LEGO.",
                "../assets/lego.png",
                "https://es.wikipedia.org/wiki/Lego_Star_Wars:_The_Skywalker_Saga"),

                ("Animal Crossing: New Horizons", "Simulación", "Nintendo Switch", 2020,
                "Crea tu propia isla y comunidad.",
                "../assets/animalcrossing.png",
                "https://es.wikipedia.org/wiki/Animal_Crossing:_New_Horizons"),

                ("Hades", "Roguelike", "PC/Consola", 2020,
                "Escapa del inframundo en este título de acción.",
                "../assets/hades.png",
                "https://es.wikipedia.org/wiki/Hades_(videojuego)"),

                ("The Legend of Zelda: Breath of the Wild", "Aventura", "Nintendo Switch", 2017,
                "Explora libremente el vasto mundo de Hyrule.",
                "../assets/zelda.png",
                "https://es.wikipedia.org/wiki/The_Legend_of_Zelda:_Breath_of_the_Wild"),

                ("Stardew Valley", "Simulación", "PC/Consola", 2016,
                "Crea tu granja y vive una vida tranquila en el campo.",
                "../assets/stardew.png",
                "https://es.wikipedia.org/wiki/Stardew_Valley"),

                ("Rocket League", "Deportes", "PC/Consola", 2015,
                "Combina fútbol y coches en un juego lleno de acción.",
                "../assets/rocketleague.png",
                "https://es.wikipedia.org/wiki/Rocket_League"),

                ("2048", "Puzzle", "Web", 2014,
                "Desliza los números hasta llegar a 2048.",
                "../assets/2048.png",
                "https://es.wikipedia.org/wiki/2048_(videojuego)"),

                ("Minecraft", "Aventura", "PC/Consola", 2011,
                "Construye y sobrevive en mundos infinitos.",
                "../assets/minecraft.png",
                "https://es.wikipedia.org/wiki/Minecraft"),

                ("Snake", "Clásico", "Web", 1997,
                "Guía la serpiente para comer y crecer sin chocar.",
                "../assets/snake.png",
                "https://es.wikipedia.org/wiki/La_serpiente_(videojuego)"),

                ("DOOM", "Shooter", "PC", 1993,
                "Enfréntate a hordas demoníacas en este clásico FPS.",
                "../assets/doom.png",
                "https://es.wikipedia.org/wiki/Doom_(videojuego_de_1993)"),

                ("Tetris", "Puzzle", "Web", 1984,
                "Encaja las piezas antes de llenar la pantalla.",
                "../assets/tetris.png",
                "https://es.wikipedia.org/wiki/Tetris"),

                ("Pac-Man", "Clásico", "Arcade", 1980,
                "Come puntos y esquiva fantasmas en el laberinto.",
                "../assets/pacman.png",
                "https://es.wikipedia.org/wiki/Pac-Man")
            ]

            cur.executemany("""
                INSERT INTO juegos (nombre, genero, plataforma, anio, descripcion, imagen_ruta, wikipedia_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """, juegos_iniciales)
            print("Juegos iniciales insertados en la base de datos")

        conn.commit()
        cur.close()
        conn.close()


# ============================================================
# === SERVICIO DE USUARIOS ==================================
# ============================================================

class UserService:
    """
    Servicio de gestión de usuarios con tokens en memoria.
    """
    def __init__(self, db: Database):
        self.db = db
        self.tokens = {}  # token -> {user_id, es_admin}

    def register(self, username, email, password):
        conn = self.db.connect()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO usuarios (username, email, password)
                VALUES (%s, %s, %s)
                RETURNING id;
            """, (username, email, password))
            new_id = cur.fetchone()[0]
            conn.commit()
            return new_id
        except psycopg2.Error as e:
            conn.rollback()
            if "unique" in str(e).lower():
                return None
            raise e
        finally:
            cur.close()
            conn.close()

    def login(self, username, password):
        conn = self.db.connect()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
            SELECT id, es_admin 
            FROM usuarios 
            WHERE username=%s AND password=%s;
        """, (username, password))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if not user:
            return None

        # Generar token y guardarlo en memoria
        token = secrets.token_hex(16)
        self.tokens[token] = {
            "user_id": user["id"],
            "es_admin": user["es_admin"]
        }
        return token

    def check_token(self, token):
        return self.tokens.get(token)

    def authenticate(self, request):
        """Verifica si el usuario está autenticado mediante el token en cookies."""
        token = request.cookies.get("token")
        if not token:
            return None

        user = self.check_token(token)
        if not user:
            return None

        return {
            "user_id": user["user_id"],
            "es_admin": user["es_admin"]
        }

    def logout(self, token):
        if token in self.tokens:
            del self.tokens[token]


# ============================================================
# === SERVICIO DE JUEGOS ====================================
# ============================================================

class GameService:
    def __init__(self, db: Database):
        self.db = db

    def listar(self):
        conn = self.db.connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM juegos ORDER BY id;")
        rows = cur.fetchall()
        cur.close()
        conn.close()

        return [
            {
                "id": r[0],
                "nombre": r[1],
                "genero": r[2],
                "plataforma": r[3],
                "anio": r[4],
                "descripcion": r[5],
                "imagen_ruta": r[6],
                "wikipedia_url": r[7]
            }
            for r in rows
        ]

    def crear(self, data):
        conn = self.db.connect()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO juegos (nombre, genero, plataforma, anio, descripcion, imagen_ruta, wikipedia_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;
        """, (
            data['nombre'],
            data['genero'],
            data['plataforma'],
            data['anio'],
            data.get('descripcion', 'Sin descripción disponible'),
            data.get('imagen_ruta'),
            data.get('wikipedia_url')
        ))
        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return new_id

# ============================================================
# === SERVIDOR PRINCIPAL FLASK ===============================
# ============================================================

class AppServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = "supersecreto"

        # Configuración correcta de CORS
        CORS(
            self.app,
            supports_credentials=True,
            origins=["*"]
        )

        DATABASE_URL = os.getenv("DATABASE_URL")
        if not DATABASE_URL:
            raise RuntimeError("DATABASE_URL no está definida en Render")

        # Parsear la URL de Render
        url = up.urlparse(DATABASE_URL)

        self.db = Database(
            host=url.hostname,
            db=url.path[1:],  # Sin la barra inicial
            user=url.username,
            password=url.password
        )
        self.db.init_schema()

        self.users = UserService(self.db)
        self.games = GameService(self.db)

        self.register_routes()

    def requiere_autenticacion(self, func):
        def wrapper(*args, **kwargs):
            user_info = self.users.authenticate(request)
            if not user_info:
                return jsonify({"error": "No autorizado"}), 401
            return func(*args, **kwargs)

        wrapper.__name__ = func.__name__
        return wrapper

    def register_routes(self):
        app = self.app

        # ---------- REGISTRO ----------
        @app.route('/register', methods=['POST'])
        def register():
            data = request.json
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            if not username or not email or not password:
                return jsonify({"error": "Faltan campos obligatorios"}), 400

            user_id = self.users.register(username, email, password)
            if not user_id:
                return jsonify({"error": "El usuario o email ya existen"}), 409

            return jsonify({
                "mensaje": "Usuario registrado correctamente",
                "id": user_id
            }), 201

        # ---------- LOGIN ----------
        @app.route('/login', methods=['POST'])
        def login():
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')

            print("Datos recibidos desde frontend:", data)

            # Usa el servicio de usuarios
            token = self.users.login(username, password)
            if not token:
                return jsonify({"error": "Credenciales incorrectas"}), 401

            # Crea la respuesta con cookie
            response = jsonify({"message": "Inicio de sesión correcto"})
            response.set_cookie(
                "token",
                token,
                httponly=True,
                samesite="None",
                secure=True
            )
            return response

        # ---------- ESTADO DE AUTENTICACIÓN ----------
        @app.route('/auth/status', methods=['GET'])
        def auth_status():
            user_info = self.users.authenticate(request)
            if not user_info:
                return jsonify({"autenticado": False}), 401

            return jsonify({
                "autenticado": True,
                "user_id": user_info["user_id"],
                "es_admin": user_info["es_admin"]
            })

        # ---------- LISTAR JUEGOS ----------
        @app.route('/juegos', methods=['GET'])
        @self.requiere_autenticacion
        def listar_juegos():
            juegos = self.games.listar()
            return jsonify(juegos)

        # ---------- CREAR JUEGO ----------
        @app.route('/juegos', methods=['POST'])
        @self.requiere_autenticacion
        def crear_juego():
            user_info = self.users.authenticate(request)
            if not user_info or not user_info["es_admin"]:
                return jsonify({"error": "Solo administradores pueden crear juegos"}), 403

            new_id = self.games.crear(request.json)
            return jsonify({"mensaje": "Juego creado", "id": new_id}), 201

        # ---------- EDITAR JUEGO ----------
        @app.route('/juegos/<int:juego_id>', methods=['PUT'])
        @self.requiere_autenticacion
        def editar_juego(juego_id):
            user_info = self.users.authenticate(request)
            if not user_info or not user_info["es_admin"]:
                return jsonify({"error": "Solo administradores pueden editar juegos"}), 403

            data = request.json
            conn = self.db.connect()
            cur = conn.cursor()

            cur.execute("""
                UPDATE juegos
                SET nombre=%s,
                    genero=%s,
                    plataforma=%s,
                    anio=%s,
                    descripcion=%s,
                    imagen_ruta=%s,
                    wikipedia_url=%s
                WHERE id=%s
                RETURNING id;
            """, (
                data['nombre'],
                data['genero'],
                data['plataforma'],
                data['anio'],
                data.get('descripcion', 'Sin descripción disponible'),
                data.get('imagen_ruta'),
                data.get('wikipedia_url'),
                juego_id
            ))

            updated = cur.fetchone()
            conn.commit()
            cur.close()
            conn.close()

            if not updated:
                return jsonify({"error": "Juego no encontrado"}), 404

            return jsonify({"mensaje": "Juego actualizado correctamente", "id": updated[0]}), 200

        # ---------- ELIMINAR JUEGO ----------
        @app.route('/juegos/<int:juego_id>', methods=['DELETE'])
        @self.requiere_autenticacion
        def eliminar_juego(juego_id):
            user_info = self.users.authenticate(request)
            if not user_info or not user_info["es_admin"]:
                return jsonify({"error": "Solo administradores pueden eliminar juegos"}), 403

            conn = self.db.connect()
            cur = conn.cursor()
            cur.execute("DELETE FROM juegos WHERE id=%s RETURNING id;", (juego_id,))
            deleted = cur.fetchone()
            conn.commit()
            cur.close()
            conn.close()

            if not deleted:
                return jsonify({"error": "Juego no encontrado"}), 404

            return jsonify({"mensaje": "Juego eliminado correctamente", "id": deleted[0]}), 200

        # ---------- LOGOUT ----------
        @app.route('/logout', methods=['POST'])
        @self.requiere_autenticacion
        def logout():
            token = request.cookies.get('token')
            self.users.logout(token)

            response = make_response(jsonify({"mensaje": "Sesión cerrada"}))
            response.delete_cookie("token")
            return response

    # ========================================================
    # === EJECUCIÓN DEL SERVIDOR =============================
    # ========================================================
    def run(self):
        print("Servidor Flask iniciado en http://127.0.0.1:9000")
        self.app.run(port=9000, debug=True)


# ============================================================
# === INICIO DE EJECUCIÓN ===================================
# ============================================================
server = AppServer()
app = server.app  # Render y Gunicorn usarán esta variable

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, debug=True)
