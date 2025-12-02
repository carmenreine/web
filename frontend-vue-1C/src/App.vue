<!-- 
============================================================
Componente principal de la aplicación: App.vue
============================================================
Funcionalidad:
- Muestra la estructura general de la interfaz del portal.
- Gestiona autenticación, búsqueda, ordenamiento y sesión del usuario.
- Controla la navegación entre vistas (router-view) y los banners de bienvenida.
-->

<template>
  <div class="layout">

    <!-- Cabecera principal -->
    <header class="header">
      <h1 class="logo">GAME PORTAL</h1>

      <!-- Zona de filtros y controles de sesión -->
      <div class="filters">

        <!-- Barra de búsqueda -->
        <input type="text" placeholder="Search games" v-model="search" />

        <!-- Selector de orden -->
        <select v-model="sort">
          <option disabled value="">Sort by</option>
          <option value="anio">Año ascendiente (más antiguo primero)</option>
          <option value="-anio">Año descendente (más nuevo primero)</option>
          <option value="nombre">Nombre A-Z</option>
        </select>

        <!-- Controles de sesión -->
        <div class="session-controls">
          <!-- Si el usuario está autenticado -->
          <template v-if="auth">
            <span class="user-info">{{ userInfo.username || 'Admin' }}</span>
            <button @click="logout">Logout</button>
          </template>

          <!-- Si el usuario no está autenticado -->
          <template v-else>
            <router-link to="/login" class="login-link">Login</router-link>
            <router-link to="/register" class="login-link">Sign Up</router-link>
          </template>
        </div>
      </div>
    </header>

    <main>
      <!-- Vista principal si no hay autenticación -->
      <div v-if="!auth && $route.path === '/'">

        <!-- Carrusel superior de imágenes -->
        <div class="banner-wrapper">
          <button class="arrow left" @click="scrollLeft('top')">‹</button>

          <div class="banner-row" ref="bannerTop">
            <img v-for="(img, i) in bannerImages" :key="i" :src="img" alt="juego" />
          </div>

          <button class="arrow right" @click="scrollRight('top')">›</button>
        </div>

        <!-- Sección de bienvenida -->
        <div class="welcome-section">
          <h2><span class="highlight">Bienvenido a Game Portal</span></h2>
          <p class="slogan">Tu acceso a la diversión infinita</p>
          <p class="subtext">Inicia sesión o regístrate para explorar cientos de juegos.</p>
        </div>

        <!-- Carrusel inferior de imágenes -->
        <div class="banner-wrapper">
          <button class="arrow left" @click="scrollLeft('bottom')">‹</button>

          <div class="banner-row" ref="bannerBottom">
            <img v-for="(img, i) in bannerImages" :key="i" :src="img" alt="juego" />
          </div>

          <button class="arrow right" @click="scrollRight('bottom')">›</button>
        </div>
      </div>

      <!-- Contenedor de vistas según la ruta -->
      <router-view
        :search="search"
        :sort="sort"
        :userInfo="userInfo"
        @updateKeywords="updateKeywords"
        @login-success="onLoginSuccess"
        :key="$route.fullPath"
      />
    </main>

    <!-- Pie de página -->
    <footer class="app-footer">
      <section class="keywords-card">
        <h2>Keywords</h2>

        <!-- Palabras clave dinámicas -->
        <div class="keywords" v-if="keywords.length">
          <span 
            v-for="(kw, index) in keywords" 
            :key="index" 
            class="tag"
            @click="search = kw"
          >
            {{ kw }}
          </span>
        </div>

        <!-- Mensaje si no hay keywords -->
        <div v-else>
          <small>Explora juegos para ver keywords</small>
        </div>

      </section>
    </footer>

  </div>
</template>

<script>
import Footer from "./components/Footer.vue";
import { api } from "./api";

export default {
  name: "App",

  data() {
    return {
      // Imágenes del banner de bienvenida
      bannerImages: [
        new URL('@/assets/hades.png', import.meta.url).href,
        new URL('@/assets/zelda.png', import.meta.url).href,
        new URL('@/assets/stardew.png', import.meta.url).href,
        new URL('@/assets/rocketleague.png', import.meta.url).href,
        new URL('@/assets/animalcrossing.png', import.meta.url).href,
        new URL('@/assets/minecraft.png', import.meta.url).href,
        new URL('@/assets/doom.png', import.meta.url).href,
        new URL('@/assets/tetris.png', import.meta.url).href,
        new URL('@/assets/pacman.png', import.meta.url).href,
        new URL('@/assets/snake.png', import.meta.url).href
      ],
      keywords: [],
      search: '',       // Término de búsqueda
      sort: 'newest',   // Criterio de orden
      auth: false,      // Estado de autenticación
      userInfo: {},     // Datos del usuario autenticado
    }
  },

  methods: {
    // Desplaza el banner hacia la izquierda
    scrollLeft(pos) {
      const ref = pos === 'top' ? this.$refs.bannerTop : this.$refs.bannerBottom;
      if (ref) ref.scrollBy({ left: -300, behavior: 'smooth' });
    },

    // Desplaza el banner hacia la derecha
    scrollRight(pos) {
      const ref = pos === 'top' ? this.$refs.bannerTop : this.$refs.bannerBottom;
      if (ref) ref.scrollBy({ left: 300, behavior: 'smooth' });
    },

    // Actualiza las palabras clave de búsqueda
    updateKeywords(newKeywords) {
      console.log("updateKeywords recibió:", newKeywords);
      this.keywords = newKeywords;
    },

    // Comprueba si el usuario está autenticado
    async checkAuth() {
      try {
        const res = await api.checkAuth();
        this.auth = true;
        this.userInfo = {
          user_id: res.data.user_id,
          es_admin: res.data.es_admin,
          username: res.data.username,
        };
      } catch {
        this.auth = false;
        this.userInfo = {};
      }
    },

    // Cierra la sesión del usuario
    async logout() {
      try {
        await api.logout();
        this.auth = false;
        this.userInfo = {};
        this.keywords = [];
        localStorage.removeItem("username");
        this.$router.push("/");
      } catch (err) {
        console.error("Error cerrando sesión:", err);
      }
    },

    // Acción al iniciar sesión correctamente
    async onLoginSuccess() {
      await this.checkAuth();
      const storedUsername = localStorage.getItem("username");
      if (storedUsername && !this.userInfo.username) {
        this.userInfo.username = storedUsername;
      }
      const dest = this.$route.query.redirect || "/games";
      this.$router.replace(dest);
    },
  },

  // Ciclo de vida: al montar el componente, verifica autenticación
  async mounted() {
    await this.checkAuth();
  },
};
</script>

