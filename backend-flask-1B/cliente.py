'''
cliente.py

Autoras: Leire Bernárdez Vázquez y Carmen Reiné Rueda

Descripción:
    Script que prueba las diferentes operaciones disponibles en servidor.py
    para confirmar su correcto funcionamiento en la terminal.

Pruebas principales:
    - Registro de un usuario
    - Login como administrador
    - Comprobar el estado de autenticación
    - Crear un juego nuevo
    - Listar los juegos
    - Cerrar sesión
    - Verificar que el estado de autenticación ha cambiado
    
Notas:
    - Asegurarse de tener la base de datos de PostgreSQL corriendo en otra terminal.
    
'''

import requests
import random

BASE_URL = "http://localhost:9000"

def test_api():
    print("==== PRUEBA COMPLETA DEL PORTAL DE JUEGOS ====\n")

    # ========================================================
    # =========== REGISTRO DE UN USUARIO NUEVO ===============
    # ========================================================
    usuario_random = f"leire{random.randint(1000,9999)}"
    nuevo_usuario = {
        "username": usuario_random,
        "email": f"{usuario_random}@test.com",
        "password": "1234"
    }

    print("Registrando nuevo usuario...")
    r_reg = requests.post(f"{BASE_URL}/register", json=nuevo_usuario)
    try:
        print("POST /register:", r_reg.status_code, r_reg.json(), "\n")
    except Exception:
        print("POST /register:", r_reg.status_code, r_reg.text, "\n")

    # ========================================================
    # ============= LOGIN COMO ADMINISTRADOR =================
    # ========================================================
    print("Iniciando sesión como superusuario (admin)...")
    session = requests.Session()
    login_data = {"username": "admin", "password": "admin123"}
    r_login = session.post(f"{BASE_URL}/login", json=login_data)
    print("POST /login:", r_login.status_code, r_login.json(), "\n")

    if r_login.status_code != 200:
        print("Error de login. Revisa usuario/contraseña.")
        return
    
    # ========================================================
    # ========= COMPROBAR ESTADO DE AUTENTICACIÓN ============
    # ========================================================
    print("Verificando estado de autenticación...")
    r_status = session.get(f"{BASE_URL}/auth/status")
    print("GET /auth/status:", r_status.status_code, r_status.json(), "\n")

    if not r_status.ok:
        print("No hay sesión activa. Deteniendo prueba.")
        return

    # ========================================================
    # =============== CREAR UN JUEGO NUEVO ===================
    # ========================================================
    print("Creando nuevo juego...")
    nuevo_juego = {
        "nombre": "The Legend of Zelda",
        "genero": "Aventura",
        "plataforma": "Switch",
        "anio": 2017,
        "descripcion": "Aventura épica en el reino de Hyrule con Link como protagonista."
    }

    r_post = session.post(f"{BASE_URL}/juegos", json=nuevo_juego)
    try:
        print("POST /juegos:", r_post.status_code, r_post.json(), "\n")
    except Exception:
        print("POST /juegos:", r_post.status_code, r_post.text, "\n")

    # ========================================================
    # ============== LISTAR TODOS LOS JUEGOS =================
    # ========================================================
    print("Listando todos los juegos...")
    r_get = session.get(f"{BASE_URL}/juegos")
    if r_get.ok:
        juegos = r_get.json()
        print(f"GET /juegos: {r_get.status_code} - {len(juegos)} juegos encontrados\n")
    else:
        print("GET /juegos: Error", r_get.status_code, r_get.text, "\n")

    # ========================================================
    # =================== CERRAR SESIÓN ======================
    # ========================================================
    # --------------------------------------------------------
    # 5️. CERRAR SESIÓN
    # --------------------------------------------------------
    print("Cerrando sesión...")
    r_logout = session.post(f"{BASE_URL}/logout")
    print("POST /logout:", r_logout.status_code, r_logout.json(), "\n")

    # ========================================================
    # ======== VERIFICAR QUE YA NO ESTÁ AUTENTICADO ==========
    # ========================================================
    print("Verificando que la sesión esté cerrada...")
    r_status2 = session.get(f"{BASE_URL}/auth/status")
    print("GET /auth/status (tras logout):", r_status2.status_code, r_status2.json())

    print("\nPRUEBA FINALIZADA")


if __name__ == "__main__":
    test_api()