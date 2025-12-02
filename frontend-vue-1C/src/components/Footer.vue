<!-- 
============================================================
Componente: Footer.vue
============================================================
Descripción:
Componente de pie de página que muestra las palabras clave 
(keywords) dinámicas de los juegos visitados o buscados. 
Permite filtrar los juegos haciendo clic en una keyword.
-->

<template>
  <footer class="app-footer">

    <!-- Tarjeta que contiene el listado de keywords -->
    <section class="keywords-card">
      <h2>Keywords</h2>

      <!-- Contenedor de etiquetas de palabras clave -->
      <div class="keywords">
        <!-- 
          Itera sobre cada keyword recibida como prop.
          Cada palabra clave se muestra como una etiqueta clicable.
          Al hacer clic, emite el evento 'filterByKeyword' al componente padre.
        -->
        <span 
          v-for="(kw, index) in keywords" 
          :key="index" 
          class="tag"
          @click="$emit('filterByKeyword', kw)"
        >
          {{ kw }}
        </span>
      </div>
    </section>

  </footer>
</template>

<script>
export default {
  name: "Footer",

  // Recibe las palabras clave desde el componente padre (App.vue)
  props: {
    keywords: {
      type: Array,
      default: () => [] // Si no se envía ninguna, usa un arreglo vacío
    }
  }
}
</script>

<style>
/* =========================================
   Estilos del footer y las palabras clave
========================================= */

/* Título del bloque de keywords */
.keywords-card h2 {
  margin-bottom: 12px;
  font-size: 18px;
  color: #f1f4f7;
}

/* Contenedor principal de etiquetas */
.keywords {
  display: flex;
  justify-content: center;
  gap: 10px;
}

/* Estilo visual de cada palabra clave */
.tag {
  background-color: #10b981; /* color verde principal */
  color: #fff;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

/* Cambio de color al pasar el cursor */
.tag:hover {
  background-color: #059669;
}
</style>
