<template>
  <div class="container">
    <h1>Usuarios desde la API</h1>

    <button @click="getUsers">Cargar usuarios</button>

    <div v-if="users.length" class="users">
      <div v-for="user in users" :key="user.id" class="user-card">
        <h3>{{ user.firstName }} {{ user.lastName }}</h3>
        <p class="email">{{ user.email }}</p>
      </div>
    </div>

    <p v-else>No se han cargado usuarios aún.</p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'UsersAPI',
  data() {
    return {
      users: []
    }
  },
  methods: {
    getUsers() {
      axios.get('https://dummyjson.com/users')
        .then(response => {
          this.users = response.data.users
        })
        .catch(error => {
          console.error('Hubo un error en la solicitud:', error)
        })
    }
  }
}
</script>

<style scoped>
.container {
  text-align: center;
  font-family: 'Poppins', sans-serif;
  padding: 2rem;
}

h1 {
  margin-bottom: 1rem;
  color: #1e293b;
}

button {
  background-color: #4f46e5;
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 8px;
  cursor: pointer;
  margin-bottom: 40px;
  font-weight: 500;
  font-size: 1rem;
}
button:hover {
  background-color: #4338ca;
}

.users {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px; /* Más espacio entre tarjetas */
  justify-items: center;
  padding: 0 2rem;
}

.user-card {
  background-color: #ffffff;
  border-radius: 14px;
  padding: 24px 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  width: 100%;
  max-width: 280px;
  text-align: center;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.user-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.12);
}

.user-card h3 {
  font-size: 1.15rem;
  margin-bottom: 8px;
  color: #1e293b;
  font-weight: 600;
}

.email {
  font-size: 0.80rem;
  color: #475569;
  line-height: 1.4;
  word-break: break-word; 
  max-width: 240px;
  margin: 0 auto;
}
</style>
