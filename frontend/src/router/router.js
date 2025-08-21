import { createRouter, createWebHistory } from 'vue-router'
import Login from '../components/LoginInput.vue'
import Home from '../components/DashBoard.vue'

const routes = [
  { path: '/', name: 'Login', component: Login },
  { path: '/home', name: 'Home', component: Home },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
