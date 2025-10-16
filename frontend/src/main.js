/* eslint-disable */
import { createApp } from 'vue'
import App from './App.vue'
import router from './router/router'

import { isTokenValid } from './utils'

import '@fortawesome/fontawesome-free/css/all.min.css'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

// createApp(App).mount('#app')
createApp(App).use(router).mount('#app')

const API_BASE = process.env.VUE_APP_API_BASE_URL;

console.log(API_BASE)
setInterval(async () => {
  const token = localStorage.getItem("access_token");
  if (!token || isTokenValid(token)) return;

  try {
    await axios.get(`${API_BASE}/validate-token`, {
      headers: { Authorization: `Bearer ${token}` },
    });
  } catch {
    localStorage.removeItem("access_token");
    window.location.reload();
  }
}, 1000);
