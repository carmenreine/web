<!-- 
============================================================
Componente: GameList.vue
============================================================
Descripción:
Vista principal que muestra la lista de videojuegos disponibles.
Permite buscar, ordenar, crear, editar y eliminar juegos (según rol).
Incluye modales para agregar y editar registros.
-->

<template>
  <div class="game-list">

    <!-- Cabecera de la lista con título y botón de añadir (solo admin) -->
    <div class="header-row">
      <h2>Lista de Juegos</h2>

      <!-- Solo visible si el usuario es administrador -->
      <button
        v-if="userInfo?.es_admin"
        class="add-btn"
        @click="mostrarModal = true"
      >
        + Añadir juego
      </button>
    </div>

    <!-- Mensajes de carga y error -->
    <div v-if="cargando" class="loading">Cargando juegos...</div>
    <div v-else-if="error" class="error">{{ error }}</div>

    <!-- Contenedor de las tarjetas de juegos -->
    <div v-else class="games">
      <div v-for="juego in juegosFiltrados" :key="juego.id" class="game-card">
        
        <!-- Imagen del juego -->
        <div class="cover">
          <img :src="getImage(juego.imagen_ruta)" alt="Portada del juego" />
        </div>

        <!-- Información del juego -->
        <div class="game-info">
          <h3>{{ juego.nombre }}</h3>
          <p><b>Género:</b> {{ juego.genero }}</p>
          <p><b>Plataforma:</b> {{ juego.plataforma }}</p>
          <p class="year"><b>Año:</b> {{ juego.anio }}</p>
          <p>{{ juego.descripcion }}</p>

          <!-- Botones de acción -->
          <div class="actions">
            <!-- Si el juego es local (Hangman), se usa una ruta interna -->
            <RouterLink
              v-if="esJuegoLocal(juego)"
              class="play-btn"
              :to="getRutaJuego(juego)"
            >
              Play
            </RouterLink>

            <!-- Si no, abre el enlace de Wikipedia en nueva pestaña -->
            <a
              v-else
              class="play-btn"
              :href="juego.wikipedia_url"
              target="_blank"
              rel="noopener noreferrer"
            >
              Play
            </a>

            <!-- Botones de edición y eliminación visibles solo para administradores -->
            <template v-if="userInfo?.es_admin">
              <button class="edit-btn" @click="editarJuego(juego)">Editar</button>
              <button class="delete-btn" @click="eliminarJuego(juego.id)">Eliminar</button>
            </template>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal para agregar nuevo juego -->
    <div v-if="mostrarModal" class="modal-backdrop" @click.self="cerrarModal">
      <div class="modal">
        <h3>Agregar nuevo juego</h3>

        <form @submit.prevent="guardarJuego">
          <input v-model="nuevoJuego.nombre" placeholder="Nombre" required />
          <input v-model="nuevoJuego.genero" placeholder="Género" required />
          <input v-model="nuevoJuego.plataforma" placeholder="Plataforma" required />
          <input v-model.number="nuevoJuego.anio" placeholder="Año" required type="number" />
          <textarea v-model="nuevoJuego.descripcion" placeholder="Descripción"></textarea>
          <input v-model="nuevoJuego.imagen_ruta" placeholder="URL de imagen (opcional)" />
          <input v-model="nuevoJuego.wikipedia_url" placeholder="URL de Wikipedia (opcional)" />

          <div class="modal-actions">
            <button type="submit" class="save-btn">Guardar</button>
            <button type="button" class="cancel-btn" @click="cerrarModal">Cancelar</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal para editar juego existente -->
    <div v-if="mostrarModalEdicion" class="modal-backdrop" @click.self="mostrarModalEdicion = false">
      <div class="modal">
        <h3>Editar juego</h3>
        <form @submit.prevent="guardarEdicion">
          <input v-model="juegoEditado.nombre" placeholder="Nombre" required />
          <input v-model="juegoEditado.genero" placeholder="Género" required />
          <input v-model="juegoEditado.plataforma" placeholder="Plataforma" required />
          <input v-model.number="juegoEditado.anio" placeholder="Año" required type="number" />
          <textarea v-model="juegoEditado.descripcion" placeholder="Descripción"></textarea>
          <input v-model="juegoEditado.imagen_ruta" placeholder="URL de imagen (opcional)" />
          <div class="modal-actions">
            <button type="submit" class="save-btn">Guardar cambios</button>
            <button type="button" class="cancel-btn" @click="mostrarModalEdicion = false">Cancelar</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>


