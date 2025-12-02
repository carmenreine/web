<!-- 
============================================================
Componente: Register.vue
============================================================
Descripción:
Vista que gestiona el registro de nuevos usuarios.
Incluye validación básica, comunicación con la API del servidor
y retroalimentación visual de éxito o error.
Tras el registro exitoso, redirige automáticamente a la página de login.
-->

<template>
  <div class="register-page">
    <div class="register-box">
      <h2>Crear cuenta</h2>

      <!-- Formulario de registro -->
      <form @submit.prevent="register">
        <!-- Campo de nombre de usuario -->
        <div class="input-group">
          <label>Usuario</label>
          <input v-model="username" type="text" placeholder="Nombre de usuario" required />
        </div>

        <!-- Campo de correo electrónico -->
        <div class="input-group">
          <label>Email</label>
          <input v-model="email" type="email" placeholder="Correo electrónico" required />
        </div>

        <!-- Campo de contraseña -->
        <div class="input-group">
          <label>Contraseña</label>
          <input v-model="password" type="password" placeholder="Contraseña" required />
        </div>

        <!-- Botón principal -->
        <button type="submit" class="register-btn">Registrarse</button>

        <!-- Mensaje de error -->
        <p v-if="error" class="error">{{ error }}</p>

        <!-- Mensaje de éxito -->
        <p v-if="success" class="success">{{ success }}</p>

        <!-- Enlace para usuarios que ya tienen cuenta -->
        <p class="login-link">
          ¿Ya tienes cuenta?
          <router-link to="/login">Inicia sesión aquí</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script>
import { api } from "../api"; // Módulo para interactuar con el backend

export default {
  name: "Register",

  data() {
    return {
      username: "",  // Nombre de usuario ingresado
      email: "",     // Correo electrónico del usuario
      password: "",  // Contraseña elegida
      error: "",     // Mensaje de error (usuario duplicado o fallo general)
      success: ""    // Mensaje de éxito tras el registro
    };
  },

  methods: {
    /**
     * Envía los datos del formulario al servidor para crear un nuevo usuario.
     * Muestra mensajes de error o éxito según la respuesta.
     * Redirige automáticamente a /login si el registro fue correcto.
     */
    async register() {
      this.error = "";
      this.success = "";

      try {
        const res = await api.register(this.username, this.email, this.password);

        // Si el servidor confirma el registro (HTTP 201)
        if (res.status === 201) {
          this.success = "Usuario registrado correctamente";
          
          // Redirección automática al login después de 1.5 segundos
          setTimeout(() => this.$router.push("/login"), 1500);
        }
      } catch (err) {
        // Si el servidor devuelve conflicto (usuario o email ya existen)
        if (err.response?.status === 409)
          this.error = "El usuario o email ya existen";
        else
          this.error = "Error al registrar usuario";
      }
    }
  }
};
</script>

<style scoped>
/* =========================================
   Estilos del formulario de registro
========================================= */

/* Centra el formulario en pantalla */
.register-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80vh;
}

/* Contenedor principal del formulario */
.register-box {
  background: #1e293b;
  padding: 40px;
  border-radius: 12px;
  width: 380px;
  text-align: center;
  box-shadow: 0 0 10px rgba(0,0,0,0.2);
}

/* Título principal */
h2 {
  color: #10b981;
  margin-bottom: 20px;
}

/* Contenedor de cada campo */
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

/* Botón de registro */
.register-btn {
  background: #10b981;
  border: none;
  color: white;
  font-weight: bold;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
}

/* Efecto hover en el botón */
.register-btn:hover {
  background: #059669;
}

/* Mensaje de error */
.error {
  color: #ef4444;
  margin-top: 10px;
}

/* Mensaje de éxito */
.success {
  color: #10b981;
  margin-top: 10px;
}

/* Enlace al login */
.login-link {
  margin-top: 15px;
  color: white;
}

/* Estilo del enlace dentro del texto */
.login-link a {
  color: white;
  font-weight: bold;
}
</style>
