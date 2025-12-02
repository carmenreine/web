import { createApp } from 'vue';
import App from './App.vue';
import axiosInstance from './plugins/axios';

const app = createApp(App);

app.config.globalProperties.$axios = axiosInstance;

app.mount('#app');