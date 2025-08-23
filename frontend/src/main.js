/* eslint-disable */
import { createApp } from 'vue'
import App from './App.vue'
import router from './router/router'

import { isTokenValid } from './utils'


import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

// createApp(App).mount('#app')
createApp(App).use(router).mount('#app')

setInterval(async () => {
  const token = localStorage.getItem("access_token");
  if (!token || isTokenValid(token)) return;

  try {
    await axios.get("http://127.0.0.1:8000/api/v1/validate-token", {
      headers: { Authorization: `Bearer ${token}` },
    });
  } catch {
    localStorage.removeItem("access_token");
    window.location.reload();
  }
}, 1000);
