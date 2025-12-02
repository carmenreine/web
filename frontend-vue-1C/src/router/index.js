// src/router/index.js
import { createRouter, createWebHistory } from "vue-router";
import GameList from "../components/GameList.vue";
import Hangman from '../components/Hangman.vue';
import { api } from "../api";

const routes = [
  { path: "/games", name: "Games", component: GameList, meta: { requiresAuth: true } },
  { path: "/hangman", name: "Hangman", component: () => import("../components/Hangman.vue"), meta: { requiresAuth: true } },
  { path: "/login", name: "Login", component: () => import("../components/Login.vue") },
  { path: "/register", name: "Register", component: () => import("../components/Register.vue") },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Guard global: protege /games
router.beforeEach(async (to, _from, next) => {
  if (!to.meta.requiresAuth) return next();
  try {
    const res = await api.checkAuth(); // debe devolver 200 si hay token
    if (res.status === 200 && res.data?.autenticado) return next();
  } catch (_) {}
  // sin sesión -> manda a login y luego volver a /games
  next({ name: "Login", query: { redirect: to.fullPath } });
});

export default router;