<script>
import { api } from "../api";
import { RouterLink } from "vue-router";

export default {
  name: "GameList",
  components: { RouterLink },

  // Recibe las propiedades desde el componente principal
  props: ["search", "sort", "userInfo"],

  data() {
    return {
      juegos: [],                 // Lista de juegos obtenida desde la API
      cargando: true,             // Estado de carga inicial
      error: "",                  // Mensaje de error
      mostrarModal: false,        // Control del modal de creación
      mostrarModalEdicion: false, // Control del modal de edición

      // Objeto modelo para crear nuevo juego
      nuevoJuego: {
        nombre: "",
        genero: "",
        plataforma: "",
        anio: "",
        descripcion: "",
        imagen_ruta: "",
        wikipedia_url: ""
      },

      // Objeto modelo para editar juego existente
      juegoEditado: {
        id: null,
        nombre: "",
        genero: "",
        plataforma: "",
        anio: "",
        descripcion: "",
        imagen_ruta: "",
        wikipedia_url: ""
      }
    };
  },

  // Al montar el componente, se cargan los juegos desde el servidor
  async mounted() {
    await this.fetchGames();
  },

  computed: {
    // Aplica búsqueda y orden sobre la lista de juegos
    juegosFiltrados() {
      let lista = [...this.juegos];

      // Filtro por texto de búsqueda
      if (this.search && this.search.trim() !== "") {
        const keyword = this.search.toLowerCase();
        lista = lista.filter(j =>
          j.nombre.toLowerCase().includes(keyword) ||
          j.genero.toLowerCase().includes(keyword) ||
          j.plataforma.toLowerCase().includes(keyword) ||
          (j.descripcion || "").toLowerCase().includes(keyword)
        );
      }

      // Ordenamiento según el criterio elegido
      if (this.sort) {
        const desc = this.sort.startsWith("-");
        const key = desc ? this.sort.slice(1) : this.sort;

        lista.sort((a, b) => {
          if (a[key] < b[key]) return desc ? 1 : -1;
          if (a[key] > b[key]) return desc ? -1 : 1;
          return 0;
        });
      }
      return lista;
    }
  },

  methods: {
    // Solicita los juegos al backend
    async fetchGames() {
      try {
        const res = await api.getGames();
        this.juegos = res.data;

        // Emite al componente padre las palabras clave extraídas
        this.$emit(
          "updateKeywords",
          this.extraerKeywords(
            res.data.map(j => [j.nombre, j.genero, j.plataforma, j.descripcion].join(" "))
          )
        );
      } catch (err) {
        console.error("Error cargando juegos:", err);
        this.error = "Error al cargar los juegos. ¿Estás logueado?";
      } finally {
        this.cargando = false;
      }
    },

    // Extrae palabras clave únicas de los textos de descripción y nombre
    extraerKeywords(textos) {
      const stop = new Set(["para", "con", "este", "esta", "esto", "esas", "unos", "unas", "las", "los", "the", "and", "del", "de", "una", "uno", "por", "que", "sus", "muy"]);
      const words = textos.join(" ").toLowerCase().split(/\W+/).filter(w => w.length > 3 && !stop.has(w));
      return [...new Set(words)].slice(0, 18);
    },

    // Determina si un juego es local (no externo)
    esJuegoLocal(juego) {
      return juego.nombre.toLowerCase().includes("hangman");
    },

    // Devuelve la ruta correspondiente para juegos locales o externos
    getRutaJuego(juego) {
      if (juego.nombre.toLowerCase().includes("hangman")) {
        return "/hangman";
      }
      return "/games";
    },

    // Resuelve correctamente la URL de la imagen
    getImage(imagenUrl) {
      if (!imagenUrl || imagenUrl.trim() === "") {
        return new URL("../assets/default.jpg", import.meta.url).href;
      }

      if (imagenUrl.startsWith("http://") || imagenUrl.startsWith("https://")) {
        return imagenUrl;
      }

      return imagenUrl.startsWith("/")
        ? imagenUrl
        : `/assets/${imagenUrl}`;
    },

    // Cierra el modal de creación
    cerrarModal() {
      this.mostrarModal = false;
    },

    // Abre el modal de edición y carga los datos del juego seleccionado
    editarJuego(juego) {
      this.juegoEditado = { ...juego };
      if (!this.juegoEditado.imagen) {
        this.juegoEditado.imagen = "";
      }
      this.mostrarModalEdicion = true;
    },

    // Guarda un nuevo juego en la base de datos
    async guardarJuego() {
      try {
        if (!this.nuevoJuego.imagen_ruta || this.nuevoJuego.imagen_ruta.trim() === "") {
          this.nuevoJuego.imagen_ruta = "../assets/default.jpg";
        }

        const res = await api.createGame(this.nuevoJuego);
        console.log("Juego creado:", res.data);

        await this.fetchGames();
        this.cerrarModal();
      } catch (err) {
        console.error("Error al crear juego:", err);
        alert("No se pudo crear el juego");
      }
    },

    // Guarda los cambios realizados en un juego existente
    async guardarEdicion() {
      try {
        const res = await api.updateGame(this.juegoEditado.id, this.juegoEditado);
        console.log("Juego actualizado:", res.data);

        await this.fetchGames();
        this.mostrarModalEdicion = false;
      } catch (err) {
        console.error("Error al editar:", err.response?.status, err.response?.data);
        alert("No se pudo editar el juego");
      }
    },

    // Elimina un juego por su id
    async eliminarJuego(id) {
      console.log("eliminarJuego ejecutada", id);
      try {
        const res = await api.deleteGame(id);
        console.log("Eliminado:", res.data);
        this.juegos = this.juegos.filter(j => j.id !== id);
      } catch (err) {
        console.error("Error al eliminar:", err.response?.status, err.response?.data);
      }
    }
  },
};
</script>

