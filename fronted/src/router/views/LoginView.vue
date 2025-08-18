<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="bg-white p-6 rounded-2xl shadow-md w-96">
      <h2 class="text-2xl font-bold text-center mb-4">Login</h2>

      <form @submit.prevent="handleLogin">
        <div class="mb-4">
          <label class="block text-gray-700">Email</label>
          <input v-model="email" type="email" class="w-full p-2 border rounded-lg" required />
        </div>

        <div class="mb-4">
          <label class="block text-gray-700">Password</label>
          <input v-model="password" type="password" class="w-full p-2 border rounded-lg" required />
        </div>

        <button class="w-full bg-blue-500 text-white p-2 rounded-lg hover:bg-blue-600">Login</button>
      </form>

      <p class="text-sm text-center mt-4">
        Don’t have an account?
        <router-link to="/register" class="text-blue-500">Register</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
// defineOptions({ name: "LoginView" });
import { ref } from "vue";

const email = ref("");
const password = ref("");

function handleLogin() {
  
  console.log("Logging in with:", email.value, password.value);
  alert("Login form submitted");
}
</script>
