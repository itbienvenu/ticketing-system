<template>
  <div class="d-flex justify-content-center align-items-center vh-100 bg-light">
    <div class="card shadow-lg border-0 p-4" style="width: 380px; background: white; border-radius: 15px;">
      
      <!-- Title -->
      <div class="text-center mb-4">
        <h2 class="fw-bold text-primary">Ticketing System</h2>
        <p class="text-muted small">Registration Panel</p>
      </div>

      <!-- Form -->
      <form @submit.prevent="register">
        <!-- Names -->
         <div class="mb-3">
          <label for="email" class="form-label fw-semibold text-dark">Names</label>
          <input
            v-model="names"
            type="text"
            id="names"
            class="form-control border-2 border-primary"
            placeholder="Enter your names"
            required
          >
        </div>
        <!-- Email -->
        <div class="mb-3">
          <label for="email" class="form-label fw-semibold text-dark">Email</label>
          <input
            v-model="email"
            type="email"
            id="email"
            class="form-control border-2 border-primary"
            placeholder="Enter your email"
            required
          >
        </div>
<!-- Phone number input box -->
         <div class="mb-3">
          <label for="email" class="form-label fw-semibold text-dark">Phone number</label>
          <input
            v-model="phone"
            type="text"
            id="phone"
            class="form-control border-2 border-primary"
            placeholder="Enter your phone number"
            required
          >
        </div>

        <!-- Password -->
        <div class="mb-3">
          <label for="password" class="form-label fw-semibold text-dark">Password</label>
          <input
            v-model="password"
            type="password"
            id="password"
            class="form-control border-2 border-primary"
            placeholder="••••••••"
            required
          >
        </div>


        <!-- Submit Button -->
        <button
          type="submit"
          class="btn w-100 fw-bold text-white d-flex justify-content-center align-items-center"
          style="background: linear-gradient(90deg, #0d6efd, #6f42c1); border-radius: 10px;"
          :disabled="loading"
        >
          <span v-if="!loading">Register</span>
          <span v-else class="spinner-border spinner-border-sm text-white" role="status"></span>
        </button>
        <br>
        <p>
          If you have an account login  <a href="/">here</a>.
        </p>
        <!-- Error Message -->
        <p v-if="errorMessage" class="text-danger mt-2">{{ errorMessage }}</p>
      </form>

    </div>
  </div>
</template>

<script setup>
 /* eslint-disable */
const API_BASE = process.env.VUE_APP_API_BASE_URL;

import { ref } from "vue"
import axios from "axios"
import { useRouter } from 'vue-router'

const email = ref("")
const names = ref("")
const password = ref("")
const phone = ref("")
const errorMessage = ref("")
const loading = ref(false)

const router = useRouter()

async function register() {
  errorMessage.value = ""
  loading.value = true

  try {
    const response = await axios.post(`${API_BASE}/register/`, {
      full_name: names.value,
      phone_number: phone.value,
      email: email.value,
      password: password.value
    }, {
      headers: { 'Content-Type': 'application/json' }
    })
    
    // Redirect to Home
    router.push('/')

  } catch (error) {
    console.error("Login error:", error)
    if (error.response && error.response.data) {
      // FastAPI returns 'detail' on errors
      errorMessage.value = error.response.data.detail || "An error occurred"
    } else {
      errorMessage.value = "An error occurred. Please try again."
    }

  } finally {
    loading.value = false
  }
}
</script>