<style scoped>
/* =========================================
   Estilos del listado de juegos y modales
========================================= */

/* Fondo semitransparente del modal */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(15, 23, 42, 0.9);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}

/* Contenedor del modal */
.modal {
  background: #1e293b;
  padding: 24px;
  border-radius: 12px;
  width: 400px;
  color: white;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
}

.modal h3 {
  color: #10b981;
  text-align: center;
  margin-bottom: 16px;
}

/* Campos de formulario del modal */
.modal input,
.modal textarea {
  width: 100%;
  background: #0f172a;
  color: white;
  border: 1px solid #334155;
  border-radius: 8px;
  padding: 8px;
  margin-bottom: 10px;
  font-size: 14px;
}

/* Contenedor de botones del modal */
.modal-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
}

/* Contenedor general de acciones en las tarjetas */
.actions {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  margin-top: 10px;
}

/* Botones y enlaces dentro de la tarjeta */
.actions button,
.actions a {
  display: inline-block;
  min-width: 80px;
  text-align: center;
  padding: 6px 10px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 14px;
  color: white;
  border: none;
  text-decoration: none;
  cursor: pointer;
  transition: transform 0.1s ease, background 0.2s ease;
}

/* Efecto hover en los botones */
.actions button:hover,
.actions a:hover {
  transform: scale(1.05);
}

/* Colores específicos por tipo de acción */
.play-btn {
  background-color: #10b981;
}
.play-btn:hover {
  background-color: #059669;
}

.edit-btn {
  background-color: #3b82f6;
}
.edit-btn:hover {
  background-color: #2563eb;
}

.delete-btn {
  background-color: #ef4444;
}
.delete-btn:hover {
  background-color: #dc2626;
}
</style>