<style>
/* =========================================
   Estilos generales
========================================= */

html,
body {
  margin: 0;
  padding: 0;
  background-color: #0f172a;
  color: white;
  box-sizing: border-box;
}

/* Logo principal */
.logo {
  color: #10b981;
  font-weight: 800;
  font-size: 2rem;
  text-decoration: none;
  cursor: default;
}

/* Cabecera fija */
.header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background-color: #0f172a;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 40px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  z-index: 1000;
}

.header h1 {
  font-size: 50px;
  font-weight: bold;
}

/* Filtros (buscador y selector) */
.filters {
  display: flex;
  gap: 15px;
}

.filters input,
.filters select {
  background: #1e293b;
  border: 1px solid #334155;
  color: white;
  padding: 12px 16px;
  border-radius: 10px;
}

/* Estructura general de la página */
.layout {
  width: 100%;
  margin-top: 130px;
  padding-bottom: 120px;
}

/* Grid de juegos */
.games {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  padding-bottom: 100px;
  width: 100%;
}

/* Tarjeta de cada juego */
.game-card {
  display: flex;
  gap: 12px;
  background: #1e293b;
  padding: 16px;
  border-radius: 12px;
  align-items: center;
}

/* Imagen de portada */
.cover {
  width: 160px;
  aspect-ratio: 1 / 1;
  border-radius: 12px;
  overflow: hidden;
  flex-shrink: 0;
}

.cover img {
  width: 100%;
  height: 100%;
  display: block;
}

/* Información del juego */
.game-info h3 {
  margin: 0;
  font-size: 18px;
  font-weight: bold;
}

.game-info p {
  margin: 5px 0;
  font-size: 14px;
  color: #cbd5e1;
}

.year {
  font-size: 13px;
  color: #94a3b8;
}

/* Botones de acción */
.actions {
  margin-top: 10px;
}

button,
.play-btn {
  display: inline-block;
  margin-top: 5px;
  padding: 6px 12px;
  background: #10b981;
  border-radius: 6px;
  font-size: 14px;
  font-weight: bold;
  color: white;
  text-decoration: none;
  transition: background 0.2s;
}

.play-btn:hover {
  background: #059669;
}

/* Pie de página */
footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: #1e293b;
  color: #fff;
  padding: 15px;
  text-align: center;
  border-top: 0.5px solid rgba(255, 255, 255, 0.08);
  z-index: 2000;
}

/* Controles de sesión */
.session-controls {
  display: flex;
  align-items: center;
  gap: 12px;
}

.session-controls button,
.login-link {
  background: #10b981;
  border: none;
  border-radius: 6px;
  padding: 8px 14px;
  color: white;
  font-weight: bold;
  cursor: pointer;
  text-decoration: none;
}

.session-controls button:hover,
.login-link:hover {
  background: #059669;
}

/* Información del usuario */
.user-info {
  color: #cbd5e1;
  font-size: 15px;
}

/* Carruseles de imágenes */
.banner-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 20px auto;
  max-width: 1200px;
}

.banner-row {
  display: flex;
  gap: 20px;
  overflow-x: auto;
  overflow-y: hidden;
  scroll-behavior: smooth;
  padding: 10px 0;
  scrollbar-width: none;
}

.banner-row::-webkit-scrollbar {
  display: none;
}

.banner-row img {
  height: 120px;
  border-radius: 12px;
  flex-shrink: 0;
  object-fit: cover;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.banner-row img:hover {
  transform: scale(1.05);
}

/* Flechas de navegación en los carruseles */
.arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0, 0, 0, 0.4);
  border: none;
  color: white;
  font-size: 2rem;
  padding: 8px 14px;
  cursor: pointer;
  z-index: 2;
  border-radius: 50%;
  transition: background 0.2s ease;
}

.arrow:hover {
  background: rgba(0, 0, 0, 0.7);
}

.arrow.left { left: -30px; }
.arrow.right { right: -30px; }

/* Sección de bienvenida */
.welcome-section {
  text-align: center;
  background: rgba(11, 18, 32, 0.2);
  backdrop-filter: blur(6px);
  border-radius: 16px;
  padding: 60px 20px;
  max-width: 600px;
  margin: 0 auto;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
}

.welcome-section h2 {
  font-size: 2rem;
  margin-bottom: 10px;
}

.welcome-section .highlight {
  color: #10b981;
}

.welcome-section .slogan {
  font-size: 1.3rem;
  color: #10b981;
  margin-bottom: 10px;
}

.welcome-section .subtext {
  color: #cbd5e1;
  font-size: 0.95rem;
}
</style>
