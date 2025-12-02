<!-- 
============================================================
Componente: Login.vue
============================================================
Descripción:
Vista que gestiona el inicio de sesión del usuario.
Incluye un formulario con validación básica, manejo de errores
y comunicación con el backend mediante el módulo API.
Emite un evento al componente principal al iniciar sesión correctamente.
-->

<template>
  <div class="login-page">
    <div class="login-box">
      <h2>Iniciar sesión</h2>

      <!-- Formulario de login -->
      <form @submit.prevent="login">
        <!-- Campo de usuario -->
        <div class="input-group">
          <label>Usuario</label>
          <input
            v-model="username"
            type="text"
            placeholder="Nombre de usuario"
            required
          />
        </div>

        <!-- Campo de contraseña -->
        <div class="input-group">
          <label>Contraseña</label>
          <input
            v-model="password"
            type="password"
            placeholder="Contraseña"
            required
          />
        </div>

        <!-- Botón principal de envío -->
        <button type="submit" class="login-btn">Entrar</button>

        <!-- Mensaje de error en caso de credenciales incorrectas -->
        <p v-if="error" class="error">{{ error }}</p>
      </form>
    </div>
  </div>
</template>

<script>
import { api } from "../api"; // Importa el módulo de comunicación con el backend

export default {
  name: "Login",

  data() {
    return {
      username: "", // Campo de nombre de usuario
      password: "", // Campo de contraseña
      error: "",    // Mensaje de error si la autenticación falla
    };
  },

  methods: {
    /**
     * Envía los datos del formulario al servidor.
     * Si la autenticación es correcta, almacena el nombre de usuario
     * y notifica al componente principal (App.vue).
     */
    async login() {
      this.error = "";
      try {
        const res = await api.login(this.username, this.password);

        // Si el servidor devuelve una respuesta válida
        if (res.status === 200) {
          // Guarda el nombre de usuario en localStorage
          localStorage.setItem("username", res.data.username || this.username);

          // Emite un evento al componente padre para actualizar el estado global
          this.$emit("login-success");
        }
      } catch (err) {
        // Captura errores en la petición o credenciales incorrectas
        console.error("Error en login:", err);
        this.error = "Usuario o contraseña incorrectos";
      }
    },
  },
};
</script>

<style scoped>
/* =========================================
   Estilos del formulario de inicio de sesión
========================================= */

/* Centra vertical y horizontalmente el contenedor principal */
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80vh;
}

/* Caja contenedora del formulario */
.login-box {
  background: #1e293b;
  padding: 40px;
  border-radius: 12px;
  width: 350px;
  text-align: center;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

/* Título */
h2 {
  color: #10b981;
  margin-bottom: 20px;
}

/* Grupo de cada campo del formulario */
.input-group {
  margin-bottom: 15px;
  text-align: left;
}

/* Etiquetas de los campos */
label {
  display: block;
  font-size: 14px;
  color: #94a3b8;
  margin-bottom: 5px;
}

/* Campos de entrada */
input {
  width: 100%;
  padding: 10px;
  border-radius: 6px;
  border: none;
  background: #0f172a;
  color: white;
}

/* Botón de envío */
.login-btn {
  background: #10b981;
  border: none;
  color: white;
  font-weight: bold;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
}

/* Efecto hover en el botón */
.login-btn:hover {
  background: #059669;
}

/* Mensaje de error */
.error {
  color: #ef4444;
  margin-top: 10px;
}
</style>
