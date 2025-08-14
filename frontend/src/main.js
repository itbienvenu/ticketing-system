import { createApp } from 'vue'
import App from './App.vue'

import axios from 'axios';

axios.get('http://127.0.0.1:8000/api/home')
  .then(res => console.log(res.data))
  .catch(err => console.log(err));


createApp(App).mount('#app')
