import axios from "axios";

const client = axios.create({
  baseURL: "http://127.0.0.1:9000",
  withCredentials: true,
});

client.interceptors.request.use((config) => {
  console.log(`[AXIOS] ${config.method.toUpperCase()} ${config.url}`, config.data || "");
  return config;
});

export const api = {
  login(username, password) {
    return client.post("/login", { username, password });
  },

  register(username, email, password) {
    return client.post("/register", { username, email, password });
  },

  getGames() {
    return client.get("/juegos");
  },

  createGame(game) {
    return client.post("/juegos", game);
  },

  updateGame(id, data) {
    return client.put(`/juegos/${id}`, data);
  },

  deleteGame(id) {
    return client.delete(`/juegos/${id}`);
  },

  checkAuth() {
    return client.get("/auth/status");
  },

  logout() {
    return client.post("/logout");
  },
};
