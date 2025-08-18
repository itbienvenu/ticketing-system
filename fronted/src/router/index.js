import { createRouter, createWebHistory } from "vue-router";
import LoginView from "./views/LoginView.vue";
import RegisterView from "./views/RegisterView.vue";

const routes = [
  { path: "/login", name: "LoginView", component: LoginView },
  { path: "/register", name: "RegisterView", component: RegisterView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
