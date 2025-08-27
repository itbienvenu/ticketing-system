import { createRouter, createWebHistory } from 'vue-router'
import Login from '../components/LoginInput.vue'
import Home from '../components/DashBoard.vue'
import Register from '../components/RegisterInput.vue'
import RoutesComponent from '../components/RoutesComponent.vue'
import Admin from '../admin/AdminDashboard.vue'

const routes = [
  { 
    path: '/', 
    name: 'Login', 
    component: Login, 
    meta: { title: 'Login Page' } 
  },
  { 
    path: '/home', 
    name: 'Home', 
    component: Home, 
    meta: { title: 'Dashboard' } 
  },
  { 
    path: '/register', 
    name: 'Register', 
    component: Register, 
    meta: { title: 'Register Page' } 
  },
  { 
    path: '/admin', 
    name: 'Admin', 
    component: Admin, 
    meta: { title: 'Admin Page' } 
  },
  { 
    path: '/routes', 
    name: 'Routes', 
    component: RoutesComponent, 
    meta: { title: 'Routes Info' } 
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})


router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'Ticketing system'
  next()
})

export default router
