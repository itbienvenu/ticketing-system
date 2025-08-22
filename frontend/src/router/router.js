import { createRouter, createWebHistory } from 'vue-router'
import Login from '../components/LoginInput.vue'
import Home from '../components/DashBoard.vue'
import Register from '../components/RegisterInput.vue'
import RoutesComponent from '../components/RoutesComponent.vue'

const routes = [
  { path: '/', name: 'Login', component: Login },
  { path: '/home', name: 'Home', component: Home },
  { path: '/register', name: 'Register', component: Register },
  { path: '/routes', name: 'Routes', component: RoutesComponent },
  
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
