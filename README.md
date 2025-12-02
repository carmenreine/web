# Game Portal

Este proyecto implementa un portal de videojuegos desarrollado con Vue.js en el frontend y Flask (Python) en el backend, utilizando PostgreSQL como base de datos.

Permite registrarse, iniciar sesión como usuario particular o como administrador, explorar juegos y jugar al juego del ahorcado implementado localmente.

---

## Características principales

- Juego del ahorcado implementado localmente dentro del portal.
- Registro, inicio de sesión y cierre de sesión.
- Roles de usuario:
  - Usuario particular: puede ver y jugar.
  - Administrador: puede añadir, editar y eliminar juegos.
- El usuario administrador se crea automáticamente al iniciar el backend.
- CRUD completo de juegos (crear, leer, actualizar, eliminar) para administradores.
- Búsqueda, filtrado y ordenación de juegos.
- Interfaz con banners y pantalla de bienvenida para usuarios no autenticados.

---

## Tecnologías utilizadas

Frontend:
- Vue.js 3
- Vue Router
- Axios
- HTML5 y CSS3

Backend:
- Flask
- psycopg2 (para conexión con PostgreSQL)
- Flask-CORS
- Python `secrets` (para generación de tokens de sesión)

Base de datos:
- PostgreSQL

---

## Estructura del proyecto

- backend/
  - servidor.py — servidor Flask principal (crea las tablas y el admin por defecto)
  - cliente.py — script de prueba del servidor
- frontend/
  - src/
  - App.vue — componente raíz que contiene el layout general, cabecera, banners animados, buscador y footer con palabras clave
  - components/
    - Footer.vue — muestra las palabras clave
    - GameCard.vue — encargado de representar una tarjeta individual con la información de un videojuego
    - GameList.vue — muestra todos los juegos disponibles. Incluye filtrado, orden, botones de acción y modales para CRUD
    - Hangman.vue — juego del ahorcado implementado por nosotras
    - Login.vue — formulario de autenticación que valida credenciales con la API
    - Register.vue —
  - api.js — conexión con el backend Flask
  - router/index.js — rutas del portal
  - public/assets/ — imágenes

---

## Instalación y ejecución

### Requisitos previos
- Python 3.x  
- Node.js y npm 
- Axios 
- PostgreSQL instalado y en ejecución

---

### 1. Configuración de la base de datos

1. En PostgreSQL, crear la base de datos:

```sql
CREATE DATABASE portaljuegosdb;
```

2. Al ejecutarse por primera vez, se crearán automáticamente los elementos iniciales del sistema:

- Tablas necesarias (`usuarios`, `juegos`).
- Inserción de los juegos iniciales.
- Generación de un usuario administrador por defecto: ('admin', 'admin@portal.com', 'admin123', TRUE)

---

## Ejecución del backend

```bash
cd backend-flask-1B
python servidor.py
```

El servidor se inicia en: http://127.0.0.1:9000

### Ejecución del frontend

```bash
cd frontend-vue-1C
npm install
npm intall axios
npm run dev
```

## Autores

Leire Bernárdez Vázquez
Carmen Reiné Rueda