<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="bg-white p-6 rounded-2xl shadow-md w-96">
      <h2 class="text-2xl font-bold text-center mb-4">Register</h2>

      <form @submit.prevent="handleRegister">
        <div class="mb-4">
          <label class="block text-gray-700">Name</label>
          <input v-model="name" type="text" class="w-full p-2 border rounded-lg" required />
        </div>

        <div class="mb-4">
          <label class="block text-gray-700">Email</label>
          <input v-model="email" type="email" class="w-full p-2 border rounded-lg" required />
        </div>

        <div class="mb-4">
          <label class="block text-gray-700">Password</label>
          <input v-model="password" type="password" class="w-full p-2 border rounded-lg" required />
        </div>

        <button class="w-full bg-green-500 text-white p-2 rounded-lg hover:bg-green-600">Register</button>
      </form>

      <p class="text-sm text-center mt-4">
        Already have an account?
        <router-link to="/login" class="text-blue-500">Login</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
// defineOptions({ name: "RegisterView" });
import { ref } from "vue";

const name = ref("");
const email = ref("");
const password = ref("");

function handleRegister() {
  console.log("Registering:", name.value, email.value, password.value);
  alert("Register form submitted");
}
</script>
