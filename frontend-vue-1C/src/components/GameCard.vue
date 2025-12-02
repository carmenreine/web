<!-- 
============================================================
Componente: GameCard.vue
============================================================
Descripción:
Componente encargado de representar una tarjeta individual
con la información de un videojuego. 
Muestra imagen, datos básicos y botones de acción.
Emite eventos al padre para ejecutar las acciones "play",
"edit" y "delete".
-->

<template>
  <!-- Contenedor principal de la tarjeta del juego -->
  <article class="game-card">

    <!-- Sección de la imagen de portada -->
    <div class="cover">
      <img
        :src="game.image"                        <!-- Fuente dinámica de la imagen -->
        :alt="`${game.name} cover`"              <!-- Texto alternativo accesible -->
        loading="lazy"                           <!-- Carga diferida para optimizar -->
        @error="onError"                         <!-- Imagen de reserva si falla -->
      />
    </div>

    <!-- Sección con la información textual del juego -->
    <div class="game-info">
      <h3>{{ game.name }}</h3>
      <p><b>Género:</b> {{ game.genre }}</p>
      <p><b>Plataforma:</b> {{ game.platform }}</p>
      <p><b>Año:</b> {{ game.year }}</p>
      <p class="description">{{ game.description }}</p>

      <!-- Botones de acción -->
      <div class="actions">
        <button class="play" @click="$emit('play', game)">Play</button>
        <button class="edit" @click="$emit('edit', game)">Editar</button>
        <button class="delete" @click="$emit('delete', game)">Eliminar</button>
      </div>
    </div>
  </article>
</template>

<script>
export default {
  name: 'GameCard',

  // Propiedades recibidas desde el componente padre
  props: {
    game: { 
      type: Object, 
      required: true // Se requiere un objeto con los datos del juego
    }
  },

  // Eventos que el componente puede emitir
  emits: ['play', 'edit', 'delete'],

  methods: {
    // Manejador de error para la imagen
    // Si no se puede cargar la imagen original, usa un SVG de texto genérico
    onError(e) {
      const ph = `data:image/svg+xml;utf8,
        <svg xmlns="http://www.w3.org/2000/svg" width="800" height="500">
          <rect width="100%" height="100%" fill="#1e293b"/>
          <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle"
            font-family="Poppins,Segoe UI,sans-serif" font-size="28" fill="white">
            No cover
          </text>
        </svg>`;
      e.target.src = ph;
    }
  }
}
</script>

<style scoped>
/* =========================================
   Estilos del componente GameCard
========================================= */

/* Contenedor principal de la tarjeta */
.game-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #1e2636;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  width: 100%;
  max-width: 650px;   /* Tarjeta amplia */
  padding: 16px;
  box-sizing: border-box;
  transition: transform 0.2s ease;
  margin: 0 auto;
}

/* Efecto al pasar el cursor */
.game-card:hover {
  transform: translateY(-4px);
}

/* Contenedor de la imagen */
.cover {
  width: 100%;
  aspect-ratio: 4/2;
  border-radius: 12px;
  overflow: hidden;
  background: #0b1220;
  margin-bottom: 12px;
}

/* Imagen del juego */
.cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  display: block;
}

/* Información textual del juego */
.game-info {
  text-align: center;
  width: 100%;
}

.game-info h3 {
  font-size: 1.2rem;
  margin-bottom: 8px;
}

/* Descripción del juego */
.description {
  color: #b9c2d0;
  font-size: 0.9rem;
  margin: 8px 0;
}

/* Contenedor de botones de acción */
.actions {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 10px;
}

/* Estilo general de los botones */
.actions button {
  border: none;
  padding: 6px 10px;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  font-size: 0.85rem;
}

/* Botón: jugar */
.play {
  background: #10b981;
  color: white;
}

/* Botón: editar */
.edit {
  background: #3b82f6;
  color: white;
}

/* Botón: eliminar */
.delete {
  background: #ef4444;
  color: white;
}
</style>
