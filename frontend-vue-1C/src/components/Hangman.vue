<!-- 
============================================================
Componente: Hangman.vue
============================================================
Descripción:
Implementación del clásico juego del Ahorcado.
El jugador debe adivinar una palabra aleatoria 
introduciendo letras. 
Cuenta con un sistema visual de progreso (imágenes)
y control de intentos restantes.
-->

<template>
  <div class="hangman">
    <h2>Juego del Ahorcado</h2>

    <!-- Imagen del estado actual del personaje -->
    <img :src="currentImage" alt="Ahorcado" class="hangman-image" />

    <!-- Botón para iniciar una nueva partida -->
    <div class="button-container">
      <button @click="resetGame">Nueva partida</button>
    </div>

    <!-- Muestra la palabra con guiones o letras descubiertas -->
    <p>
      Palabra:
      <span v-for="(letter, index) in displayedWord" :key="index" class="letter">
        {{ letter }}
      </span>
    </p>

    <!-- Contador de intentos -->
    <p>Intentos restantes: {{ attemptsLeft }}</p>

    <!-- Campo de entrada para escribir una letra -->
    <input
      v-model="guess"
      @keyup.enter="makeGuess"
      maxlength="1"
      placeholder="Introduce una letra"
    />
    <button @click="makeGuess">Probar</button>

    <!-- Letras ya utilizadas -->
    <p>Letras usadas: {{ usedLetters.join(', ') }}</p>

    <!-- Mensajes de fin de partida -->
    <div v-if="gameOver" class="game-over">
      <p v-if="wordGuessed">¡Ganaste! La palabra era: {{ word }}</p>
      <p v-else>Perdiste. La palabra era: {{ word }}</p>
      <button @click="resetGame">Jugar de nuevo</button>
    </div>
  </div>
</template>

<script>
import palabras from "../palabras.json";

// Importación de las imágenes que representan los estados del juego
import img1 from "../assets/hangman/Imagen-1.jpg";
import img2 from "../assets/hangman/Imagen-2.jpg";
import img3 from "../assets/hangman/Imagen-3.jpg";
import img4 from "../assets/hangman/Imagen-4.jpg";
import img5 from "../assets/hangman/Imagen-5.jpg";
import img6 from "../assets/hangman/Imagen-6.jpg";
import img7 from "../assets/hangman/Imagen-7.jpg";

export default {
  name: "Hangman",

  data() {
    return {
      // Lista de palabras disponibles (convertidas a mayúsculas)
      words: palabras.map(p => p.toUpperCase()),

      // Palabra actual del juego
      word: "",

      // Representación visual de la palabra (guiones o letras)
      displayedWord: [],

      // Número de intentos restantes
      attemptsLeft: 6,

      // Letra que el jugador introduce
      guess: "",

      // Letras que ya se han usado
      usedLetters: [],

      // Estado del juego
      gameOver: false,
      wordGuessed: false,

      // Lista de imágenes del ahorcado según el número de fallos
      images: [img1, img2, img3, img4, img5, img6, img7]
    };
  },

  computed: {
    // Determina qué imagen mostrar según los intentos restantes
    currentImage() {
      const index = 6 - this.attemptsLeft;
      return this.images[index];
    }
  },

  // Cuando el componente se monta, inicia automáticamente una partida
  mounted() {
    this.resetGame();
  },

  methods: {
    /**
     * Reinicia el juego seleccionando una nueva palabra aleatoria.
     * Restablece todos los valores del estado del juego.
     */
    resetGame() {
      let newWord;
      do {
        newWord = this.words[Math.floor(Math.random() * this.words.length)];
      } while (newWord === this.word); // Evita repetir la misma palabra

      this.word = newWord;
      this.displayedWord = Array(this.word.length).fill("_");
      this.attemptsLeft = 6;
      this.guess = "";
      this.usedLetters = [];
      this.gameOver = false;
      this.wordGuessed = false;
    },

    /**
     * Procesa una letra introducida por el jugador.
     * Actualiza el estado del juego según si la letra es correcta o no.
     */
    makeGuess() {
      // Evita continuar si el juego ha terminado o no hay letra
      if (this.gameOver || !this.guess) return;

      const letter = this.guess.toUpperCase();

      // Si la letra ya fue usada, se ignora
      if (this.usedLetters.includes(letter)) {
        this.guess = "";
        return;
      }

      // Añadir la letra al historial de usadas
      this.usedLetters.push(letter);

      // Si la letra está en la palabra, se revela en el array mostrado
      if (this.word.includes(letter)) {
        for (let i = 0; i < this.word.length; i++) {
          if (this.word[i] === letter) {
            this.displayedWord[i] = letter;
          }
        }
      } else {
        // Si no acierta, resta un intento
        this.attemptsLeft--;
      }

      // Limpia el campo de entrada
      this.guess = "";

      // Si se completó la palabra, marca como victoria
      if (!this.displayedWord.includes("_")) {
        this.wordGuessed = true;
        this.gameOver = true;
      }

      // Si no quedan intentos, el juego termina
      if (this.attemptsLeft === 0) {
        this.gameOver = true;
      }
    }
  }
};
</script>

<style scoped>
/* =========================================
   Estilos del componente Hangman
========================================= */

.hangman {
  text-align: center;
  margin-top: 20px;
  background: #1e293b;
  border-radius: 12px;
  align-items: center;
  gap: 12px;
  padding: 16px;
}

/* Título del juego */
h2 {
  margin: 0;
  font-size: 30px;
  font-weight: bold;
  padding-bottom: 15px;
}

/* Imagen principal del ahorcado */
.hangman-image {
  width: 250px;
}

/* Contenedor del botón de nueva partida */
.button-container {
  text-align: center; 
  margin-top: 10px; 
}

/* Estilo de las letras mostradas */
.letter {
  display: inline-block;
  margin: 0 4px;
  font-size: 24px;
  font-weight: bold;
}

/* Campo de texto de entrada */
input {
  margin-top: 10px;
  margin-bottom: 10px;
  background-color: #1e293b;
  border: 1px solid #ffffff;
  color: white;
  border-radius: 5px;
  padding: 6px 8px;
}

/* Botones generales */
button {
  margin-left: 5px;
  padding: 5px 10px;
}

/* Contenedor de mensaje de fin del juego */
.game-over {
  margin-top: 15px;
}
</style>
